<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
  visual: {
    type: Object,
    required: true,
  },
  alt: {
    type: String,
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

const giroX = ref(props.rx);
const giroY = ref(props.ry);
const arrastando = ref(false);
let ultimoX = 0;
let ultimoY = 0;

watch(
  () => [props.rx, props.ry],
  ([novoX, novoY]) => {
    giroX.value = novoX;
    giroY.value = novoY;
  }
);

function paraRgb(hex) {
  const h = hex.replace('#', '');
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}

function misturar(a, b, t) {
  const [r1, g1, b1] = paraRgb(a);
  const [r2, g2, b2] = paraRgb(b);
  const r = Math.round(r1 + (r2 - r1) * t);
  const g = Math.round(g1 + (g2 - g1) * t);
  const bl = Math.round(b1 + (b2 - b1) * t);
  return `rgb(${r}, ${g}, ${bl})`;
}

const camadas = computed(() => {
  const total = 18;
  const v = props.visual;

  return Array.from({ length: total }, (_, i) => {
    const t = i / (total - 1);
    const z = (0.5 - t) * 0.92;
    return {
      chave: i,
      estilo: {
        transform: `translateZ(calc(var(--d) * ${z.toFixed(3)}))`,
        background: `linear-gradient(135deg, ${misturar(v.claro, v.corpo, t)}, ${misturar(
          v.corpo,
          v.escuro,
          t
        )})`,
      },
    };
  });
});

const estiloCores = computed(() => ({
  '--claro': props.visual.claro,
  '--corpo': props.visual.corpo,
  '--escuro': props.visual.escuro,
  '--tela1': props.visual.tela1,
  '--tela2': props.visual.tela2,
  '--tela3': props.visual.tela3,
  '--aura1': props.visual.aura1,
  '--aura2': props.visual.aura2,
}));

const estiloCorpo = computed(() => ({
  transform: `rotateX(${giroX.value}deg) rotateY(${giroY.value}deg)`,
}));

function iniciar(event) {
  if (!props.interativo) {
    return;
  }
  arrastando.value = true;
  ultimoX = event.clientX;
  ultimoY = event.clientY;
  event.currentTarget.setPointerCapture?.(event.pointerId);
}

function mover(event) {
  if (!arrastando.value) {
    return;
  }
  giroY.value += (event.clientX - ultimoX) * 0.6;
  giroX.value = Math.max(-35, Math.min(35, giroX.value - (event.clientY - ultimoY) * 0.4));
  ultimoX = event.clientX;
  ultimoY = event.clientY;
}

function soltar() {
  arrastando.value = false;
}

function resetar() {
  giroX.value = props.rx;
  giroY.value = props.ry;
}

function teclar(event) {
  if (!props.interativo) {
    return;
  }

  const passo = 12;
  const teclas = {
    ArrowLeft: () => (giroY.value -= passo),
    ArrowRight: () => (giroY.value += passo),
    ArrowUp: () => (giroX.value = Math.max(-35, giroX.value - passo)),
    ArrowDown: () => (giroX.value = Math.min(35, giroX.value + passo)),
  };

  if (teclas[event.key]) {
    event.preventDefault();
    teclas[event.key]();
  }
}
</script>

<template>
  <div
    class="phone3d"
    :class="{ 'phone3d-interativo': interativo, 'phone3d-arrastando': arrastando }"
    role="img"
    :aria-label="alt"
    :tabindex="interativo ? 0 : undefined"
    :style="estiloCores"
    @pointerdown="iniciar"
    @pointermove="mover"
    @pointerup="soltar"
    @pointercancel="soltar"
    @lostpointercapture="soltar"
    @dblclick="resetar"
    @keydown="teclar"
  >
    <div class="phone3d-sombra"></div>

    <div class="phone3d-cena">
      <div class="phone3d-corpo" :style="estiloCorpo">
        <div
          v-for="camada in camadas"
          :key="camada.chave"
          class="phone3d-camada"
          :style="camada.estilo"
        ></div>

        <div class="phone3d-face phone3d-frente">
          <div class="phone3d-tela">
            <span class="phone3d-aura a"></span>
            <span class="phone3d-aura b"></span>
            <span class="phone3d-brilho"></span>
            <span v-if="visual.ilha === 'ilha'" class="phone3d-ilha"></span>
            <span v-else class="phone3d-furo"></span>
            <span class="phone3d-indicador"></span>
          </div>
        </div>

        <div class="phone3d-face phone3d-traseira">
          <div class="phone3d-modulo" :class="'modulo-' + visual.modulo">
            <span
              v-for="n in visual.lentes"
              :key="n"
              class="phone3d-lente"
            ></span>
            <span class="phone3d-flash"></span>
          </div>
          <span class="phone3d-assinatura"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.phone3d {
  --h: calc(var(--w, 11rem) * 2.05);
  --d: calc(var(--w, 11rem) * 0.105);
  --raio: calc(var(--w, 11rem) * 0.13);
  --borda: calc(var(--w, 11rem) * 0.034);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(var(--w, 11rem) * 1.6);
  height: calc(var(--h) * 1.12);
  perspective: calc(var(--w, 11rem) * 8);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.phone3d-interativo {
  cursor: grab;
  touch-action: none;
}

.phone3d-arrastando {
  cursor: grabbing;
}

.phone3d:focus-visible {
  outline: 2px solid var(--comparativo-azul);
  outline-offset: 0.6rem;
  border-radius: 1.4rem;
}

.phone3d-sombra {
  position: absolute;
  bottom: 2%;
  left: 50%;
  width: calc(var(--w) * 0.78);
  height: calc(var(--h) * 0.05);
  transform: translateX(-50%);
  border-radius: 50%;
  background: radial-gradient(closest-side, rgba(15, 20, 30, 0.4), rgba(15, 20, 30, 0));
  filter: blur(0.35rem);
  pointer-events: none;
}

.phone3d-cena {
  position: relative;
  width: var(--w);
  height: var(--h);
  transform-style: preserve-3d;
}

.phone3d-corpo {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
  transition: transform 0.55s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  will-change: transform;
}

.phone3d-arrastando .phone3d-corpo {
  transition: none;
}

.phone3d-camada {
  position: absolute;
  inset: 0;
  border-radius: var(--raio);
}

.phone3d-face {
  position: absolute;
  inset: 0;
  border-radius: var(--raio);
  backface-visibility: hidden;
}

/* FRENTE */
.phone3d-frente {
  transform: translateZ(calc(var(--d) * 0.5));
  background: linear-gradient(145deg, var(--claro), var(--corpo) 45%, var(--escuro));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.55),
    inset 0 0 0 calc(var(--w) * 0.014) rgba(0, 0, 0, 0.2);
}

.phone3d-frente::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.42),
    transparent 28%,
    transparent 72%,
    rgba(0, 0, 0, 0.16)
  );
  pointer-events: none;
}

