<script setup>
import { computed, ref } from 'vue';

const avaliacoes = [
  {
    nome: 'João Silva',
    modelo: 'S25 Ultra',
    nota: 5,
    data: '12 nov 2026',
    comentario:
      'O S25 Ultra é incrível, a bateria dura o dia todo e a tela não reflete quase nada no sol.',
  },
  {
    nome: 'Maria Souza',
    modelo: 'iPhone 17 Pro Max',
    nota: 5,
    data: '08 nov 2026',
    comentario:
      'A câmera do iPhone 17 Pro Max não tem comparação em vídeos. A estabilização é absurda.',
  },
  {
    nome: 'Carlos Lima',
    modelo: 'S25 Ultra',
    nota: 4,
    data: '03 nov 2026',
    comentario:
      'A câmera de 200 MP entrega muito detalhe, mas o app ainda demora um pouco para abrir.',
  },
  {
    nome: 'Ana Beatriz',
    modelo: 'iPhone 17 Pro Max',
    nota: 5,
    data: '28 out 2026',
    comentario:
      'Vim de um iPhone 13 e a diferença na tela de 3.000 nits é gritante. Vale cada centavo.',
  },
  {
    nome: 'Rafael Nunes',
    modelo: 'S25 Ultra',
    nota: 5,
    data: '21 out 2026',
    comentario:
      'O Snapdragon 8 Elite roda tudo no máximo sem esquentar. Excelente para jogos.',
  },
  {
    nome: 'Juliana Alves',
    modelo: 'iPhone 17 Pro Max',
    nota: 4,
    data: '15 out 2026',
    comentario: 'Bateria ótima, mas senti falta de um carregador na caixa.',
  },
  {
    nome: 'Pedro Santos',
    modelo: 'S25 Ultra',
    nota: 3,
    data: '09 out 2026',
    comentario:
      'A S Pen continua sendo o diferencial para mim, mas achei o aparelho um pouco pesado.',
  },
  {
    nome: 'Laura Ferreira',
    modelo: 'iPhone 17 Pro Max',
    nota: 5,
    data: '02 out 2026',
    comentario:
      'O resfriamento por câmara de vapor faz diferença em gravações longas. Não travou nenhuma vez.',
  },
];

const filtros = ['Todos', 'S25 Ultra', 'iPhone 17 Pro Max'];
const filtroAtivo = ref('Todos');

const avaliacoesFiltradas = computed(() => {
  if (filtroAtivo.value === 'Todos') {
    return avaliacoes;
  }
  return avaliacoes.filter((avaliacao) => avaliacao.modelo === filtroAtivo.value);
});

const media = computed(() => {
  const soma = avaliacoes.reduce((total, avaliacao) => total + avaliacao.nota, 0);
  return (soma / avaliacoes.length).toFixed(1).replace('.', ',');
});

const aprovacao = computed(() =>
  ['S25 Ultra', 'iPhone 17 Pro Max'].map((modelo) => {
    const doModelo = avaliacoes.filter((avaliacao) => avaliacao.modelo === modelo);
    const positivas = doModelo.filter((avaliacao) => avaliacao.nota >= 4).length;
    return {
      modelo,
      positivas,
      total: doModelo.length,
      percentual: Math.round((positivas / doModelo.length) * 100),
      classe: modelo === 'S25 Ultra' ? 'serie-0' : 'serie-1',
    };
  })
);

function iniciais(nome) {
  const partes = nome.split(' ');
  const primeira = partes[0]?.[0] ?? '';
  const ultima = partes[partes.length - 1]?.[0] ?? '';
  return (primeira + ultima).toUpperCase();
}
</script>

<template>
  <main class="main_opinioes">
    <div class="opinioes">
      <div class="opinioes-topo">
        <div>
          <span class="comparativo-rotulo">Quem já usou</span>
          <h1>O que dizem os usuários</h1>
          <p>
            Opiniões de quem acompanha os lançamentos com a gente e conta o que achou na
            prática.
          </p>
        </div>

        <div class="opinioes-resumo">
          <strong>{{ media }}</strong>
          <div class="opiniao-estrelas" aria-hidden="true">
            <span v-for="n in 5" :key="n" class="opiniao-estrela ativa">★</span>
          </div>
          <span>{{ avaliacoes.length }} avaliações</span>
        </div>
      </div>

      <div class="opinioes-filtros">
        <button
          v-for="filtro in filtros"
          :key="filtro"
          class="comparativo-chip"
          :class="{ ativo: filtroAtivo === filtro }"
          type="button"
          @click="filtroAtivo = filtro"
        >
          {{ filtro }}
        </button>
      </div>

      <section class="opinioes-grade">
        <article
          v-for="avaliacao in avaliacoesFiltradas"
          :key="avaliacao.nome + avaliacao.data"
          class="opiniao-card"
        >
          <div class="opiniao-cabecalho">
            <span class="opiniao-avatar">{{ iniciais(avaliacao.nome) }}</span>
            <div>
              <strong>{{ avaliacao.nome }}</strong>
              <small>{{ avaliacao.modelo }} · {{ avaliacao.data }}</small>
            </div>
          </div>

          <div class="opiniao-estrelas" :aria-label="`${avaliacao.nota} de 5 estrelas`">
            <span
              v-for="n in 5"
              :key="n"
              class="opiniao-estrela"
              :class="{ ativa: n <= avaliacao.nota }"
              aria-hidden="true"
            >
              ★
            </span>
          </div>

          <p>{{ avaliacao.comentario }}</p>
        </article>
      </section>

      <p v-if="!avaliacoesFiltradas.length" class="opinioes-vazio">
        Ainda não há avaliações para este modelo.
      </p>

      <section class="opinioes-aprovacao">
        <div class="comparativo-secao-cabecalho">
          <div>
            <span class="comparativo-rotulo">Índice de aprovação</span>
            <h2>Aprovação por modelo</h2>
          </div>
          <small>{{ avaliacoes.length }} avaliações no total</small>
        </div>

        <div class="comparativo-bench">
          <div v-for="item in aprovacao" :key="item.modelo" class="comparativo-bench-linha">
            <div class="comparativo-bench-topo">
              <span>{{ item.modelo }}</span>
              <strong>{{ item.percentual }}%</strong>
            </div>
            <div class="comparativo-barra">
              <span :class="item.classe" :style="{ width: item.percentual + '%' }"></span>
            </div>
            <small>
              {{ item.positivas }} de {{ item.total }} avaliações com 4 estrelas ou mais
            </small>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>
