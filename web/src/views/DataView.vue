<template>
  <div class="data-view">
    <div class="header">
      <h1 class="page-title">数据管理</h1>
      <button class="btn-primary" @click="triggerUpload">
        <span class="icon">+</span> 上传数据集
      </button>
      <input type="file" ref="fileInput" style="display: none" multiple @change="handleUpload" />
    </div>

    <div class="dataset-list">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>场景数量</th>
            <th>上传日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="dataset in datasets" :key="dataset.id">
            <tr>
              <td class="id-col">#{{ dataset.id }}</td>
              <td class="name-col">{{ dataset.name }}</td>
              <td>{{ dataset.sceneCount }}</td>
              <td>{{ dataset.date }}</td>
              <td>
                <button class="btn-small btn-view" @click="toggleExpand(dataset)">
                  {{ dataset.expanded ? '收起' : '查看' }}
                </button>
                <button class="btn-small btn-danger">删除</button>
              </td>
            </tr>
            <tr v-if="dataset.expanded" class="detail-row">
              <td colspan="5">
                <div class="scene-list">
                  <h4>包含场景:</h4>
                  <div class="tags">
                    <span v-for="scene in dataset.scenes" :key="scene" class="scene-tag">{{ scene }}</span>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const fileInput = ref(null);
const datasets = ref([]);
const API_BASE = 'http://127.0.0.1:8000/api';

const fetchDatasets = async () => {
  try {
    const res = await fetch(`${API_BASE}/datasets/`);
    if (res.ok) {
      const data = await res.json();
      datasets.value = data.map(d => ({
        ...d,
        expanded: false
      }));
    } else {
      console.error('Failed to fetch datasets');
    }
  } catch (error) {
    console.error('Error fetching datasets:', error);
  }
};

onMounted(() => {
  fetchDatasets();
});

const toggleExpand = (dataset) => {
  dataset.expanded = !dataset.expanded;
};

const triggerUpload = () => {
  fileInput.value.click();
};

const handleUpload = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    // Mock upload logic
    alert(`上传功能尚未连接到后端。`);
  }
};
</script>

<style scoped>
/* Existing styles... */
.page-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-main);
  margin: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

/* Removed local .btn-primary to use global from base.css */

.dataset-list {
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  color: var(--text-muted);
}

th {
  background: var(--bg-sidebar);
  padding: 16px 24px;
  text-align: left;
  font-weight: 600;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border-color);
}

td {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-main);
}

tr:last-child td {
  border-bottom: none;
}

tbody > tr:not(.detail-row):hover {
  background: var(--bg-card-hover);
}

.detail-row {
  background: rgba(0, 0, 0, 0.2);
}

.scene-list {
  padding: 8px 0;
}

.scene-list h4 {
  margin: 0 0 8px 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.scene-tag {
  background: rgba(139, 92, 246, 0.1);
  color: var(--primary);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.id-col {
  color: var(--text-muted);
  font-family: monospace;
}

.name-col {
  color: var(--text-main);
  font-weight: 500;
}

.btn-small {
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
  border: 1px solid transparent;
  margin-right: 8px;
}

.btn-view {
  background: rgba(6, 182, 212, 0.1);
  color: var(--secondary);
  border-color: rgba(6, 182, 212, 0.2);
}

.btn-view:hover {
  background: rgba(6, 182, 212, 0.2);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
  border-color: rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
  background: rgba(239, 68, 68, 0.2);
}

</style>
