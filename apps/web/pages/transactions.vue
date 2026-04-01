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
        <h3>录入原则</h3>
      </div>
      <ul class="simple-list">
        <li>只录入买入、卖出、转入、转出和现金变动</li>
        <li>基金保留申请日、确认日、确认净值日</li>
        <li>系统后续自动更新持仓、成本、收益和回撤</li>
      </ul>
    </article>
    <article class="card">
      <div class="section-title">
        <h3>下一步接口</h3>
      </div>
      <ul class="simple-list">
        <li>POST /transactions</li>
        <li>GET /transactions</li>
        <li>PATCH /transactions/:id/status</li>
      </ul>
    </article>
  </section>
</template>
