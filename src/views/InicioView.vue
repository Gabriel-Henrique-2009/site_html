<script setup>
import iphoneDuoImage from '../../imagem/iphone_duo.png';
import conjuntoAppleImage from '../../imagem/conjunto_apple.png';
import celularesModelosImage from '../../imagem/3_celulares_modelos.png';
</script>

<template>
  <main id="coluna" class="inicio">
    <section class="inicio-secao">
      <div class="inicio-texto">
        <h1>Bem-vindo ao Cell Phone</h1>
        <p>
          Sua fonte principal para comparar os lançamentos mais atuais do
          mercado. Explore as especificações e descubra qual o melhor
          smartphone para você.
        </p>
      </div>
      <RouterLink
        to="/comparativo"
        class="inicio-imagem-link"
        aria-label="Ir para a página de comparativo"
      >
        <img
          class="inicio-imagem"
          :src="iphoneDuoImage"
          alt="Dois celulares segurados pelas mãos"
        />
      </RouterLink>
    </section>

    <section class="inicio-secao">
      <RouterLink
        to="/marcas"
        class="inicio-imagem-link"
        aria-label="Ir para a página de marcas"
      >
        <img
          class="inicio-imagem"
          :src="conjuntoAppleImage"
          alt="iPhone, Apple Watch e AirPods"
        />
      </RouterLink>
      <div class="inicio-texto">
        <p>
          Fique por dentro das novas tendências e acompanhe os novos
          lançamentos das marcas mais famosas. Você também, pode compará-los
          com outros aparelhos na página de comparação
        </p>
      </div>
    </section>

    <section class="inicio-secao">
      <div class="inicio-texto">
        <p>
          Veja quais especificações se adequam melhor ao seu dia-a-dia. Não se
          esqueça de comentar a sua opinião!
        </p>
      </div>
      <RouterLink
        to="/opinioes"
        class="inicio-imagem-link grande"
        aria-label="Ir para a página de opiniões"
      >
        <img
          class="inicio-imagem"
          :src="celularesModelosImage"
          alt="Celulares de diferentes marcas lado a lado"
        />
      </RouterLink>
    </section>
  </main>
</template>
