<template>
  <div class="home-view">
    <h1 class="page-title">系统概览</h1>
    <div class="stats-container">
      <div class="stat-card">
        <h3>数据集总数</h3>
        <p class="highlight">12</p>
      </div>
      <div class="stat-card">
        <h3>已完成任务</h3>
        <p class="highlight success">8</p>
      </div>
      <div class="stat-card">
        <h3>进行中任务</h3>
        <p class="highlight warning">1</p>
      </div>
    </div>
    
    <div class="recent-activity">
      <h2>最近活动</h2>
      <ul class="activity-list">
        <li class="activity-item">
          <span class="dot success"></span>
          任务 "Scene_01_Rain" 已成功完成。
        </li>
        <li class="activity-item">
          <span class="dot info"></span>
          新数据集 "Campus_Snow" 已上传。
        </li>
        <li class="activity-item">
          <span class="dot warning"></span>
          用户编辑了 "Office_Room" 模型。
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.page-title {
  font-size: 2rem;
  margin-bottom: 32px;
  font-weight: 600;
  background: linear-gradient(90deg, var(--text-main), var(--text-muted));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stats-container {
  display: flex;
  gap: 24px;
  margin-bottom: 48px;
}

.stat-card {
  background: var(--bg-card);
  backdrop-filter: blur(10px);
  padding: 24px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  flex: 1;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  box-shadow: var(--shadow-lg);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  border-color: var(--primary);
}

.stat-card h3 {
  margin: 0;
  color: var(--text-muted);
  font-size: 1rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stat-card p.highlight {
  font-size: 3.5rem;
  margin: 16px 0 0;
  color: var(--text-main);
  font-weight: 700;
  line-height: 1;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}

.stat-card p.highlight.success {
  color: var(--success);
  text-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.stat-card p.highlight.warning {
  color: var(--warning);
  text-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}

.recent-activity {
  background: var(--bg-card);
  padding: 32px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
}

.recent-activity h2 {
  margin-top: 0;
  margin-bottom: 24px;
  color: var(--text-main);
  font-size: 1.5rem;
}

.activity-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-item {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  transition: background 0.2s;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background: var(--bg-card-hover);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 16px;
  display: inline-block;
}

.dot.success { background-color: var(--success); box-shadow: 0 0 8px rgba(16, 185, 129, 0.5); }
.dot.info { background-color: var(--secondary); box-shadow: 0 0 8px rgba(6, 182, 212, 0.5); }
.dot.warning { background-color: var(--warning); box-shadow: 0 0 8px rgba(245, 158, 11, 0.5); }
</style>
