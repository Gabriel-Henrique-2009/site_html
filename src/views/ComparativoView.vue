<script setup>
import { computed, ref } from 'vue';
import PhoneCard from '../components/PhoneCard.vue';
import PhoneModel from '../components/PhoneModel.vue';
import OfertasModal from '../components/OfertasModal.vue';
import { celulares } from '../data/celulares.js';
import { modelos3d } from '../data/modelos3d.js';

const selecionados = ref(['s25-ultra', 'iphone-17-pro-max']);

const phones = computed(() =>
  selecionados.value.map((id) => celulares.find((celular) => celular.id === id))
);

function trocarModelo(indice, id) {
  if (!id || id === selecionados.value[indice]) {
    return;
  }

  const outro = 1 - indice;

  if (selecionados.value[outro] === id) {
    selecionados.value[outro] = selecionados.value[indice];
  }

  selecionados.value[indice] = id;
}

const comparacoesRapidas = [
  {
    rotulo: 'S25 Ultra vs iPhone 17 Pro Max',
    ids: ['s25-ultra', 'iphone-17-pro-max'],
  },
  {
    rotulo: 'iPhone 17 Pro vs iPhone 12 Pro',
    ids: ['iphone-17-pro', 'iphone-12-pro'],
  },
  {
    rotulo: 'Nothing Phone (2) vs OnePlus 12',
    ids: ['nothing-phone-2', 'oneplus-12'],
  },
];

const comparacaoAtiva = computed(() =>
  comparacoesRapidas.findIndex(
    (comparacao) =>
      comparacao.ids[0] === selecionados.value[0] &&
      comparacao.ids[1] === selecionados.value[1]
  )
);

function aplicarComparacao(comparacao) {
  selecionados.value = [...comparacao.ids];
}

const abas3d = ['Celular', 'Câmera', 'Conexão', 'Tamanho', 'Tela', 'Lado a Lado'];
const aba3d = ref('Celular');
const comparar3d = ref(true);

const ofertaSelecionada = ref(null);
const ofertas = [];

function abrirOfertas(phone) {
  ofertaSelecionada.value = phone;
}

function fecharOfertas() {
  ofertaSelecionada.value = null;
}

const criterios = [
  { chave: 'desempenho', rotulo: 'Desempenho bruto', valor: 8 },
  { chave: 'camera', rotulo: 'Câmera', valor: 8 },
  { chave: 'tela', rotulo: 'Duração e tela', valor: 7 },
  { chave: 'bateria', rotulo: 'Bateria e recarga', valor: 6 },
  { chave: 'custo', rotulo: 'Custo-benefício', valor: 6 },
];

const pesos = ref(
  criterios.reduce((lista, criterio) => {
    lista[criterio.chave] = criterio.valor;
    return lista;
  }, {})
);

const radarRotulos = ['Desempenho', 'Câmera', 'Tela', 'Bateria', 'Custo', 'Portabilidade'];
const radarChaves = ['desempenho', 'camera', 'tela', 'bateria', 'custo', 'portabilidade'];
const radarCentro = 120;
const radarRaio = 82;

function radarPonto(indice, valor) {
  const angulo = (Math.PI * 2 * indice) / radarChaves.length - Math.PI / 2;
  const distancia = (valor / 100) * radarRaio;
  return [
    radarCentro + Math.cos(angulo) * distancia,
    radarCentro + Math.sin(angulo) * distancia,
  ];
}

function radarPoligono(phone) {
  return radarChaves
    .map((chave, indice) => radarPonto(indice, phone.notas[chave]).join(','))
    .join(' ');
}

const radarGrade = [25, 50, 75, 100].map((nivel) =>
  radarChaves.map((_, indice) => radarPonto(indice, nivel).join(',')).join(' ')
);

const radarEixos = radarChaves.map((chave, indice) => {
  const [x, y] = radarPonto(indice, 112);
  return {
    chave,
    x,
    y,
    rotulo: radarRotulos[indice],
    ancora: x < 105 ? 'end' : x > 135 ? 'start' : 'middle',
  };
});

