<template>
  <div class="image-selector">
    <!-- Gallery View -->
    <div v-if="!selectedImage" class="gallery-view">
      <div class="gallery-header">
        <h3>数据集图片 ({{ images.length }})</h3>
        <p class="hint" v-if="dataset">当前: {{ dataset }} <span v-if="scene">/ {{ scene }}</span></p>
        <p class="hint">请选择一张图片进行标注</p>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-if="error" class="error-msg">{{ error }}</div>
      </div>
      
      <div class="image-grid" v-if="!loading && !error">
        <div 
          v-for="(img, index) in images" 
          :key="index" 
          class="image-card"
          @click="selectImage(img)"
        >
          <div class="image-wrapper">
            <img :src="img.url" :alt="img.name" loading="lazy" />
            <div class="overlay">
              <span>点击标注</span>
            </div>
          </div>
          <div class="image-info">{{ img.name }}</div>
        </div>
      </div>
    </div>

    <!-- Annotation View -->
    <div v-else class="annotation-view">
      <div class="annotation-toolbar">
        <button class="btn-back" @click="closeImage">
          <span class="icon">←</span> 返回图库
        </button>
        <div class="tool-info">
          <span class="current-mode">
            当前模式: {{ tool === 'box' ? '框选区域' : '点选物体' }}
          </span>
          <span class="instruction">
            {{ tool === 'box' ? '按住鼠标左键拖拽框选物体' : '点击图片中的物体添加提示点' }}
          </span>
        </div>
        <div class="actions">
          <button class="btn-confirm" @click="confirmSelection">
            <span class="icon">✓</span> 完成标注
          </button>
        </div>
      </div>

      <div class="canvas-wrapper">
        <div 
          class="canvas-container" 
          ref="containerRef"
          @mousedown="handleMouseDown"
          @mousemove="handleMouseMove"
          @mouseup="handleMouseUp"
          @mouseleave="handleMouseUp"
        >
          <img 
            ref="imageRef" 
            :src="selectedImage.url" 
            class="target-image" 
            draggable="false"
          />
          
          <!-- Render Points -->
          <div 
            v-for="(pt, idx) in points" 
            :key="`pt-${idx}`" 
            class="point-marker"
            :style="{ left: pt.x + 'px', top: pt.y + 'px' }"
          ></div>

          <!-- Render Box -->
          <div 
            v-if="box.visible" 
            class="box-overlay"
            :style="{
              left: Math.min(box.startX, box.currentX) + 'px',
              top: Math.min(box.startY, box.currentY) + 'px',
              width: Math.abs(box.currentX - box.startX) + 'px',
              height: Math.abs(box.currentY - box.startY) + 'px'
            }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';

