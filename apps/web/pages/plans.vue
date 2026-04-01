<script setup lang="ts">
const config = useRuntimeConfig()
const { data } = await useFetch(`${config.public.apiBase}/plans`, { default: () => [] })
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Plans</p>
      <h2>进场计划</h2>
    </div>
  </section>

  <section class="card-grid">
    <article v-for="plan in data" :key="plan.name" class="card">
      <div class="section-title">
        <h3>{{ plan.name }}</h3>
        <span>{{ plan.status }}</span>
      </div>
      <ul class="simple-list">
        <li><span>总预算</span><strong>¥{{ Number(plan.total_budget).toLocaleString() }}</strong></li>
        <li><span>分批月数</span><strong>{{ plan.months }}</strong></li>
        <li><span>首月比例</span><strong>{{ (Number(plan.first_month_ratio) * 100).toFixed(0) }}%</strong></li>
        <li><span>本月应投</span><strong>¥{{ Number(plan.planned_this_month).toLocaleString() }}</strong></li>
        <li><span>本月已投</span><strong>¥{{ Number(plan.invested_this_month).toLocaleString() }}</strong></li>
      </ul>
    </article>
  </section>
</template>
