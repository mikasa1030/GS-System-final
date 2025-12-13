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
                <button class="btn-small btn-danger" @click="deleteDataset(dataset)">删除</button>
              </td>
            </tr>
            <tr v-if="dataset.expanded" class="detail-row">
              <td colspan="5">
                <div class="scene-list">
                  <h4>包含场景及目录结构:</h4>
                  <div class="scenes-grid">
                    <div v-for="scene in dataset.scenes" :key="scene" class="scene-item">
                      <div class="scene-name">{{ scene }}</div>
                      <div class="scene-subdirs">
                         <span v-for="subdir in (dataset.sceneDetails && dataset.sceneDetails[scene]) || []" :key="subdir" class="subdir-tag">
                           {{ subdir }}
                         </span>
                         <span v-if="!dataset.sceneDetails || !dataset.sceneDetails[scene] || dataset.sceneDetails[scene].length === 0" class="empty-tag">无子目录</span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal">
        <h2>删除确认</h2>
        <p class="warning-text">
          确定要删除数据集 "{{ datasetToDelete?.name }}" 吗?
          <br>
          此操作将永久删除该数据集及其所有文件，且不可恢复！
        </p>
        <div class="form-group">
          <label>请输入数据集名称 "{{ datasetToDelete?.name }}" 以确认:</label>
          <input 
            v-model="deleteConfirmationInput" 
            type="text" 
            placeholder="输入数据集名称"
            @keyup.enter="confirmDelete"
          />
        </div>
        <div class="modal-actions">
          <button @click="closeDeleteModal" class="btn-secondary">取消</button>
          <button 
            @click="confirmDelete" 
            class="btn-danger-solid"
            :disabled="deleteConfirmationInput !== datasetToDelete?.name"
          >
            确认删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const fileInput = ref(null);
const datasets = ref([]);
const API_BASE = 'http://127.0.0.1:8000/api';

// Delete Modal State
const showDeleteModal = ref(false);
const datasetToDelete = ref(null);
const deleteConfirmationInput = ref('');

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

const deleteDataset = (dataset) => {
  datasetToDelete.value = dataset;
  deleteConfirmationInput.value = '';
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  datasetToDelete.value = null;
  deleteConfirmationInput.value = '';
};

const confirmDelete = async () => {
  if (!datasetToDelete.value) return;
  if (deleteConfirmationInput.value !== datasetToDelete.value.name) return;
  
  const dataset = datasetToDelete.value;
  
  try {
    const res = await fetch(`${API_BASE}/datasets/${dataset.name}/`, {
      method: 'DELETE'
    });
    
    if (res.ok) {
      // Remove from list
      datasets.value = datasets.value.filter(d => d.name !== dataset.name);
      // alert(`数据集 "${dataset.name}" 已成功删除。`); // Optional, maybe just close modal
      closeDeleteModal();
    } else {
      const err = await res.json();
      alert(`删除失败: ${err.error || '未知错误'}`);
    }
  } catch (e) {
    console.error("Error deleting dataset:", e);
    alert('删除请求出错');
  }
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

.scenes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 8px;
}

.scene-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.scene-name {
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 4px;
}

.scene-subdirs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.subdir-tag {
  background: rgba(139, 92, 246, 0.15);
  color: var(--text-main);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.empty-tag {
  color: var(--text-muted);
  font-size: 0.8rem;
  font-style: italic;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-card);
  padding: 32px;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-xl);
}

.modal h2 {
  margin: 0 0 24px 0;
  color: var(--text-main);
}

.warning-text {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
  padding: 16px;
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  margin-bottom: 24px;
  line-height: 1.6;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-main);
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-input);
  color: var(--text-main);
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
}

.btn-danger-solid {
  background: var(--danger);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-danger-solid:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-1px);
}

.btn-danger-solid:disabled {
  background: var(--border-color);
  color: var(--text-dim);
  cursor: not-allowed;
  transform: none;
}

</style>
