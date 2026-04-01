<script setup lang="ts">
const config = useRuntimeConfig()

const { data: assets, refresh: refreshAssets } = await useFetch(`${config.public.apiBase}/assets`, {
  default: () => []
})
const { data: transactions, refresh } = await useFetch(`${config.public.apiBase}/transactions`, {
  default: () => []
})

const form = reactive({
  use_existing_asset: true,
  asset_id: 1,
  asset_code: "",
  asset_name: "",
  asset_type: "fund",
  market: "CN_FUND",
  currency: "CNY",
  target_weight: 0,
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
  const payload = { ...form }
  if (form.use_existing_asset) {
    payload.asset_code = null
    payload.asset_name = null
    payload.asset_type = null
    payload.market = null
  } else {
    payload.asset_id = null
  }

  await $fetch(`${config.public.apiBase}/transactions`, {
    method: "POST",
    body: payload
  })

  Object.assign(form, {
    use_existing_asset: true,
    asset_id: assets.value[0]?.id || 1,
    asset_code: "",
    asset_name: "",
    asset_type: "fund",
    market: "CN_FUND",
    currency: "CNY",
    target_weight: 0,
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
  await Promise.all([refresh(), refreshAssets()])
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
        <label class="form-full">
          录入方式
          <select v-model="form.use_existing_asset">
            <option :value="true">选择已有标的</option>
            <option :value="false">按代码新增标的</option>
          </select>
        </label>

        <label v-if="form.use_existing_asset">
          标的
          <select v-model="form.asset_id">
            <option v-for="asset in assets" :key="asset.id" :value="asset.id">
              {{ asset.code }} - {{ asset.name }}
            </option>
          </select>
        </label>

        <template v-else>
          <label>
            代码
            <input v-model="form.asset_code" type="text" />
          </label>
          <label>
            名称
            <input v-model="form.asset_name" type="text" />
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
        </template>

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
