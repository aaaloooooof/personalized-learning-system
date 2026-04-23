<template>
  <section class="not-found">
    <h1>404</h1>
    <p>页面不存在，返回仪表盘继续浏览。</p>
    <RouterLink class="back-link" to="/">回到仪表盘</RouterLink>
  </section>
</template>

<style scoped>
.not-found {
  display: grid;
  place-items: center;
  gap: 12px;
  min-height: 60vh;
  text-align: center;
  padding: 32px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(148, 163, 184, 0.24);
}

.not-found h1 {
  margin: 0;
  font-size: 64px;
}

.back-link {
  padding: 12px 18px;
  border-radius: 999px;
  color: #fff;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}
</style>
