<template>
  <aside class="sidebar">
    <div class="logo">
      <h2>3D 场景重建与编辑系统</h2>
    </div>
    <nav>
      <router-link to="/" class="nav-item" active-class="active">
        <span class="icon">📊</span> 系统概览
      </router-link>
      <router-link to="/data" class="nav-item" active-class="active">
        <span class="icon">📂</span> 数据管理
      </router-link>
      <router-link to="/tasks" class="nav-item" active-class="active">
        <span class="icon">🚀</span> 重建任务
      </router-link>
      <router-link to="/editor" class="nav-item" active-class="active">
        <span class="icon">🎨</span> 场景编辑
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: var(--bg-sidebar);
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  padding: 24px;
  box-sizing: border-box;
  border-right: 1px solid var(--border-color);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.logo {
  margin-bottom: 48px;
  text-align: center;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
}

.logo h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(90deg, var(--secondary), var(--primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-transform: uppercase;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  color: var(--text-muted);
  text-decoration: none;
  margin-bottom: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  border: 1px solid transparent;
}

.nav-item .icon {
  margin-right: 12px;
  font-size: 1.1rem;
}

.nav-item:hover {
  background-color: var(--bg-card-hover);
  color: var(--text-main);
  transform: translateX(4px);
}

.nav-item.active {
  background: rgba(139, 92, 246, 0.1); /* Primary with opacity */
  color: var(--primary);
  border: 1px solid rgba(139, 92, 246, 0.2);
  box-shadow: 0 0 15px rgba(139, 92, 246, 0.1);
}
</style>
