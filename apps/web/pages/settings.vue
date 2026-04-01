<script setup lang="ts">
const config = useRuntimeConfig()

const syncing = ref(false)
const syncMessage = ref("")

async function syncQuotes() {
  syncing.value = true
  syncMessage.value = ""
  try {
    const result = await $fetch(`${config.public.apiBase}/quotes/sync`, {
      method: "POST"
    })
    syncMessage.value = `同步完成：${result.synced_count} 个标的，时间 ${new Date(result.synced_at).toLocaleString()}`
  } catch {
    syncMessage.value = "行情同步失败，请检查后端日志"
  } finally {
    syncing.value = false
  }
}
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Settings</p>
      <h2>规则设置</h2>
    </div>
  </section>

  <section class="card-grid">
    <article class="card">
      <div class="section-title">
        <h3>回撤规则</h3>
      </div>
      <ul class="simple-list">
        <li>-15% 触发第一档弹药</li>
        <li>-25% 触发第二档弹药</li>
        <li>-35% 触发第三档弹药</li>
      </ul>
    </article>

    <article class="card">
      <div class="section-title">
        <h3>提醒方式</h3>
      </div>
      <ul class="simple-list">
        <li>站内提醒</li>
        <li>邮件提醒</li>
      </ul>
    </article>

    <article class="card">
      <div class="section-title">
        <h3>行情同步</h3>
      </div>
      <p class="card-label">支持自动后台同步，也支持手动立即触发。</p>
      <button class="submit-btn" :disabled="syncing" @click="syncQuotes">
        {{ syncing ? "同步中..." : "立即同步行情" }}
      </button>
      <p v-if="syncMessage" class="card-label">{{ syncMessage }}</p>
    </article>
  </section>
</template>
