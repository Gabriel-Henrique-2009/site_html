<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import PhoneRender from './PhoneRender.vue';

const props = defineProps({
  visual: {
    type: Object,
    required: true,
  },
  alt: {
    type: String,
    default: '',
  },
  modelo: {
    type: [String, Object],
    default: '',
  },
  interativo: {
    type: Boolean,
    default: false,
  },
  rx: {
    type: Number,
    default: -7,
  },
  ry: {
    type: Number,
    default: -24,
  },
});

const raiz = ref(null);
const canvas = ref(null);
const pronto = ref(false);

const arquivo = computed(() =>
  typeof props.modelo === 'string' ? props.modelo : props.modelo?.arquivo || ''
);

const ajuste = computed(() =>
  typeof props.modelo === 'object' && props.modelo ? props.modelo.ajuste || {} : {}
);

const materiais = computed(() =>
  typeof props.modelo === 'object' && props.modelo ? props.modelo.materiais || {} : {}
);

let THREE = null;
let renderer = null;
let cena = null;
let camera = null;
let grupo = null;
let observador = null;

let geracao = 0;
let arrastando = false;
let ultimoX = 0;
let ultimoY = 0;
let rotX = props.rx;
let rotY = props.ry;

function desenhar() {
  if (renderer && cena && camera) {
    renderer.render(cena, camera);
  }
}

function aplicarGiro() {
  if (!grupo || !THREE) {
    return;
  }
  grupo.rotation.x = THREE.MathUtils.degToRad(rotX);
  grupo.rotation.y = THREE.MathUtils.degToRad(rotY);
  desenhar();
}

function redimensionar() {
  if (!renderer || !camera || !raiz.value) {
    return;
  }

  const largura = raiz.value.clientWidth;
  const altura = raiz.value.clientHeight;

  if (!largura || !altura) {
    return;
  }

  renderer.setSize(largura, altura, false);
  camera.aspect = largura / altura;
  camera.updateProjectionMatrix();
  desenhar();
}


function papelDeParede(visual) {
  const largura = 512;
  const altura = 1024;
  const tela = document.createElement('canvas');
  tela.width = largura;
  tela.height = altura;
  const contexto = tela.getContext('2d');

  const base = contexto.createLinearGradient(0, 0, largura, altura);
  base.addColorStop(0, visual.tela1 || '#101a33');
  base.addColorStop(0.52, visual.tela2 || '#2f6fd0');
  base.addColorStop(1, visual.tela3 || '#05070d');
  contexto.fillStyle = base;
  contexto.fillRect(0, 0, largura, altura);

  const brilhos = [
    [0.78, 0.26, 0.62, visual.aura1 || '#7f9bff', 0.5],
    [0.2, 0.74, 0.7, visual.aura2 || '#b06bff', 0.5],
    [0.62, 0.52, 0.5, visual.aura1 || '#7f9bff', 0.28],
  ];
  contexto.globalCompositeOperation = 'lighter';
  brilhos.forEach(([x, y, raio, cor, alfa]) => {
    const gradiente = contexto.createRadialGradient(
      x * largura,
      y * altura,
      0,
      x * largura,
      y * altura,
      raio * largura
    );
    gradiente.addColorStop(0, cor);
    gradiente.addColorStop(1, 'rgba(0, 0, 0, 0)');
    contexto.globalAlpha = alfa;
    contexto.fillStyle = gradiente;
    contexto.fillRect(0, 0, largura, altura);
  });

  const textura = new THREE.CanvasTexture(tela);
  textura.colorSpace = THREE.SRGBColorSpace;
  textura.anisotropy = 4;
  return textura;
}

