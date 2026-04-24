export const useWebSocket = () => {
  const newChannel = ref<Record<string, any> | null>(null)
  const removedChannelId = ref<string | null>(null)
  let ws: WebSocket | null = null

  const connect = (userId: number) => {
    if (import.meta.server) return

    const { wsUrl } = useRuntimeConfig().public
    ws = new WebSocket(`${wsUrl}/ws/${userId}`)

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.event === 'channel_added') {
        newChannel.value = data.channel
      } else if (data.event === 'channel_removed') {
        removedChannelId.value = data.channel_id
      }
    }
  }

  const disconnect = () => {
    ws?.close()
    ws = null
  }

  return { newChannel, removedChannelId, connect, disconnect }
}
