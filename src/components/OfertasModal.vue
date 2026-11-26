<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue';
import PhoneModel from './PhoneModel.vue';

const props = defineProps({
  phone: {
    type: Object,
    default: null,
  },
  ofertas: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['fechar']);
const botaoFechar = ref(null);

function aoTeclar(event) {
  if (event.key === 'Escape') {
    emit('fechar');
  }
}

watch(
  () => props.phone,
  async (phone) => {
    if (phone) {
      document.addEventListener('keydown', aoTeclar);
      document.body.style.overflow = 'hidden';
      await nextTick();
      botaoFechar.value?.focus();
    } else {
      document.removeEventListener('keydown', aoTeclar);
      document.body.style.overflow = '';
    }
  }
);

onBeforeUnmount(() => {
  document.removeEventListener('keydown', aoTeclar);
  document.body.style.overflow = '';
});
</script>

<template>
  <Teleport to="body">
    <div v-if="phone" class="ofertas-fundo" @click.self="emit('fechar')">
      <section
        class="ofertas-modal"
        role="dialog"
        aria-modal="true"
        :aria-label="'Ofertas para ' + phone.name"
      >
        <div class="ofertas-topo">
          <div>
            <span class="comparativo-rotulo">Onde comprar</span>
            <h2>{{ phone.name }}</h2>
          </div>
          <button
            ref="botaoFechar"
            class="ofertas-fechar"
            type="button"
            aria-label="Fechar ofertas"
            @click="emit('fechar')"
          >
            ×
          </button>
        </div>

        <div class="ofertas-aparelho">
          <figure>
            <PhoneModel :visual="phone.visual" :modelo="phone.modelo3d" :alt="phone.name" />
          </figure>
          <div>
            <span v-if="phone.selo" class="comparativo-selo">{{ phone.selo }}</span>
            <strong>{{ phone.preco }}</strong>
            <small>{{ phone.especificacoes }}</small>
          </div>
        </div>

        <ul v-if="ofertas.length" class="ofertas-lista">
          <li v-for="oferta in ofertas" :key="oferta.loja" class="oferta">
            <div>
              <strong>{{ oferta.loja }}</strong>
              <small>{{ oferta.parcelas }} · {{ oferta.frete }}</small>
            </div>
            <div class="oferta-preco">
              <strong>{{ oferta.preco }}</strong>
              <a :href="oferta.link" target="_blank" rel="noopener">Ir à loja →</a>
            </div>
          </li>
        </ul>

        <div v-else class="ofertas-vazio">
          <span class="ofertas-vazio-icone" aria-hidden="true">R$</span>
          <strong>Nenhuma oferta disponível no momento</strong>
          <p>As lojas e os preços aparecerão aqui assim que uma fonte de preços for conectada.</p>
        </div>

        <div class="ofertas-rodape">
          <small>Preços e disponibilidade podem variar sem aviso.</small>
        </div>
      </section>
    </div>
  </Teleport>
</template>