function aplicarPintura(material, cor, tipo) {
  if (!material) {
    return;
  }

  // Remove texturas originais (vermelho, floral, wallpapers aleatórios) para
  // que a cor sólida da paleta apareça de forma limpa.
  if ('map' in material) {
    material.map = null;
  }
  if ('emissiveMap' in material) {
    material.emissiveMap = null;
  }
  if (material.color) {
    material.color.set(cor);
  }
  if (material.emissive) {
    material.emissive.set(0x000000);
  }

  if (tipo === 'metal') {
    if ('metalness' in material) material.metalness = 0.9;
    if ('roughness' in material) material.roughness = 0.3;
    if ('envMapIntensity' in material) material.envMapIntensity = 1.55;
  } else if (tipo === 'escuro') {
    if ('metalness' in material) material.metalness = 0.5;
    if ('roughness' in material) material.roughness = 0.42;
    if ('envMapIntensity' in material) material.envMapIntensity = 1.1;
  } else {
    if ('metalness' in material) material.metalness = 0.25;
    if ('roughness' in material) material.roughness = 0.6;
    if ('envMapIntensity' in material) material.envMapIntensity = 0.95;
  }

  material.needsUpdate = true;
}

// Recolore as partes do GLB conforme `materiais` (modelos3d.js). Telas
// nativas (iPhone Max, Xiaomi, Pixel, Edge) já funcionam e não recebem
// wallpaper — apenas telas quebradas (S25, iPhone 17 Pro) usam `telaExtra`.
function estilizar(objeto) {
  const visual = props.visual || {};
  const config = materiais.value || {};
  const lista = (chave) => (Array.isArray(config[chave]) ? config[chave] : []);

  const corpo = lista('corpo');
  const metal = lista('metal');
  const escuro = lista('escuro');
  const telas = lista('tela');
  const telasMalhas = lista('telaMalhas');
  const ocultar = lista('ocultar');

  // Wallpaper só para telas quebradas (config.telaExtra true)
  const precisaTelaExtra = !!config.telaExtra;
  const temTelaNativa = telas.length > 0 || telasMalhas.length > 0;

  const textura = precisaTelaExtra && temTelaNativa ? papelDeParede(visual) : null;
  let materialTela = null;
  if (textura) {
    materialTela = new THREE.MeshBasicMaterial({
      map: textura,
      toneMapped: false,
      side: THREE.DoubleSide,
    });
    materialTela.name = '__tela__';
  }

  let materialTelaExtra = null;
  if (materialTela && precisaTelaExtra) {
    const texturaExtra = papelDeParede(visual);
    materialTelaExtra = materialTela.clone();
    materialTelaExtra.name = '__tela_extra__';
    materialTelaExtra.side = THREE.FrontSide;
    materialTelaExtra.transparent = true;
    materialTelaExtra.alphaTest = 0.5;
    materialTelaExtra.map = texturaExtra;
    materialTelaExtra.needsUpdate = true;
  }

  const cache = new Map();
  const descartar = new Set();

  const pintar = (material, cor, tipo) => {
    const chave = `${material.uuid}|${tipo}`;
    if (cache.has(chave)) {
      return cache.get(chave);
    }
    const copia = material.clone();
    copia.name = material.name;
    aplicarPintura(copia, cor, tipo);
    cache.set(chave, copia);
    descartar.add(material);
    return copia;
  };

  objeto.traverse((no) => {
    if (!no.isMesh) {
      return;
    }

    if (ocultar.includes(no.name)) {
      no.visible = false;
      return;
    }

    const originais = Array.isArray(no.material) ? no.material : [no.material];
    let esconder = false;

    const aplicados = originais.map((material) => {
      if (!material) {
        return material;
      }

      const nome = material.name || '';

      if (ocultar.includes(nome)) {
        esconder = true;
        return material;
      }

      // Telas nativas: aplica wallpaper só se for telaExtra (tela quebrada).
      // Senão, deixa o material original da tela (já funciona).
      if (materialTela && (telas.includes(nome) || telasMalhas.includes(no.name))) {
        return materialTela;
      }

      if (corpo.includes(nome)) {
        return pintar(material, visual.corpo || '#c2cbd9', 'corpo');
      }
      if (metal.includes(nome)) {
        return pintar(material, visual.escuro || '#6f7b90', 'metal');
      }
      if (escuro.includes(nome)) {
        return pintar(material, visual.escuro || '#6f7b90', 'escuro');
      }

      return material;
    });

    if (esconder) {
      no.visible = false;
      return;
    }

    no.material = Array.isArray(no.material) ? aplicados : aplicados[0];
  });

  // Libera apenas materiais originais que realmente saíram de uso.
  const emUso = new Set();
  objeto.traverse((no) => {
    if (!no.isMesh) {
      return;
    }
    const usados = Array.isArray(no.material) ? no.material : [no.material];
    usados.forEach((material) => material && emUso.add(material));
  });
  descartar.forEach((material) => {
    if (!emUso.has(material)) {
      material.dispose?.();
    }
  });

  return { materialTela, materialTelaExtra };
}

