<script setup lang="ts">
import { useWebApp } from 'vue-tg'
import { useWebSocket } from '~/composables/useWebSocket'

const { initDataUnsafe } = useWebApp()
const userId = computed(() => initDataUnsafe?.user?.id)

const { newChannel, connect, disconnect } = useWebSocket()
const setupDone = ref(false)

onMounted(() => {
  if (userId.value) {
    connect(userId.value)
  }
})

onUnmounted(() => {
  disconnect()
})
</script>

<template>
  <div class="p-4 flex flex-col gap-6">
    <template v-if="!newChannel && !setupDone">
      <p class="text-gray-600 text-sm">
        Добавь своего бота в канал чтобы начать.
      </p>
      <AddChannel />
    </template>

    <template v-else-if="newChannel && !setupDone">
      <ChannelSetup :channel="newChannel" @saved="setupDone = true" />
    </template>

    <template v-else>
      <p class="text-green-600 font-medium">Канал успешно настроен!</p>
    </template>
  </div>
</template>