const pontos = computed(() =>
  phones.value.map((phone) => {
    const somaPesos = criterios.reduce(
      (total, criterio) => total + pesos.value[criterio.chave],
      0
    );
    const soma = criterios.reduce(
      (total, criterio) => total + phone.notas[criterio.chave] * pesos.value[criterio.chave],
      0
    );
    return { ...phone, pontos: Math.round(soma / somaPesos) };
  })
);

const ranking = computed(() => [...pontos.value].sort((a, b) => b.pontos - a.pontos));
const vencedor = computed(() => ranking.value[0]);

const diferencaEspessura = computed(() => {
  const [a, b] = phones.value;
  return Math.abs(a.dimensoes.espessura - b.dimensoes.espessura)
    .toFixed(2)
    .replace('.', ',');
});

const maiorBenchmark = computed(() =>
  Math.max(...phones.value.map((phone) => phone.antutu))
);

const maiorRecarga = computed(() => Math.max(...phones.value.map((phone) => phone.recarga)));

const linhasComparativas = computed(() => [
  { rotulo: 'Chipset', valores: phones.value.map((phone) => phone.chip) },
  { rotulo: 'Memória', valores: phones.value.map((phone) => phone.ram) },
  {
    rotulo: 'Tela',
    valores: phones.value.map((phone) => `${phone.tela.tamanho} · ${phone.tela.taxa}`),
  },
  { rotulo: 'Brilho', valores: phones.value.map((phone) => phone.tela.brilho) },
  {
    rotulo: 'Câmera',
    valores: phones.value.map((phone) => `${phone.camera.principal} · ${phone.camera.zoom}`),
  },
  { rotulo: 'Bateria', valores: phones.value.map((phone) => phone.bateria) },
  { rotulo: 'Peso', valores: phones.value.map((phone) => phone.peso) },
  { rotulo: 'Espessura', valores: phones.value.map((phone) => phone.espessura) },
  {
    rotulo: 'AnTuTu',
    valores: phones.value.map((phone) => `${phone.antutu.toLocaleString('pt-BR')} pts`),
  },
]);

function formatarNumero(valor) {
  return valor.toLocaleString('pt-BR');
}

function formatarMedida(valor) {
  return String(valor).replace('.', ',');
}

function resetarPesos() {
  criterios.forEach((criterio) => {
    pesos.value[criterio.chave] = criterio.valor;
  });
}

function irParaComparacao() {
  document.getElementById('comparacao-3d')?.scrollIntoView({ behavior: 'smooth' });
}

function trocarModelos() {
  document
    .getElementById('comparativo-cards')
    ?.scrollIntoView({ behavior: 'smooth', block: 'center' });

  setTimeout(() => {
    document.querySelector('.comparativo-card-seletor')?.focus({ preventScroll: true });
  }, 450);
}

const creditos = computed(() => {
  const vistos = new Set();

  return phones.value
    .map((phone) => modelos3d[phone.id])
    .filter((credito) => {
      if (!credito?.autor || vistos.has(credito.link)) {
        return false;
      }
      vistos.add(credito.link);
      return true;
    });
});
</script>

