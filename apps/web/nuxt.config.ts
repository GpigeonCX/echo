export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ["~/assets/main.css"],
  app: {
    head: {
      title: "Echo 投资助手",
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api"
    }
  }
})
