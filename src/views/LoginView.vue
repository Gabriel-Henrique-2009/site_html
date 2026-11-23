<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <main id="coluna">
    <div class="div-login">
      <form class="login" @submit.prevent="router.push('/inicio')">
        <label for="email">E-mail:</label>
        <input id="email" type="email" autocomplete="email" />
        <label for="senha">Senha:</label>
        <input
          id="senha"
          type="password"
          autocomplete="current-password"
        />
        <input type="submit" value="Enter" />
      </form>
    </div>
  </main>
</template>
