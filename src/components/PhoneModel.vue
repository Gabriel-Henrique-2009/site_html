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
  renderer?.forceContextLoss?.();
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

      involucro.scale.multiplyScalar(escala);
      involucro.position.copy(centro).multiplyScalar(-escala);

      objeto.traverse((no) => {
        if (no.isMesh && no.material) {
          no.material.envMapIntensity = 1.15;
        }
      });

      grupo.add(involucro);
      grupo.updateMatrixWorld(true);
      const caixaMundo = new THREE.Box3().setFromObject(involucro);
      window.__phoneDebug = {
        giro,
        objRot: objeto.rotation.toArray(),
        escala,
        invPos: involucro.position.toArray(),
        worldSize: caixaMundo.getSize(new THREE.Vector3()).toArray(),
      };
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
