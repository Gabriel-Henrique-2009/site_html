<script setup>
import samsungLogo from '../../imagem/Samsung_Orig_Wordmark_BLACK_RGB.png';
import appleLogo from '../../imagem/Apple_logo_black.svg';

const marcas = [
  {
    nome: 'Samsung',
    logo: samsungLogo,
    className: 'samsung',
    descricao:
      'Líder em inovação de telas e câmeras, com a linha Galaxy S25 apostando em inteligência artificial e alta performance.',
    destaque: 'Galaxy S25 Ultra',
  },
  {
    nome: 'Apple',
    logo: appleLogo,
    className: 'apple',
    descricao:
      'Referência em ecossistema e performance, o iPhone 17 Pro Max chega com o chip A19 Pro e câmeras totalmente de 48 MP.',
    destaque: 'iPhone 17 Pro Max',
  },
];
</script>

<template>
  <main class="main_marcas">
    <div class="marcas">
      <div class="marcas-topo">
        <span class="comparativo-rotulo">Fabricantes</span>
        <h1>Marcas em destaque</h1>
        <p>
          Conheça de perto as marcas que acompanhamos e compare os principais lançamentos
          de cada uma delas.
        </p>
      </div>

      <section class="marcas-grade">
        <article v-for="marca in marcas" :key="marca.nome" class="marca-card">
          <figure class="marca-logo">
            <img :src="marca.logo" :alt="marca.nome" :class="marca.className" />
          </figure>

          <div class="marca-info">
            <h2>{{ marca.nome }}</h2>
            <p>{{ marca.descricao }}</p>

            <span class="marca-destaque">{{ marca.destaque }}</span>

            <RouterLink class="comparativo-botao escuro" to="/comparativo">
              Ver modelos
            </RouterLink>
          </div>
        </article>
      </section>
    </div>
  </main>
</template>
