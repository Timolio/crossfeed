<script setup lang="ts">
import { useWebApp } from 'vue-tg';
import { useWebSocket } from '~/composables/useWebSocket';
import { Check, CircleAlert } from 'lucide-vue-next';

const { initDataUnsafe } = useWebApp();
const isDev = import.meta.dev;
const userId = computed(
    () => initDataUnsafe?.user?.id ?? (isDev ? 898654264 : null),
);

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

const formatCount = (n: number) => {
    if (!n) return '0';
    if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'K';
    return n.toString();
};
</script>

<template>
    <div class="p-4 flex flex-col gap-4">
        <AddChannel />

        <div
            v-if="channels.length"
            class="flex flex-col rounded-xl overflow-hidden border border-tg-section-separator"
        >
            <div
                v-for="(channel, i) in channels"
                :key="channel.id"
                class="py-3 px-4 bg-tg-section-bg flex items-center justify-between"
                :class="{ 'border-t border-tg-section-separator': i > 0 }"
            >
                <div>
                    <p class="font-medium text-tg-text">
                        {{ channel.title }}
                        <span class="text-tg-hint font-normal text-sm">
                            {{ channel.username ? '@' + channel.username : '' }}
                        </span>
                    </p>
                    <p class="text-sm text-tg-subtitle">
                        {{ formatCount(channel.member_count) }} подписчиков
                    </p>
                </div>
                <Check
                    v-if="channel.setup_complete"
                    :size="20"
                    class="text-tg-accent shrink-0"
                />
                <CircleAlert
                    v-else
                    :size="20"
                    class="text-tg-destructive shrink-0"
                />
            </div>
        </div>

        <ChannelSetup
            v-if="setupChannel"
            :channel="setupChannel"
            @saved="onSaved"
        />
    </div>
</template>
