<template>
  <div class="task-view">
    <div class="header">
      <h1 class="page-title">重建任务</h1>
      <button class="btn-primary" @click="showCreateModal = true">
        <span class="icon">+</span> 新建任务
      </button>
    </div>

    <!-- Task List -->
    <div class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-card">
        <div class="task-info">
          <h3>{{ task.name }}</h3>
          <span :class="['status', getStatusClass(task.status)]">{{ task.statusDisplay }}</span>
          <div class="meta-info">
            <p><span class="label">模式:</span> {{ task.modeDisplay }}</p>
            <p><span class="label">数据集:</span> {{ task.dataset }} / {{ task.scene }}</p>
          </div>
        </div>
        <div class="task-actions">
          <button v-if="task.status === 'completed'" @click="viewResult(task)" class="btn-outline">查看模型</button>
          <button v-if="task.status === 'completed'" @click="exportModel(task)" class="btn-outline">导出</button>
          <button v-if="task.status === 'processing'" class="btn-outline disabled" disabled>处理中...</button>
          <!-- Handle other statuses if needed, e.g. pending/failed -->
          <button v-if="task.status === 'pending'" class="btn-outline disabled" disabled>等待中...</button>
          <button v-if="task.status === 'failed'" class="btn-outline failed" disabled>失败</button>
          <button @click="deleteTask(task)" class="btn-outline danger">删除</button>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateModal" class="modal-overlay">
      <div class="modal">
        <h2>新建重建任务</h2>
        <div class="form-group">
          <label>任务名称</label>
          <input v-model="newTask.name" type="text" placeholder="输入任务名称" />
        </div>
        <div class="form-group">
          <label>选择数据集</label>
          <select v-model="newTask.dataset">
            <option v-for="ds in datasetOptions" :key="ds" :value="ds">{{ ds }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>选择场景</label>
          <select v-model="newTask.scene">
            <option v-for="scene in availableScenes" :key="scene" :value="scene">{{ scene }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>重建模式</label>
          <div class="radio-group">
            <label class="radio-item">
              <input type="radio" value="normal" v-model="newTask.mode" />
              <span class="radio-text">常规 / 稀疏重建 <small>(一致性引导)</small></span>
            </label>
            <label class="radio-item">
              <input type="radio" value="derain" v-model="newTask.mode" />
              <span class="radio-text">去雨模式 <small>(不透明度约束)</small></span>
            </label>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="showCreateModal = false" class="btn-secondary">取消</button>
          <button @click="createTask" class="btn-primary">开始重建</button>
        </div>
      </div>
    </div>

    <!-- Delete Task Modal -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal" style="max-width: 400px;">
        <h2>删除任务</h2>
        <p style="color: var(--text-muted); margin-bottom: 24px;">
          确定要删除任务 "{{ taskToDelete?.name }}" 吗? 此操作无法撤销。
        </p>
        <div class="modal-actions">
          <button @click="closeDeleteModal" class="btn-secondary">取消</button>
          <button @click="confirmDelete" class="btn-primary" style="background: var(--danger); border-color: var(--danger);">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const showCreateModal = ref(false);
const showDeleteModal = ref(false);
const taskToDelete = ref(null);
const tasks = ref([]);
const datasets = ref([]);
const API_BASE = 'http://127.0.0.1:8000/api';

const newTask = ref({
  name: '',
  dataset: '',
  scene: '',
  mode: 'normal'
});

const fetchDatasets = async () => {
  try {
    const res = await fetch(`${API_BASE}/datasets/`);
    if (res.ok) {
      datasets.value = await res.json();
      // Set default dataset if available
      if (datasets.value.length > 0 && !newTask.value.dataset) {
        newTask.value.dataset = datasets.value[0].name;
      }
    }
  } catch (e) {
    console.error("Error fetching datasets", e);
  }
};

const fetchTasks = async () => {
  try {
    const res = await fetch(`${API_BASE}/tasks/`);
    if (res.ok) {
      const data = await res.json();
      // Map backend status/mode to frontend display
      tasks.value = data.map(t => ({
        ...t,
        statusDisplay: mapStatus(t.status),
        modeDisplay: mapMode(t.mode)
      }));
    }
  } catch (e) {
    console.error("Error fetching tasks", e);
  }
};

const mapStatus = (status) => {
  const map = { 'pending': '等待中', 'processing': '进行中', 'completed': '已完成', 'failed': '失败' };
  return map[status] || status;
};

const mapMode = (mode) => {
  const map = { 'normal': '常规', 'derain': '去雨' };
  return map[mode] || mode;
};

onMounted(() => {
  fetchDatasets();
  fetchTasks();
});

const datasetOptions = computed(() => datasets.value.map(d => d.name));

// Available scenes based on selected dataset
const availableScenes = computed(() => {
  const ds = datasets.value.find(d => d.name === newTask.value.dataset);
  return ds ? ds.scenes : [];
});

// Watch for dataset changes to reset scene
watch(() => newTask.value.dataset, (newVal) => {
  const ds = datasets.value.find(d => d.name === newVal);
  if (ds && ds.scenes.length > 0) {
    newTask.value.scene = ds.scenes[0];
  } else {
    newTask.value.scene = '';
  }
}, { immediate: true });

const getStatusClass = (status) => {
  return status === 'completed' ? 'completed' : 'running';
};

const createTask = async () => {
  try {
    const payload = {
      name: newTask.value.name || `Task_${tasks.value.length + 1}`,
      dataset: newTask.value.dataset,
      scene: newTask.value.scene,
      mode: newTask.value.mode,
      status: 'processing'
    };

    const res = await fetch(`${API_BASE}/tasks/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const createdTask = await res.json();
      showCreateModal.value = false;
      fetchTasks(); // Refresh list
      
      // Simulate completion after 5 seconds
      setTimeout(async () => {
        await fetch(`${API_BASE}/tasks/${createdTask.id}/complete/`, { method: 'POST' });
        fetchTasks();
      }, 5000);
    }
  } catch (e) {
    console.error("Error creating task", e);
  }
};

const exportModel = async (task) => {
  try {
    const res = await fetch(`${API_BASE}/tasks/${task.id}/export/`);
    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${task.name}_model.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } else {
        const err = await res.json();
        alert(`导出失败: ${err.error || '模型文件不存在'}`);
    }
  } catch (e) {
    console.error("Export error", e);
    alert('导出出错');
  }
};

const deleteTask = (task) => {
  taskToDelete.value = task;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  taskToDelete.value = null;
};

const confirmDelete = async () => {
  if (!taskToDelete.value) return;
  
  const task = taskToDelete.value;
  
  try {
    const res = await fetch(`${API_BASE}/tasks/${task.id}/`, {
      method: 'DELETE'
    });

    if (res.ok) {
      // Remove from list
      tasks.value = tasks.value.filter(t => t.id !== task.id);
      closeDeleteModal();
    } else {
      alert('删除失败');
    }
  } catch (e) {
    console.error("Error deleting task", e);
    alert('删除出错');
  }
};

const viewResult = (task) => {
  router.push({ 
    path: '/editor', 
    query: { 
      model: task.name, // In a real app, this might be a path or ID
      dataset: task.dataset,
      scene: task.scene
    } 
  });
};
</script>

<style scoped>
.task-view {
  position: relative;
}

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

.task-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.task-card {
  background: var(--bg-card);
  padding: 24px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s, box-shadow 0.3s;
}

.task-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.task-info h3 {
  margin: 0 0 16px 0;
  color: var(--text-main);
  font-size: 1.2rem;
}

.meta-info p {
  margin: 8px 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.meta-info .label {
  color: var(--text-dim);
  margin-right: 8px;
}

.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 16px;
  text-transform: uppercase;
}

.status.completed {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
  border: 1px solid rgba(16, 185, 129, 0.2);
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
}

.status.running {
  background: rgba(139, 92, 246, 0.1);
  color: var(--primary);
  border: 1px solid rgba(139, 92, 246, 0.2);
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.1);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.6; }
  100% { opacity: 1; }
}

/* Removed local .btn-primary to use global from base.css */

.task-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn-outline {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(139, 92, 246, 0.5);
  color: var(--primary);
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  font-size: 0.9rem;
  height: 40px;
}

.btn-outline:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: var(--primary);
  color: var(--text-main);
  transform: translateY(-1px);
}

.btn-outline.disabled {
  border-color: var(--border-color);
  color: var(--text-muted);
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-outline.disabled:hover {
  background: transparent;
  color: var(--text-muted);
  transform: none;
}

.btn-outline.failed {
  border-color: var(--danger);
  color: var(--danger);
}

.btn-outline.danger {
  border-color: var(--danger);
  color: var(--danger);
  margin-left: 0;
}

/* Modal Styles */
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
  width: 500px;
  max-width: 90%;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-lg);
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 24px;
  color: var(--text-main);
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-muted);
}

.form-group input[type="text"],
.form-group select {
  width: 100%;
  padding: 12px;
  background: var(--bg-app);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-main);
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-item {
  display: flex;
  align-items: center;
  background: var(--bg-app);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
}

.radio-item:hover {
  border-color: #475569;
}

.radio-item input {
  margin-right: 12px;
}

.radio-text {
  color: #e2e8f0;
}

.radio-text small {
  color: #94a3b8;
  margin-left: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}

.btn-secondary {
  background: transparent;
  color: #94a3b8;
  border: 1px solid #475569;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #cbd5e1;
  color: #f8fafc;
}
</style>
