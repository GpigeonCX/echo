<script setup lang="ts">
const config = useRuntimeConfig()
const { data, refresh } = await useFetch(`${config.public.apiBase}/assets/holdings`, { default: () => [] })

const form = reactive({
  code: "",
  name: "",
  asset_type: "fund",
  market: "CN_FUND",
  currency: "CNY",
  target_weight: 0,
  quantity: 0,
  average_cost: 0,
  current_price: 0,
  fx_rate_to_cny: 1,
  account_id: 1
})

async function submitHolding() {
  await $fetch(`${config.public.apiBase}/assets/manual-holdings`, {
    method: "POST",
    body: form
  })
  Object.assign(form, {
    code: "",
    name: "",
    asset_type: "fund",
    market: "CN_FUND",
    currency: "CNY",
    target_weight: 0,
    quantity: 0,
    average_cost: 0,
    current_price: 0,
    fx_rate_to_cny: 1,
    account_id: 1
  })
  await refresh()
}
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Holdings</p>
      <h2>持仓列表</h2>
    </div>
  </section>

  <section class="split-grid">
    <article class="card">
      <div class="section-title">
        <h3>手工录入持仓</h3>
      </div>
      <form class="form-grid" @submit.prevent="submitHolding">
        <label>
          代码
          <input v-model="form.code" type="text" />
        </label>
        <label>
          名称
          <input v-model="form.name" type="text" />
        </label>
        <label>
          类型
          <select v-model="form.asset_type">
            <option value="fund">fund</option>
            <option value="hk_stock">hk_stock</option>
            <option value="cash">cash</option>
            <option value="money_fund">money_fund</option>
          </select>
        </label>
        <label>
          市场
          <input v-model="form.market" type="text" />
        </label>
        <label>
          数量
          <input v-model="form.quantity" type="number" min="0" step="0.0001" />
        </label>
        <label>
          成本
          <input v-model="form.average_cost" type="number" min="0" step="0.0001" />
        </label>
        <label>
          现价
          <input v-model="form.current_price" type="number" min="0" step="0.0001" />
        </label>
        <label>
          目标权重
          <input v-model="form.target_weight" type="number" min="0" step="0.0001" />
        </label>
        <button class="submit-btn" type="submit">保存持仓</button>
      </form>
    </article>

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
  </section>
</template>
