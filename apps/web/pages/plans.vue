<script setup lang="ts">
const config = useRuntimeConfig()
const { data, refresh } = await useFetch(`${config.public.apiBase}/plans`, { default: () => [] })

const editing = reactive({
  id: 0,
  name: "",
  total_budget: 0,
  months: 6,
  first_month_ratio: 0.4,
  status: "in_progress"
})

watch(
  data,
  (plans) => {
    if (!plans?.length) return
    const plan = plans[0]
    Object.assign(editing, plan)
  },
  { immediate: true }
)

async function savePlan() {
  await $fetch(`${config.public.apiBase}/plans/${editing.id}`, {
    method: "PUT",
    body: editing
  })
  await refresh()
}
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">Plans</p>
      <h2>进场计划</h2>
    </div>
  </section>

  <section class="split-grid">
    <article class="card">
      <div class="section-title">
        <h3>编辑计划</h3>
      </div>
      <form class="form-grid" @submit.prevent="savePlan">
        <label class="form-full">
          计划名称
          <input v-model="editing.name" type="text" />
        </label>
        <label>
          总预算
          <input v-model="editing.total_budget" type="number" min="1" step="0.01" />
        </label>
        <label>
          分批月数
          <input v-model="editing.months" type="number" min="1" step="1" />
        </label>
        <label>
          首月比例
          <input v-model="editing.first_month_ratio" type="number" min="0" max="1" step="0.01" />
        </label>
        <label>
          状态
          <select v-model="editing.status">
            <option value="draft">draft</option>
            <option value="in_progress">in_progress</option>
            <option value="completed">completed</option>
            <option value="paused">paused</option>
          </select>
        </label>
        <button class="submit-btn" type="submit">保存计划</button>
      </form>
    </article>

    <article v-for="plan in data" :key="plan.id" class="card">
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
