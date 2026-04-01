<script setup lang="ts">
const config = useRuntimeConfig()
const { data } = await useFetch(`${config.public.apiBase}/assets/holdings`, { default: () => [] })
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Holdings</p>
      <h2>持仓列表</h2>
    </div>
  </section>

  <article class="card">
    <table class="table">
      <thead>
        <tr>
          <th>代码</th>
          <th>名称</th>
          <th>类型</th>
          <th>数量</th>
          <th>现价</th>
          <th>成本</th>
          <th>市值(CNY)</th>
          <th>收益(CNY)</th>
          <th>当前权重</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.code">
          <td>{{ item.code }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.asset_type }}</td>
          <td>{{ Number(item.quantity).toLocaleString() }}</td>
          <td>{{ Number(item.current_price).toLocaleString() }}</td>
          <td>{{ Number(item.average_cost).toFixed(4) }}</td>
          <td>¥{{ Number(item.market_value_cny).toLocaleString() }}</td>
          <td>¥{{ Number(item.profit_cny).toLocaleString() }}</td>
          <td>{{ (Number(item.current_weight) * 100).toFixed(2) }}%</td>
        </tr>
      </tbody>
    </table>
  </article>
</template>
