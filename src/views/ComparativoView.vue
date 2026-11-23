<script setup>
import PhoneCard from '../components/PhoneCard.vue';
import galaxyImage from '../../imagem/S25Ultra.png';
import iphoneImage from '../../imagem/iphone-17-pro-max.png';

const comparisons = [1, 2, 3];

const phones = [
  {
    name: 'S25 Ultra',
    image: galaxyImage,
    description:
      'O S25 Ultra une o potente chip Snapdragon 8 Elite a 16 GB de RAM, focando em inteligência artificial e alta performance. Traz uma tela de 6,9 polegadas com cantos arredondados e um conjunto de câmeras liderado pelo sensor de 200 MP e ultra-wide de 50 MP.',
  },
  {
    name: 'iPhone 17 Pro Max',
    image: iphoneImage,
    description:
      'O iPhone 17 Pro Max combina o chip A19 Pro com 12 GB de RAM e um inédito sistema de resfriamento por câmara de vapor. Sua tela de 6,9 polegadas atinge 3.000 nits, enquanto o conjunto fotográfico agora é totalmente composto por sensores de 48 MP.',
    className: 'iphone',
  },
];
</script>

<template>
  <main class="main_comparacao">
    <section v-for="comparison in comparisons" :key="comparison" class="fora">
      <template v-for="(phone, index) in phones" :key="phone.name">
        <div v-if="index > 0" class="divisor"></div>
        <PhoneCard v-bind="phone" />
      </template>
    </section>
  </main>
  <footer>
    <p>2026 Cell Phone - ligue para um de nossos colaboradores!</p>
  </footer>
</template>