<template>
  <main class="main_comparacao">
    <div class="comparativo">
      <div class="comparativo-topo">
        <div>
          <span class="comparativo-rotulo">Lado a lado</span>
          <h1>Comparar modelos</h1>
        </div>

        <div class="comparativo-acoes">
          <button class="comparativo-botao" type="button" @click="trocarModelos">
            ⇄ Trocar modelos
          </button>
          <button class="comparativo-botao" type="button" @click="resetarPesos">
            Limpar tudo
          </button>
          <button class="comparativo-botao escuro" type="button" @click="irParaComparacao">
            Comparar
          </button>
        </div>
      </div>

      <div class="comparativo-rapidas">
        <span>Comparações rápidas</span>
        <button
          v-for="(comparacao, indice) in comparacoesRapidas"
          :key="comparacao.rotulo"
          class="comparativo-chip"
          :class="{ ativo: comparacaoAtiva === indice }"
          type="button"
          @click="aplicarComparacao(comparacao)"
        >
          {{ comparacao.rotulo }}
        </button>
      </div>

      <section id="comparativo-cards" class="comparativo-cards">
        <PhoneCard
          v-for="(phone, indice) in phones"
          :key="indice"
          :modelo-id="phone.id"
          :modelos="celulares"
          :name="phone.name"
          :visual="phone.visual"
          :modelo="phone.modelo3d"
          :description="phone.description"
          :selo="phone.selo"
          :preco="phone.preco"
          :preco-antigo="phone.precoAntigo"
          :especificacoes="phone.especificacoes"
          @atualizar-modelo="(id) => trocarModelo(indice, id)"
          @ver-detalhes="abrirOfertas(phone)"
        />
      </section>

      <section id="comparacao-3d" class="comparativo-secao comparativo-3d">
        <div class="comparativo-secao-cabecalho">
          <div>
            <span class="comparativo-rotulo">Dimensões e espessura</span>
            <h2>Dimensões e espessura em 3D</h2>
          </div>

          <label v-if="aba3d === 'Celular'" class="comparativo-alternar">
            Comparar em 3D
            <input v-model="comparar3d" type="checkbox" />
          </label>
        </div>

        <div class="comparativo-abas">
          <button
            v-for="aba in abas3d"
            :key="aba"
            class="comparativo-aba"
            :class="{ ativa: aba3d === aba }"
            type="button"
            @click="aba3d = aba"
          >
            {{ aba }}
          </button>
        </div>

        <div v-if="aba3d === 'Celular'" class="comparativo-palco">
          <div
            v-for="phone in phones"
            :key="phone.id"
            class="comparativo-aparelho"
          >
            <PhoneModel
              :visual="phone.visual"
              :modelo="phone.modelo3d"
              :alt="phone.name"
              interativo
              :rx="comparar3d ? -7 : 0"
              :ry="comparar3d ? -24 : 0"
            />
            <span class="comparativo-medida">{{ phone.espessura }}</span>
          </div>

          <div class="comparativo-chao"></div>
        </div>

        <div v-else-if="aba3d === 'Câmera'" class="comparativo-palco-conteudo">
          <div v-for="(phone, indice) in phones" :key="indice" class="comparativo-camera">
            <figure class="comparativo-camera-foto">
              <PhoneModel
                :visual="phone.visual"
                :modelo="phone.modelo3d"
                :alt="'Câmera do ' + phone.name"
              />
            </figure>
            <div class="comparativo-camera-specs">
              <span class="comparativo-rotulo">{{ phone.apelido }}</span>
              <strong>{{ phone.camera.principal }}</strong>
              <small>
                {{ phone.camera.abertura }} · {{ phone.camera.zoom }} · frontal
                {{ phone.camera.frontal }}
              </small>
            </div>
          </div>
        </div>

        <div v-else-if="aba3d === 'Conexão'" class="comparativo-palco-conteudo">
          <div v-for="phone in phones" :key="phone.id" class="comparativo-conexao">
            <h3>{{ phone.apelido }}</h3>
            <ul>
              <li v-for="item in phone.conexao" :key="item">
                <span class="comparativo-check" aria-hidden="true">✓</span>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <div v-else-if="aba3d === 'Tamanho'" class="comparativo-palco-conteudo">
          <div v-for="(phone, indice) in phones" :key="phone.id" class="comparativo-tamanho">
            <h3>{{ phone.apelido }}</h3>

            <div class="comparativo-tamanho-linha">
              <span>Altura</span>
              <strong>{{ formatarMedida(phone.dimensoes.altura) }} mm</strong>
              <div class="comparativo-barra">
                <span
                  :class="'serie-' + indice"
                  :style="{ width: (phone.dimensoes.altura / 200) * 100 + '%' }"
                ></span>
              </div>
            </div>

            <div class="comparativo-tamanho-linha">
              <span>Largura</span>
              <strong>{{ formatarMedida(phone.dimensoes.largura) }} mm</strong>
              <div class="comparativo-barra">
                <span
                  :class="'serie-' + indice"
                  :style="{ width: (phone.dimensoes.largura / 100) * 100 + '%' }"
                ></span>
              </div>
            </div>

            <div class="comparativo-tamanho-linha">
              <span>Espessura</span>
              <strong>{{ formatarMedida(phone.dimensoes.espessura) }} mm</strong>
              <div class="comparativo-barra">
                <span
                  :class="'serie-' + indice"
                  :style="{ width: (phone.dimensoes.espessura / 10) * 100 + '%' }"
                ></span>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="aba3d === 'Tela'" class="comparativo-palco-conteudo">
          <div v-for="phone in phones" :key="phone.id" class="comparativo-tela-card">
            <span class="comparativo-rotulo">{{ phone.apelido }}</span>
            <strong class="comparativo-tela-numero">{{ phone.tela.tamanho }}</strong>
            <dl class="comparativo-tela-itens">
              <div>
                <dt>Resolução</dt>
                <dd>{{ phone.tela.resolucao }}</dd>
              </div>
              <div>
                <dt>Brilho</dt>
                <dd>{{ phone.tela.brilho }}</dd>
              </div>
              <div>
                <dt>Taxa de atualização</dt>
                <dd>{{ phone.tela.taxa }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <div v-else class="comparativo-palco-tabela">
          <table class="comparativo-tabela">
            <thead>
              <tr>
                <th scope="col">Especificação</th>
                <th v-for="phone in phones" :key="phone.id" scope="col">
                  {{ phone.apelido }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="linha in linhasComparativas" :key="linha.rotulo">
                <th scope="row">{{ linha.rotulo }}</th>
                <td v-for="(valor, indice) in linha.valores" :key="indice">{{ valor }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="aba3d === 'Celular'" class="comparativo-rodape-3d">
          <div class="comparativo-rodape-nomes">
            <span
              v-for="(phone, indice) in phones"
              :key="phone.id"
              class="comparativo-nome-chip"
            >
              <i :class="'serie-' + indice"></i>
              {{ phone.apelido }}
            </span>
          </div>
          <small>
            Diferença de espessura: {{ diferencaEspessura }} mm · arraste os modelos para girar
          </small>
        </div>

        <div v-if="creditos.length" class="comparativo-creditos">
          <span>Modelos 3D:</span>
          <a
            v-for="credito in creditos"
            :key="credito.link || credito.autor"
            :href="credito.link"
            target="_blank"
            rel="noopener"
          >
            {{ credito.autor }} · {{ credito.licenca }}
          </a>
        </div>
      </section>

      <div class="comparativo-grade-analise">
        <section class="comparativo-secao comparativo-pesos">
          <div class="comparativo-secao-cabecalho">
            <div>
              <span class="comparativo-rotulo">Do seu jeito</span>
              <h2>Ajuste seus pesos</h2>
            </div>
            <button class="comparativo-link" type="button" @click="resetarPesos">
              Restaurar
            </button>
          </div>

          <p class="comparativo-ajuda">
            Arraste os controles para dar mais importância ao que importa para você.
          </p>

          <label v-for="criterio in criterios" :key="criterio.chave" class="comparativo-peso">
            <span>{{ criterio.rotulo }}</span>
            <strong>{{ pesos[criterio.chave] }}/10</strong>
            <input
              v-model.number="pesos[criterio.chave]"
              type="range"
              min="0"
              max="10"
              step="1"
              :style="{ '--preenchimento': pesos[criterio.chave] * 10 + '%' }"
              :aria-label="criterio.rotulo"
            />
          </label>
        </section>

        <section class="comparativo-secao comparativo-radar-painel">
          <div class="comparativo-secao-cabecalho">
            <div>
              <span class="comparativo-rotulo">Visão geral</span>
              <h2>Equilíbrio por categoria</h2>
            </div>
          </div>

          <svg
            class="comparativo-radar"
            viewBox="0 0 240 240"
            role="img"
            aria-label="Gráfico de equilíbrio por categoria"
          >
            <polygon
              v-for="(grade, indice) in radarGrade"
              :key="'grade-' + indice"
              :points="grade"
              class="radar-grade"
            />
            <line
              v-for="eixo in radarEixos"
              :key="'eixo-' + eixo.chave"
              x1="120"
              y1="120"
              :x2="eixo.x"
              :y2="eixo.y"
              class="radar-eixo"
            />
            <polygon :points="radarPoligono(phones[0])" class="radar-serie-0" />
            <polygon :points="radarPoligono(phones[1])" class="radar-serie-1" />
            <text
              v-for="eixo in radarEixos"
              :key="'rotulo-' + eixo.chave"
              :x="eixo.x"
              :y="eixo.y"
              :text-anchor="eixo.ancora"
              class="radar-rotulo"
            >
              {{ eixo.rotulo }}
            </text>
          </svg>

          <div class="comparativo-legenda">
            <span><i class="serie-0"></i>{{ phones[0].apelido }}</span>
            <span><i class="serie-1"></i>{{ phones[1].apelido }}</span>
          </div>
        </section>
      </div>

      <section class="comparativo-vencedor">
        <div class="comparativo-vencedor-texto">
          <span class="comparativo-rotulo">Melhor combinação para seus pesos</span>
          <h2>{{ vencedor.name }}</h2>
          <p>
            Com os pesos que você escolheu, o {{ vencedor.apelido }} leva a melhor no
            equilíbrio geral entre os dois modelos.
          </p>
        </div>

        <div class="comparativo-pontuacoes">
          <div v-for="phone in pontos" :key="phone.id" class="comparativo-pontuacao">
            <span>{{ phone.apelido }}</span>
            <strong>{{ phone.pontos }}<small> pts</small></strong>
          </div>
        </div>

        <div class="comparativo-pontuacao-geral">
          <strong>{{ vencedor.pontos }}</strong>
          <span>de 100</span>
        </div>
      </section>

      <div class="comparativo-grade-final">
        <section class="comparativo-secao">
          <span class="comparativo-rotulo">Medições detalhadas</span>
          <h2>Benchmarks e autonomia</h2>

          <div class="comparativo-bench">
            <div v-for="(phone, indice) in phones" :key="phone.id" class="comparativo-bench-linha">
              <div class="comparativo-bench-topo">
                <span>{{ phone.apelido }}</span>
                <strong>{{ formatarNumero(phone.antutu) }} pts</strong>
              </div>
              <div class="comparativo-barra">
                <span
                  :class="'serie-' + indice"
                  :style="{ width: (phone.antutu / maiorBenchmark) * 100 + '%' }"
                ></span>
              </div>
              <small>AnTuTu v10</small>
            </div>
          </div>
        </section>

        <section class="comparativo-secao">
          <span class="comparativo-rotulo">Recarga</span>
          <h2>Estimativa na tomada</h2>

          <div class="comparativo-bench">
            <div v-for="(phone, indice) in phones" :key="phone.id" class="comparativo-bench-linha">
              <div class="comparativo-bench-topo">
                <span>{{ phone.apelido }}</span>
                <strong>{{ phone.recarga }} min</strong>
              </div>
              <div class="comparativo-barra">
                <span
                  :class="'serie-' + indice"
                  :style="{ width: (phone.recarga / maiorRecarga) * 100 + '%' }"
                ></span>
              </div>
              <small>
                {{ phone.recargaMeia }} min para 50% · {{ phone.recarga }} min para 100%
              </small>
            </div>
          </div>
        </section>
      </div>
    </div>

    <OfertasModal :phone="ofertaSelecionada" :ofertas="ofertas" @fechar="fecharOfertas" />
  </main>

  <footer>
    <p>2026 Cell Phone - ligue para um de nossos colaboradores!</p>
  </footer>
</template>