const props = defineProps({
  tool: {
    type: String,
    default: 'view'
  },
  dataset: {
    type: String,
    default: ''
  },
  scene: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['selection-complete']);

const images = ref([]);
const loading = ref(false);
const error = ref(null);
const API_BASE = 'http://127.0.0.1:8000/api';

const loadImages = async () => {
  loading.value = true;
  error.value = null;
  if (props.dataset && props.scene) {
    try {
      const res = await fetch(`${API_BASE}/datasets/images/?dataset=${props.dataset}&scene=${props.scene}`);
      if (res.ok) {
        images.value = await res.json();
        if (images.value.length === 0) {
           error.value = `在数据集 ${props.dataset}/${props.scene} 中未找到图片。`;
        }
      } else {
        console.error("Failed to load images from backend");
        error.value = "无法从后端加载图片。";
        images.value = [];
      }
    } catch (e) {
      console.error("Error loading images:", e);
      error.value = `加载出错: ${e.message}`;
      images.value = [];
    }
  } else {
    // Default demo image
    images.value = [{ name: 'bonsai.JPG', url: '/bonsai.JPG' }];
  }
  loading.value = false;
};

onMounted(() => {
  loadImages();
});

watch(() => [props.dataset, props.scene], () => {
  loadImages();
  selectedImage.value = null; // Reset selection on dataset change
});

const selectedImage = ref(null);
const containerRef = ref(null);
const points = ref([]);
const box = reactive({
  startX: 0,
  startY: 0,
  currentX: 0,
  currentY: 0,
  visible: false,
  isDrawing: false
});

const selectImage = (img) => {
  selectedImage.value = img;
  // Reset annotations
  points.value = [];
  box.visible = false;
  box.isDrawing = false;
};

const closeImage = () => {
  selectedImage.value = null;
};

const handleMouseDown = (e) => {
  if (!selectedImage.value) return;
  const rect = containerRef.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  if (props.tool === 'select') {
    // Add point
    points.value.push({ x, y });
  } else if (props.tool === 'box') {
    // Start box
    box.startX = x;
    box.startY = y;
    box.currentX = x;
    box.currentY = y;
    box.visible = true;
    box.isDrawing = true;
    // Clear previous box if singular selection desired? 
    // For now let's assume one box per session or reset on new draw
  }
};

const handleMouseMove = (e) => {
  if (props.tool === 'box' && box.isDrawing) {
    const rect = containerRef.value.getBoundingClientRect();
    box.currentX = e.clientX - rect.left;
    box.currentY = e.clientY - rect.top;
  }
};

const handleMouseUp = () => {
  if (props.tool === 'box' && box.isDrawing) {
    box.isDrawing = false;
  }
};

const confirmSelection = () => {
  // Calculate relative coordinates (0-1)
  if (!containerRef.value) return;
  const width = containerRef.value.clientWidth;
  const height = containerRef.value.clientHeight;

  const result = {
    dataset: props.dataset,
    image: selectedImage.value,
    width,
    height,
    points: points.value.map(p => ({ x: p.x / width, y: p.y / height })),
    box: box.visible ? {
      x: Math.min(box.startX, box.currentX) / width,
      y: Math.min(box.startY, box.currentY) / height,
      w: Math.abs(box.currentX - box.startX) / width,
      h: Math.abs(box.currentY - box.startY) / height
    } : null
  };

  emit('selection-complete', result);
  alert('标注已提交！(模拟后端调用SAM)');
  closeImage();
};
</script>

<style scoped>
.image-selector {
  width: 100%;
  height: 100%;
  background: var(--bg-app);
  color: var(--text-main);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.gallery-view {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.gallery-header {
  margin-bottom: 20px;
}

.gallery-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-main);
}

.hint {
  color: var(--text-muted);
  margin-top: 5px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.image-card {
  background: var(--bg-card);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
  border: 1px solid var(--border-color);
}

.image-card:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
  box-shadow: var(--shadow-lg);
}

.image-wrapper {
  position: relative;
  padding-top: 75%; /* 4:3 aspect ratio */
  overflow: hidden;
}

.image-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.image-card:hover .overlay {
  opacity: 1;
}

.loading {
  color: var(--primary);
  margin: 10px 0;
}

.error-msg {
  color: var(--danger);
  margin: 10px 0;
}

.image-info {
  padding: 10px;
  font-size: 0.9rem;
  color: var(--text-muted);
  text-align: center;
  background: var(--bg-card);
  border-top: 1px solid var(--border-color);
}

/* Annotation View */
.annotation-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.annotation-toolbar {
  height: 60px;
  padding: 0 20px;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
}

.btn-back, .btn-confirm {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-back {
  background: var(--bg-card-hover);
  color: var(--text-main);
  border: 1px solid var(--border-color);
}

.btn-back:hover {
  background: var(--border-color);
}

.btn-confirm {
  background: var(--primary-gradient);
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-confirm:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.tool-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.current-mode {
  font-weight: 600;
  color: var(--primary);
}

.instruction {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.canvas-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #050505;
  overflow: auto;
  padding: 20px;
}

.canvas-container {
  position: relative;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  cursor: crosshair;
}

.target-image {
  display: block;
  max-width: 100%;
  max-height: 80vh;
  user-select: none;
}

.point-marker {
  position: absolute;
  width: 12px;
  height: 12px;
  background: var(--danger);
  border: 2px solid white;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.box-overlay {
  position: absolute;
  border: 2px solid var(--success);
  background: rgba(16, 185, 129, 0.2);
  pointer-events: none;
}
</style>