.phone3d-tela {
  position: absolute;
  inset: var(--borda);
  border-radius: calc(var(--raio) - var(--borda) * 0.7);
  overflow: hidden;
  background: linear-gradient(160deg, var(--tela1), var(--tela2) 55%, var(--tela3));
}

.phone3d-aura {
  position: absolute;
  border-radius: 50%;
}

.phone3d-aura.a {
  top: -12%;
  right: -28%;
  width: 96%;
  aspect-ratio: 1;
  background: radial-gradient(circle, var(--aura1), transparent 68%);
  opacity: 0.9;
}

.phone3d-aura.b {
  bottom: -16%;
  left: -32%;
  width: 112%;
  aspect-ratio: 1;
  background: radial-gradient(circle, var(--aura2), transparent 68%);
  opacity: 0.85;
}

.phone3d-brilho {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    115deg,
    rgba(255, 255, 255, 0.34) 0%,
    rgba(255, 255, 255, 0.06) 30%,
    transparent 44%,
    transparent 72%,
    rgba(255, 255, 255, 0.09) 100%
  );
  mix-blend-mode: screen;
}

.phone3d-ilha {
  position: absolute;
  top: calc(var(--w) * 0.052);
  left: 50%;
  width: calc(var(--w) * 0.34);
  height: calc(var(--w) * 0.095);
  transform: translateX(-50%);
  border-radius: 999px;
  background: #05070c;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.07);
}

.phone3d-ilha::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 12%;
  width: 24%;
  aspect-ratio: 1;
  transform: translateY(-50%);
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #33487a, #0b1120 66%);
}

.phone3d-furo {
  position: absolute;
  top: calc(var(--w) * 0.058);
  left: 50%;
  width: calc(var(--w) * 0.078);
  aspect-ratio: 1;
  transform: translateX(-50%);
  border-radius: 50%;
  background: #05070c;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
}

