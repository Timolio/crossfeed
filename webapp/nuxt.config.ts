import tailwindcss from '@tailwindcss/vite';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    css: ['./app/assets/css/main.css'],

    ssr: false,

    vite: {
        plugins: [tailwindcss()],
    },

    modules: ['@pinia/nuxt'],

    app: {
        head: {
            script: [
                { src: 'https://telegram.org/js/telegram-web-app.js' }
            ]
        }
    },

    runtimeConfig: {
        public: {
            apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
            wsUrl: process.env.NUXT_PUBLIC_WS_URL || 'ws://localhost:8000',
            botUsername: process.env.NUXT_PUBLIC_BOT_USERNAME || '',
        },
    },
});
