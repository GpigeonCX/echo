<script setup lang="ts">
const config = useRuntimeConfig()

const { data } = await useFetch(`${config.public.apiBase}/dashboard/summary`, {
  default: () => ({
    total_assets: 0,
    cash_assets: 0,
    unrealized_pnl: 0,
    drawdown_rate: 0,
    peak_assets: 0,
    max_drawdown_rate: 0,
    drawdown_stage: "none",
    allocation: [],
    rebalance_suggestions: [],
    alerts: []
  })
})

const cards = computed(() => [
  { label: "总资产", value: `¥${Number(data.value.total_assets).toLocaleString()}` },
  { label: "现金仓", value: `¥${Number(data.value.cash_assets).toLocaleString()}` },
  { label: "浮动收益", value: `¥${Number(data.value.unrealized_pnl).toLocaleString()}` },
  { label: "当前回撤", value: `${(Number(data.value.drawdown_rate) * 100).toFixed(2)}%` },
  { label: "历史峰值", value: `¥${Number(data.value.peak_assets).toLocaleString()}` },
  { label: "最大回撤", value: `${(Number(data.value.max_drawdown_rate) * 100).toFixed(2)}%` }
])
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Dashboard</p>
      <h2>组合总览</h2>
    </div>
    <div class="badge">自动跟踪版本 v0.2</div>
  </section>

  <section class="card-grid">
    <article v-for="card in cards" :key="card.label" class="card metric-card">
      <p class="card-label">{{ card.label }}</p>
      <h3>{{ card.value }}</h3>
    </article>
  </section>

  <section class="split-grid">
    <article class="card">
      <div class="section-title">
        <h3>资产分布</h3>
        <span>按金额</span>
      </div>
      <ul class="simple-list">
        <li v-for="item in data.allocation" :key="item.name">
          <span>{{ item.name }}</span>
          <strong>¥{{ Number(item.value).toLocaleString() }}</strong>
        </li>
      </ul>
    </article>

    <article class="card">
      <div class="section-title">
        <h3>提醒</h3>
        <span>站内 / 邮件</span>
      </div>
      <ul class="simple-list">
        <li v-for="alert in data.alerts" :key="alert">{{ alert }}</li>
      </ul>
    </article>
  </section>

  <section class="split-grid">
    <article class="card">
      <div class="section-title">
        <h3>再平衡建议</h3>
        <span>偏离 ≥ 5%</span>
      </div>
      <ul class="simple-list">
        <li v-for="item in data.rebalance_suggestions" :key="item.code">
          <span>{{ item.name }}</span>
          <strong>¥{{ Number(item.suggested_amount_cny).toLocaleString() }}</strong>
        </li>
        <li v-if="!data.rebalance_suggestions.length">当前无明显再平衡建议</li>
      </ul>
    </article>

    <article class="card">
      <div class="section-title">
        <h3>回撤阶段</h3>
        <span>{{ data.drawdown_stage }}</span>
      </div>
      <ul class="simple-list">
        <li><span>第一档</span><strong>-15%</strong></li>
        <li><span>第二档</span><strong>-25%</strong></li>
        <li><span>第三档</span><strong>-35%</strong></li>
      </ul>
    </article>
  </section>
</template>
