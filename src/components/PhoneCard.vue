<script setup>
import PhoneModel from './PhoneModel.vue';

defineProps({
  name: {
    type: String,
    required: true,
  },
  visual: {
    type: Object,
    required: true,
  },
  modelo: {
    type: [String, Object],
    default: '',
  },
  description: {
    type: String,
    required: true,
  },
  selo: {
    type: String,
    default: '',
  },
  preco: {
    type: String,
    default: '',
  },
  precoAntigo: {
    type: String,
    default: '',
  },
  especificacoes: {
    type: String,
    default: '',
  },
  modeloId: {
    type: String,
    required: true,
  },
  modelos: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(['ver-detalhes', 'atualizar-modelo']);
</script>

<template>
  <section class="comparativo-card">
    <div class="comparativo-card-topo">
      <select
        class="comparativo-card-seletor"
        :value="modeloId"
        aria-label="Escolher modelo do comparativo"
        @change="emit('atualizar-modelo', $event.target.value)"
      >
        <option v-for="modelo in modelos" :key="modelo.id" :value="modelo.id">
          {{ modelo.name }}
        </option>
      </select>
      <span class="comparativo-card-seta" aria-hidden="true">⌄</span>
    </div>

    <figure class="comparativo-card-imagem">
      <PhoneModel :visual="visual" :modelo="modelo" :alt="name" />
    </figure>

    <div class="comparativo-card-info">
      <div class="comparativo-card-precos">
        <span v-if="selo" class="comparativo-selo">{{ selo }}</span>
        <strong v-if="preco">{{ preco }}</strong>
        <s v-if="precoAntigo">{{ precoAntigo }}</s>
      </div>

      <p>{{ description }}</p>

      <small v-if="especificacoes">{{ especificacoes }}</small>

      <button class="comparativo-link" type="button" @click="emit('ver-detalhes')">
        Ver detalhes →
      </button>
    </div>
  </section>
</template>