function limpar() {
  observador?.disconnect();
  observador = null;

  if (cena) {
    cena.traverse((no) => {
      if (!no.isMesh) {
        return;
      }
      no.geometry?.dispose();
      const materiais = Array.isArray(no.material) ? no.material : [no.material];
      materiais.forEach((material) => {
        if (!material) {
          return;
        }
        Object.values(material).forEach((valor) => {
          if (valor && valor.isTexture) {
            valor.dispose();
          }
        });
        material.dispose?.();
      });
    });
    cena.environment?.dispose();
  }

  renderer?.dispose();
  renderer = null;
  cena = null;
  camera = null;
  grupo = null;
  THREE = null;
  pronto.value = false;
}

async function iniciar() {
  if (!arquivo.value || !canvas.value || !raiz.value) {
    return;
  }

  const minhaGeracao = ++geracao;

  const modulo = await import('three');
  if (minhaGeracao !== geracao) {
    return;
  }
  THREE = modulo;

  const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  const { RoomEnvironment } = await import('three/addons/environments/RoomEnvironment.js');
  if (minhaGeracao !== geracao) {
    return;
  }

  const largura = raiz.value.clientWidth || 240;
  const altura = raiz.value.clientHeight || 300;

  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.setSize(largura, altura, false);
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  cena = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(34, largura / altura, 0.1, 100);
  camera.position.set(0, 0, 5.4);

  const pmrem = new THREE.PMREMGenerator(renderer);
  cena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();

  cena.add(new THREE.HemisphereLight(0xffffff, 0x3b4050, 1.15));

  const principal = new THREE.DirectionalLight(0xffffff, 2.6);
  principal.position.set(3, 5, 4);
  cena.add(principal);

  const recorte = new THREE.DirectionalLight(0x9db8ff, 1.3);
  recorte.position.set(-4, 2, -3);
  cena.add(recorte);

  const preenchimento = new THREE.DirectionalLight(0xffffff, 0.55);
  preenchimento.position.set(0, -3, 3);
  cena.add(preenchimento);

  grupo = new THREE.Group();
  cena.add(grupo);

  observador = new ResizeObserver(redimensionar);
  observador.observe(raiz.value);

  const carregador = new GLTFLoader();
  carregador.load(
    arquivo.value,
    (gltf) => {
      if (minhaGeracao !== geracao) {
        return;
      }

      const objeto = gltf.scene;
      const giro = ajuste.value;

      if (giro.remover?.length) {
        const alvos = [];
        objeto.traverse((no) => {
          if (giro.remover.includes(no.name)) {
            alvos.push(no);
          }
        });
        alvos.forEach((no) => no.parent?.remove(no));
      }

      const { materialTelaExtra } = estilizar(objeto);

      // O glTF pode trazer uma rotação própria na cena. O invólucro aplica a
      // rotação base no objeto e serve de referência para enquadrar/escalar.
      const involucro = new THREE.Group();
      involucro.add(objeto);
      objeto.position.set(0, 0, 0);
      objeto.rotation.set(
        THREE.MathUtils.degToRad(giro.baseX || 0),
        THREE.MathUtils.degToRad(giro.baseY || 0),
        THREE.MathUtils.degToRad(giro.baseZ || 0)
      );
      objeto.matrixAutoUpdate = true;
      objeto.updateMatrix();
      objeto.updateMatrixWorld(true);
      involucro.updateMatrixWorld(true);

      const caixa = new THREE.Box3().setFromObject(involucro);
      const tamanho = caixa.getSize(new THREE.Vector3());
      const centro = caixa.getCenter(new THREE.Vector3());
      const maior = Math.max(tamanho.x, tamanho.y, tamanho.z) || 1;
      const escala = 2.55 / maior;

      // Telas quebradas (S25, iPhone 17 Pro): malha nativa não renderiza.
      // Plano sobreposto com wallpaper cobre a frente do aparelho.
      if (materiais.value.telaExtra && materialTelaExtra) {
        const geometriaTela = new THREE.PlaneGeometry(tamanho.x * 0.9, tamanho.y * 0.93);
        const frente = new THREE.Mesh(geometriaTela, materialTelaExtra);
        frente.name = '__tela_extra__';
        frente.position.set(centro.x, centro.y, caixa.max.z + maior * 0.006);
        involucro.add(frente);
      }

      involucro.scale.multiplyScalar(escala);
      involucro.position.copy(centro).multiplyScalar(-escala);

      grupo.add(involucro);
      aplicarGiro();
      redimensionar();

      pronto.value = true;
    },
    undefined,
    () => {
      if (minhaGeracao === geracao) {
        pronto.value = false;
      }
    }
  );
}

