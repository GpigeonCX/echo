<script setup lang="ts">
const links = [
  { to: "/", label: "总览" },
  { to: "/holdings", label: "持仓" },
  { to: "/plans", label: "计划" },
  { to: "/transactions", label: "交易" },
  { to: "/settings", label: "设置" }
]
</script>

<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <p class="brand-kicker">Echo</p>
        <h1>投资全景助手</h1>
      </div>
      <nav class="nav">
        <NuxtLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="nav-link"
        >
          {{ link.label }}
        </NuxtLink>
      </nav>
    </aside>
    <main class="content">
      <slot />
    </main>
  </div>
</template>
