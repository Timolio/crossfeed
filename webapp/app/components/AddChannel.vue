<script setup lang="ts">
import { useWebAppNavigation } from 'vue-tg'

const { botUsername } = useRuntimeConfig().public
const { openTelegramLink } = useWebAppNavigation()

const addChannel = () => {
  openTelegramLink(`https://t.me/${botUsername}?startchannel=setup&admin=post_messages`)
}
</script>

<template>
  <button
    class="w-full py-3 px-6 bg-tg-button text-tg-button-text rounded-xl font-medium active:opacity-80"
    @click="addChannel"
  >
    Добавить канал
  </button>
</template>
