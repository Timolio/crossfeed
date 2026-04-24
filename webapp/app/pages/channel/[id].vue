<script setup lang="ts">
import { useWebAppBackButton } from 'vue-tg'

const route = useRoute()
const router = useRouter()
const { apiUrl } = useRuntimeConfig().public

const { showBackButton, hideBackButton, onBackButtonClicked } = useWebAppBackButton()

const channel = ref<Record<string, any> | null>(null)
const language = ref('')
const tags = ref<string[]>([])
const tagInput = ref('')
const saving = ref(false)

onMounted(async () => {
    showBackButton()
    onBackButtonClicked(() => router.back())

    channel.value = await $fetch(`${apiUrl}/api/channels/channel/${route.params.id}`)
    language.value = channel.value?.language ?? ''
    tags.value = channel.value?.tags ?? []
})

onUnmounted(() => hideBackButton())

const addTag = () => {
    const t = tagInput.value.trim()
    if (t && !tags.value.includes(t)) tags.value.push(t)
    tagInput.value = ''
}

const removeTag = (tag: string) => {
    tags.value = tags.value.filter(t => t !== tag)
}

const save = async () => {
    saving.value = true
    await $fetch(`${apiUrl}/api/channels/${route.params.id}`, {
        method: 'PATCH',
        body: { language: language.value, tags: tags.value },
    })
    saving.value = false
    router.back()
}

const formatCount = (n: number) => {
    if (!n) return '0'
    if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'K'
    return n.toString()
}
</script>

<template>
    <div v-if="channel" class="p-4 flex flex-col gap-4">
        <div class="p-4 bg-tg-section-bg rounded-xl border border-tg-section-separator">
            <p class="font-semibold text-tg-text text-lg">{{ channel.title }}</p>
            <p class="text-sm text-tg-hint">{{ channel.username ? '@' + channel.username : 'без username' }}</p>
            <p class="text-sm text-tg-subtitle mt-1">{{ formatCount(channel.member_count) }} подписчиков</p>
        </div>

        <div class="flex flex-col gap-3">
            <div class="flex flex-col gap-1">
                <p class="text-xs text-tg-section-header uppercase px-1">Язык канала</p>
                <select v-model="language" class="bg-tg-section-bg text-tg-text border border-tg-section-separator rounded-xl px-3 py-2.5">
                    <option value="">Выбери язык</option>
                    <option value="ru">Русский</option>
                    <option value="en">English</option>
                    <option value="ua">Українська</option>
                </select>
            </div>

            <div class="flex flex-col gap-1">
                <p class="text-xs text-tg-section-header uppercase px-1">Теги</p>
                <div class="flex gap-2">
                    <input
                        v-model="tagInput"
                        placeholder="Например: tech"
                        class="bg-tg-section-bg text-tg-text border border-tg-section-separator rounded-xl px-3 py-2.5 flex-1"
                        @keydown.enter.prevent="addTag"
                    />
                    <button class="px-4 py-2 bg-tg-section-bg border border-tg-section-separator rounded-xl text-tg-text" @click="addTag">+</button>
                </div>
                <div class="flex flex-wrap gap-2 mt-1">
                    <span
                        v-for="tag in tags"
                        :key="tag"
                        class="bg-tg-button/10 text-tg-button px-3 py-1 rounded-full text-sm flex items-center gap-1"
                    >
                        {{ tag }}
                        <button class="opacity-60" @click="removeTag(tag)">×</button>
                    </span>
                </div>
            </div>
        </div>

        <button
            class="w-full py-3 bg-tg-button text-tg-button-text rounded-xl font-medium active:opacity-80 disabled:opacity-40"
            :disabled="!language || saving"
            @click="save"
        >
            {{ saving ? 'Сохраняем...' : 'Сохранить' }}
        </button>
    </div>
</template>
