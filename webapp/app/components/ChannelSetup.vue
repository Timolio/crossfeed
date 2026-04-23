<script setup lang="ts">
const props = defineProps<{ channel: Record<string, any> }>()
const emit = defineEmits<{ saved: [] }>()

const { apiUrl } = useRuntimeConfig().public
const language = ref('')
const tagInput = ref('')
const tags = ref<string[]>([])

const addTag = () => {
  const t = tagInput.value.trim()
  if (t && !tags.value.includes(t)) {
    tags.value.push(t)
  }
  tagInput.value = ''
}

const removeTag = (tag: string) => {
  tags.value = tags.value.filter(t => t !== tag)
}

const save = async () => {
  await $fetch(`${apiUrl}/api/channels/${props.channel.id}`, {
    method: 'PATCH',
    body: { language: language.value, tags: tags.value },
  })
  emit('saved')
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <p class="font-semibold text-lg">Настройка канала «{{ channel.title }}»</p>

    <div class="flex flex-col gap-1">
      <label class="text-sm text-gray-500">Язык канала</label>
      <select v-model="language" class="border rounded-lg px-3 py-2">
        <option value="">Выбери язык</option>
        <option value="ru">Русский</option>
        <option value="en">English</option>
        <option value="ua">Українська</option>
      </select>
    </div>

    <div class="flex flex-col gap-1">
      <label class="text-sm text-gray-500">Теги</label>
      <div class="flex gap-2">
        <input
          v-model="tagInput"
          placeholder="Например: tech"
          class="border rounded-lg px-3 py-2 flex-1"
          @keydown.enter.prevent="addTag"
        />
        <button class="px-4 py-2 bg-gray-100 rounded-lg" @click="addTag">+</button>
      </div>
      <div class="flex flex-wrap gap-2 mt-1">
        <span
          v-for="tag in tags"
          :key="tag"
          class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm flex items-center gap-1"
        >
          {{ tag }}
          <button class="opacity-60" @click="removeTag(tag)">×</button>
        </span>
      </div>
    </div>

    <button
      class="w-full py-3 bg-blue-500 text-white rounded-xl font-medium active:opacity-80 disabled:opacity-40"
      :disabled="!language"
      @click="save"
    >
      Сохранить
    </button>
  </div>
</template>
