<template>
  <div class="layout-shell">
    <header class="layout-header">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">LS</span>
        <span class="brand-text">
          <strong>个性化学习系统</strong>
          <small>Learner Dashboard</small>
        </span>
      </RouterLink>

      <nav class="nav-links">
        <RouterLink class="nav-link" to="/">仪表盘</RouterLink>
        <RouterLink class="nav-link" to="/knowledge-graph">知识图谱</RouterLink>
        <RouterLink class="nav-link" to="/login">登录</RouterLink>
        <RouterLink class="nav-link nav-link--accent" to="/register">注册</RouterLink>
      </nav>
    </header>

    <main class="layout-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.layout-shell {
  width: min(1280px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 40px;
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 22px;
  margin-bottom: 24px;
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.76);
  backdrop-filter: blur(14px);
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  display: grid;
  width: 46px;
  height: 46px;
  place-items: center;
  border-radius: 14px;
  color: #fff;
  font-weight: 700;
  letter-spacing: 0.08em;
  background: linear-gradient(135deg, #2563eb, #0f766e);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-text strong {
  font-size: 16px;
}

.brand-text small {
  color: #64748b;
  font-size: 12px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-link {
  padding: 10px 16px;
  border-radius: 999px;
  color: #334155;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.24);
}

.nav-link.router-link-active {
  color: #0f172a;
  border-color: rgba(37, 99, 235, 0.3);
  background: rgba(219, 234, 254, 0.9);
}

.nav-link--accent {
  color: #fff;
  border-color: transparent;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

.layout-main {
  min-height: calc(100vh - 144px);
}

@media (max-width: 768px) {
  .layout-shell {
    width: min(100% - 20px, 1280px);
    padding-top: 12px;
  }

  .layout-header {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-links {
    flex-wrap: wrap;
  }

  .nav-link {
    flex: 1 1 calc(50% - 10px);
    text-align: center;
  }
}
</style>
