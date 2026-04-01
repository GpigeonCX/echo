<script setup lang="ts">
const config = useRuntimeConfig()
const { data } = await useFetch(`${config.public.apiBase}/assets`, { default: () => [] })
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
          <th>市场</th>
          <th>币种</th>
          <th>目标权重</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.code">
          <td>{{ item.code }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.asset_type }}</td>
          <td>{{ item.market }}</td>
          <td>{{ item.currency }}</td>
          <td>{{ (Number(item.target_weight) * 100).toFixed(2) }}%</td>
        </tr>
      </tbody>
    </table>
  </article>
</template>
