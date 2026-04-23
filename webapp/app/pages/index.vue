<script setup lang="ts">
import { useWebApp } from 'vue-tg';
import { useWebSocket } from '~/composables/useWebSocket';

const { initDataUnsafe } = useWebApp();
const userId = computed(() => initDataUnsafe?.user?.id);

const { apiUrl } = useRuntimeConfig().public;
const channels = ref<Record<string, any>[]>([]);
const setupChannel = ref<Record<string, any> | null>(null);

const fetchChannels = async () => {
    if (!userId.value) return;
    channels.value = await $fetch(`${apiUrl}/api/channels/${userId.value}`);
    const incomplete = channels.value.find(c => !c.setup_complete);
    if (incomplete) setupChannel.value = incomplete;
};

const onSaved = async () => {
    setupChannel.value = null;
    await fetchChannels();
};

const { newChannel, connect, disconnect } = useWebSocket();

watch(newChannel, channel => {
    if (!channel) return;
    channels.value.push(channel);
    setupChannel.value = channel;
});

//test

onMounted(async () => {
    if (userId.value) {
        connect(userId.value);
        await fetchChannels();
    }
});

onUnmounted(() => disconnect());
</script>

<template>
    <div class="p-4 flex flex-col gap-4">
        <AddChannel />

        <div v-if="channels.length" class="flex flex-col rounded-xl overflow-hidden border border-tg-section-separator">
            <div
                v-for="(channel, i) in channels"
                :key="channel.id"
                class="p-3 bg-tg-section-bg flex items-center justify-between"
                :class="{ 'border-t border-tg-section-separator': i > 0 }"
            >
                <div>
                    <p class="font-medium text-tg-text">{{ channel.title }}</p>
                    <p class="text-sm text-tg-subtitle">
                        {{ channel.username ? '@' + channel.username : 'без username' }}
                    </p>
                </div>
                <span
                    class="text-xs px-2 py-1 rounded-full"
                    :class="channel.setup_complete ? 'text-tg-accent' : 'text-tg-destructive'"
                >
                    {{ channel.setup_complete ? 'Готов' : 'Настрой' }}
                </span>
            </div>
        </div>

        <ChannelSetup
            v-if="setupChannel"
            :channel="setupChannel"
            @saved="onSaved"
        />
    </div>
</template>