function iniciarArrasto(event) {
  if (!props.interativo || !pronto.value) {
    return;
  }
  arrastando = true;
  ultimoX = event.clientX;
  ultimoY = event.clientY;
  event.currentTarget.setPointerCapture?.(event.pointerId);
}

function arrastar(event) {
  if (!arrastando) {
    return;
  }
  rotY += (event.clientX - ultimoX) * 0.6;
  rotX = Math.max(-35, Math.min(35, rotX - (event.clientY - ultimoY) * 0.4));
  ultimoX = event.clientX;
  ultimoY = event.clientY;
  aplicarGiro();
}

function soltar() {
  arrastando = false;
}

function teclar(event) {
  if (!props.interativo) {
    return;
  }

  const passo = 12;
  const teclas = {
    ArrowLeft: () => (rotY -= passo),
    ArrowRight: () => (rotY += passo),
    ArrowUp: () => (rotX = Math.max(-35, rotX - passo)),
    ArrowDown: () => (rotX = Math.min(35, rotX + passo)),
  };

  if (teclas[event.key]) {
    event.preventDefault();
    teclas[event.key]();
    aplicarGiro();
  }
}

watch(
  () => [props.rx, props.ry],
  ([novoX, novoY]) => {
    rotX = novoX;
    rotY = novoY;
    aplicarGiro();
  }
);

watch(arquivo, async (novo) => {
  limpar();
  if (novo) {
    await iniciar();
  }
});

onMounted(() => {
  if (arquivo.value) {
    iniciar();
  }
});

onBeforeUnmount(() => {
  geracao += 1;
  limpar();
});
</script>

<template>
  <div
    ref="raiz"
    class="phone-modelo"
    :class="{ 'phone-modelo-interativo': interativo }"
    role="img"
    :aria-label="alt"
    :tabindex="interativo ? 0 : undefined"
    @pointerdown="iniciarArrasto"
    @pointermove="arrastar"
    @pointerup="soltar"
    @pointercancel="soltar"
    @lostpointercapture="soltar"
    @keydown="teclar"
  >
    <canvas ref="canvas" v-show="pronto" class="phone-modelo-canvas"></canvas>
    <PhoneRender
      v-if="!pronto"
      :visual="visual"
      alt=""
      :interativo="interativo"
      :rx="rx"
      :ry="ry"
    />
  </div>
</template>

<style scoped>
.phone-modelo {
  --h: calc(var(--w, 11rem) * 2.05);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(var(--w, 11rem) * 1.6);
  height: calc(var(--h) * 1.12);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.phone-modelo-interativo {
  cursor: grab;
  touch-action: none;
}

.phone-modelo-interativo:active {
  cursor: grabbing;
}

.phone-modelo:focus-visible {
  outline: 2px solid var(--comparativo-azul);
  outline-offset: 0.6rem;
  border-radius: 1.4rem;
}

.phone-modelo-canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>