.phone3d-furo::after {
  content: '';
  position: absolute;
  top: 28%;
  left: 30%;
  width: 30%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: rgba(120, 150, 220, 0.55);
}

.phone3d-indicador {
  position: absolute;
  bottom: calc(var(--w) * 0.032);
  left: 50%;
  width: 30%;
  height: calc(var(--w) * 0.013);
  transform: translateX(-50%);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
}

/* TRASEIRA */
.phone3d-traseira {
  transform: translateZ(calc(var(--d) * -0.5)) rotateY(180deg);
  overflow: hidden;
  background:
    radial-gradient(ellipse at 30% 8%, rgba(255, 255, 255, 0.26), transparent 52%),
    linear-gradient(150deg, var(--claro), var(--corpo) 45%, var(--escuro));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.22),
    inset 0 0 0 calc(var(--w) * 0.014) rgba(0, 0, 0, 0.16);
}

.phone3d-traseira::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    118deg,
    rgba(255, 255, 255, 0.22),
    transparent 38%,
    transparent 72%,
    rgba(0, 0, 0, 0.1)
  );
  pointer-events: none;
}

.phone3d-modulo {
  position: absolute;
  display: grid;
  place-items: center;
  padding: 7%;
  gap: 8%;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.28), rgba(0, 0, 0, 0.42));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.22),
    0 0.25rem 0.8rem rgba(0, 0, 0, 0.34);
}

.phone3d-lente {
  display: block;
  border-radius: 50%;
  background:
    radial-gradient(circle at 34% 30%, #7d8da3 0 6%, #2b3547 24%, #090d14 62%),
    #05070c;
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.55),
    inset 0 0 0 1px rgba(255, 255, 255, 0.14);
}

.phone3d-flash {
  display: block;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 35%, #fff7d6, #d9b65a 55%, #8a6c24);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
}

.phone3d-assinatura {
  position: absolute;
  bottom: 11%;
  left: 50%;
  width: 15%;
  height: 0.5%;
  min-height: 2px;
  transform: translateX(-50%);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.2);
}

/* MÓDULOS POR FABRICANTE */
.modulo-apple {
  top: 3.4%;
  right: 5.5%;
  width: 43%;
  aspect-ratio: 1;
  border-radius: 22%;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.modulo-apple .phone3d-lente {
  width: 100%;
  aspect-ratio: 1;
}

.modulo-apple .phone3d-flash {
  width: 52%;
  aspect-ratio: 1;
}

.modulo-samsung {
  top: 3.4%;
  right: 6%;
  width: 16%;
  height: 31%;
  padding: 0;
  gap: 10%;
  grid-template-columns: 1fr;
  grid-auto-rows: 1fr;
  background: transparent;
  box-shadow: none;
}

.modulo-samsung .phone3d-lente {
  width: 100%;
  aspect-ratio: 1;
}

.modulo-samsung .phone3d-flash {
  display: none;
}

.modulo-xiaomi {
  top: 2.4%;
  right: 50%;
  width: 54%;
  aspect-ratio: 1;
  transform: translateX(50%);
  border-radius: 50%;
  padding: 12%;
  gap: 9%;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.modulo-xiaomi .phone3d-lente {
  width: 100%;
  aspect-ratio: 1;
}

.modulo-xiaomi .phone3d-flash {
  width: 46%;
  aspect-ratio: 1;
}

.modulo-pixel {
  top: 2.6%;
  left: 5%;
  right: 5%;
  height: 11%;
  padding: 0 6%;
  gap: 5%;
  grid-template-columns: 1fr 1fr 1fr;
  border-radius: 999px;
}

.modulo-pixel .phone3d-lente {
  height: 58%;
  width: auto;
  aspect-ratio: 1;
}

.modulo-pixel .phone3d-flash {
  height: 42%;
  width: auto;
  aspect-ratio: 1;
}

.modulo-motorola {
  top: 3.4%;
  right: 6%;
  width: 40%;
  aspect-ratio: 1.04;
  border-radius: 26%;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.modulo-motorola .phone3d-lente {
  width: 100%;
  aspect-ratio: 1;
}

.modulo-motorola .phone3d-flash {
  width: 48%;
  aspect-ratio: 1;
}

@media (max-width: 480px) {
  .phone3d {
    width: calc(var(--w, 11rem) * 1.45);
    height: calc(var(--h) * 1.08);
  }
}
</style>
