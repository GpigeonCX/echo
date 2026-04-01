<script setup lang="ts">
const config = useRuntimeConfig()

const { data: assets } = await useFetch(`${config.public.apiBase}/assets`, { default: () => [] })
const { data: transactions, refresh } = await useFetch(`${config.public.apiBase}/transactions`, {
  default: () => []
})

const form = reactive({
  asset_id: 1,
  account_id: 1,
  action: "buy",
  quantity: 0,
  price: 0,
  amount: 0,
  fee: 0,
  applied_date: "2026-04-01",
  confirmed_date: "2026-04-01",
  nav_date: "2026-04-01",
  status: "confirmed",
  note: ""
})

watch(
  () => [form.quantity, form.price],
  () => {
    form.amount = Number(form.quantity) * Number(form.price)
  }
)

async function submitTransaction() {
  await $fetch(`${config.public.apiBase}/transactions`, {
    method: "POST",
    body: form
  })
  form.quantity = 0
  form.price = 0
  form.amount = 0
  form.fee = 0
  form.note = ""
  await refresh()
}
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Transactions</p>
      <h2>交易录入</h2>
    </div>
  </section>

  <section class="split-grid">
    <article class="card">
      <div class="section-title">
        <h3>新增交易</h3>
      </div>
      <form class="form-grid" @submit.prevent="submitTransaction">
        <label>
          标的
          <select v-model="form.asset_id">
            <option v-for="asset in assets" :key="asset.id" :value="asset.id">
              {{ asset.name }}
            </option>
          </select>
        </label>
        <label>
          动作
          <select v-model="form.action">
            <option value="buy">buy</option>
            <option value="sell">sell</option>
            <option value="deposit">deposit</option>
            <option value="withdraw">withdraw</option>
          </select>
        </label>
        <label>
          数量
          <input v-model="form.quantity" type="number" min="0" step="0.0001" />
        </label>
        <label>
          价格
          <input v-model="form.price" type="number" min="0" step="0.0001" />
        </label>
        <label>
          金额
          <input v-model="form.amount" type="number" min="0" step="0.01" />
        </label>
        <label>
          手续费
          <input v-model="form.fee" type="number" min="0" step="0.01" />
        </label>
        <label>
          申请日
          <input v-model="form.applied_date" type="date" />
        </label>
        <label>
          确认日
          <input v-model="form.confirmed_date" type="date" />
        </label>
        <label class="form-full">
          备注
          <input v-model="form.note" type="text" />
        </label>
        <button class="submit-btn" type="submit">提交交易</button>
      </form>
    </article>

    <article class="card">
      <div class="section-title">
        <h3>最近交易</h3>
      </div>
      <ul class="simple-list">
        <li v-for="item in transactions.slice(0, 8)" :key="item.id">
          <span>{{ item.action }} #{{ item.asset_id }}</span>
          <strong>¥{{ Number(item.amount).toLocaleString() }}</strong>
        </li>
      </ul>
    </article>
  </section>
</template>
