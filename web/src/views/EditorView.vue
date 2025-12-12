<template>
  <div class="editor-view">
    <input 
      type="file" 
      ref="fileInput" 
      accept=".ply,.splat" 
      style="display: none" 
      @change="handleFileSelect"
    >
    <div class="toolbar">
      <div class="tool-group">
        <button @click="triggerFileInput">
          <span class="icon">📂</span> 打开文件
        </button>
        <button :class="{ active: currentTool === 'view' }" @click="setTool('view')">
          <span class="icon">👁️</span> 浏览
        </button>
        <button :class="{ active: currentTool === 'select' }" @click="setTool('select')">
          <span class="icon">👆</span> 点选物体
        </button>
        <button :class="{ active: currentTool === 'box' }" @click="setTool('box')">
          <span class="icon">⛶</span> 框选区域
        </button>
      </div>
      <div class="action-group" v-if="selectionMade">
        <button class="btn-danger" @click="removeSelection">
          <span class="icon">🗑️</span> 移除物体
        </button>
        <button @click="clearSelection" class="btn-clear">清除选择</button>
      </div>
      <div class="info-group">
        <span class="model-badge">模型: {{ modelName }}</span>
        <span class="dataset-badge" v-if="datasetName">数据集: {{ datasetName }} <span v-if="sceneName">/ {{ sceneName }}</span></span>
      </div>
    </div>

    <div class="viewer-wrapper">
      <template v-if="modelPath">
        <!-- 3D Viewer -->
        <div v-show="currentTool === 'view'" class="full-size">
          <GaussianSplatsViewer 
            :splatScenePath="modelPath" 
            :cameraOptions="cameraConfig"
            :format="modelFormat"
            tool="view"
          />
        </div>
        
        <!-- Image Selector -->
        <div v-if="currentTool !== 'view'" class="full-size">
          <ImageSelector 
            :tool="currentTool"
            :dataset="datasetName"
            :scene="sceneName"
            @selection-complete="handleImageSelection"
          />
        </div>
      </template>
      
      <div v-else class="placeholder">
        <div class="empty-state">
          <span class="empty-icon">🧊</span>
          <p>未加载模型，请点击“打开文件”或前往任务列表查看结果。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import GaussianSplatsViewer from '../components/GaussianSplatsViewer.vue';
import ImageSelector from '../components/ImageSelector.vue';

const route = useRoute();
const modelName = ref('Default');
const modelPath = ref('');
const modelFormat = ref(null);
const currentTool = ref('view');
const selectionMade = ref(false);
const fileInput = ref(null);
const datasetName = ref('');
const sceneName = ref('');

// Default camera config
const cameraConfig = {
  position: { x: 0, y: 1, z: 5 },
  lookAt: { x: 0, y: 0, z: 0 },
  up: { x: 0, y: 1, z: 0 },
  fov: 60
};

onMounted(() => {
  if (route.query.model) {
    modelName.value = route.query.model;
    // Check if it's a demo model or we should leave it empty
    if (route.query.model === 'Garden Demo') {
         modelPath.value = 'https://projects.markkellogg.org/threejs/demo_assets/garden/garden.splat';
         modelFormat.value = 0; 
    } else {
         // For simulated tasks or other models, default to local bonsai ply
         modelPath.value = '/models/scene/bonsai.ply';
         modelFormat.value = 2; 
    }
  } else {
     // Default demo: Bonsai
     modelName.value = 'Bonsai Demo';
     // Vite serves files in public/ at root
     modelPath.value = '/models/scene/bonsai.ply';
     modelFormat.value = 2; // Ply format
  }

  // Retrieve dataset name from route query
  if (route.query.dataset) {
    datasetName.value = route.query.dataset;
  }
  if (route.query.scene) {
    sceneName.value = route.query.scene;
  }
});

onUnmounted(() => {
    // Clean up blob URL if exists
    if (modelPath.value && modelPath.value.startsWith('blob:')) {
        URL.revokeObjectURL(modelPath.value);
    }
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    // Revoke old URL if it was a blob URL
    if (modelPath.value && modelPath.value.startsWith('blob:')) {
      URL.revokeObjectURL(modelPath.value);
    }
    
    const url = URL.createObjectURL(file);
    modelName.value = file.name;
    modelPath.value = url;
    
    // Determine format
    const extension = file.name.split('.').pop().toLowerCase();
    if (extension === 'splat') modelFormat.value = 0; // Splat
    else if (extension === 'ksplat') modelFormat.value = 1; // KSplat
    else if (extension === 'ply') modelFormat.value = 2; // Ply
    else modelFormat.value = null;

    // Reset input
    event.target.value = '';
  }
};

const setTool = (tool) => {
  currentTool.value = tool;
  if (tool === 'view') {
    // When switching back to view, we might want to clear selection mode UI state?
    // But we keep 'selectionMade' if a selection was already confirmed.
  }
};

const handleImageSelection = (result) => {
    console.log('Selection received:', result);
    selectionMade.value = true;
    // Here we would typically send the result to backend (SAM)
    // For now, we just acknowledge it and maybe switch back to view?
    // User might want to stay to select more?
    // Let's switch back to view as "confirmation"
    currentTool.value = 'view';
};

const removeSelection = () => {
  alert('物体已移除！背景修复中...');
  selectionMade.value = false;
  currentTool.value = 'view';
};

const clearSelection = () => {
  selectionMade.value = false;
};
</script>

<style scoped>
.editor-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.toolbar {
  height: 64px;
  background: var(--bg-card);
  backdrop-filter: blur(10px);
  color: var(--text-main);
  display: flex;
  align-items: center;
  padding: 0 24px;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  z-index: 100;
}

.tool-group, .action-group {
  display: flex;
  gap: 8px;
}

.tool-group button, .action-group button {
  background: var(--bg-card-hover);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.tool-group button:hover, .action-group button:hover {
  background: var(--border-color);
}

.tool-group button.active {
  background: rgba(139, 92, 246, 0.2);
  border-color: var(--primary);
  color: var(--primary);
  box-shadow: var(--glow-primary);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.2) !important;
  border-color: var(--danger) !important;
  color: var(--danger) !important;
}

.btn-danger:hover {
  background: rgba(239, 68, 68, 0.3) !important;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
}

.btn-clear {
  background: transparent !important;
  border: 1px solid var(--text-muted) !important;
  color: var(--text-muted) !important;
}

.model-badge, .dataset-badge {
  background: var(--bg-card);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  margin-left: 8px;
}

.viewer-wrapper {
  flex: 1;
  position: relative;
  background: #000;
  overflow: hidden;
}

.full-size {
  width: 100%;
  height: 100%;
}

.placeholder {
  color: var(--text-main);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: radial-gradient(circle at center, var(--bg-card) 0%, var(--bg-app) 100%);
}

.empty-state {
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 16px;
  opacity: 0.5;
}

.selection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  border: 2px dashed rgba(139, 92, 246, 0.6);
  background: rgba(139, 92, 246, 0.05);
  display: flex;
  justify-content: center;
  align-items: center;
}

.instruction {
  background: rgba(28, 33, 40, 0.8);
  color: var(--text-main);
  padding: 8px 16px;
  border-radius: 8px;
  backdrop-filter: blur(4px);
  border: 1px solid var(--border-color);
}
</style>