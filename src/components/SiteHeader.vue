<script setup>
import { onMounted, ref } from 'vue';
import settingsIcon from '../../imagem/18432.png';
import phoneIcon from '../../imagem/cell_phone_icon.svg';

const isDark = ref(false);

function toggleTheme() {
  isDark.value = !isDark.value;
  document.body.classList.toggle('modo-escuro', isDark.value);
  localStorage.setItem('cell-phone-theme', isDark.value ? 'dark' : 'light');
}

onMounted(() => {
  isDark.value = localStorage.getItem('cell-phone-theme') === 'dark';
  document.body.classList.toggle('modo-escuro', isDark.value);
});
</script>

<template>
  <header>
    <nav aria-label="Navegação principal">
      <RouterLink to="/inicio" class="logo">
        <img :src="phoneIcon" alt="" />
        <span>Cell Phone</span>
      </RouterLink>
      <ul class="nav-links">
        <li><RouterLink to="/inicio">Início</RouterLink></li>
        <li><RouterLink to="/comparativo">Comparativo</RouterLink></li>
        <li><RouterLink to="/marcas">Marcas</RouterLink></li>
        <li><RouterLink to="/opinioes">Opiniões</RouterLink></li>
        <li><RouterLink to="/login">Login</RouterLink></li>
      </ul>
      <div class="nav-acoes">
        <RouterLink to="/opinioes" class="botao-sugestao">
          Sugestão
        </RouterLink>
        <span id="config">
          <button type="button" aria-label="Abrir configurações">
            <img :src="settingsIcon" alt="" />
          </button>
          <ul>
            <li>
              <button id="tema" type="button" @click="toggleTheme">
                Tema - {{ isDark ? 'claro' : 'escuro' }}
              </button>
            </li>
          </ul>
        </span>
      </div>
    </nav>
  </header>
</template>
