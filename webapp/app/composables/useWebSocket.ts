export const useWebSocket = () => {
  const newChannel = ref<Record<string, any> | null>(null)
  let ws: WebSocket | null = null

  const connect = (userId: number) => {
    if (import.meta.server) return

    const { wsUrl } = useRuntimeConfig().public
    ws = new WebSocket(`${wsUrl}/ws/${userId}`)

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.event === 'channel_added') {
        newChannel.value = data.channel
      }
    }
  }

  const disconnect = () => {
    ws?.close()
    ws = null
  }

  return { newChannel, connect, disconnect }
}
