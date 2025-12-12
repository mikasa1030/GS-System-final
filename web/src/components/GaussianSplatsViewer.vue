<template>
  <div 
    ref="viewerContainer"
    class="viewer-root"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
  >
    <div ref="renderContainer" class="render-container"></div>
    <!-- Selection Box -->
    <div 
        v-if="selectionBox.visible" 
        class="selection-box"
        :style="{
            left: selectionBox.x + 'px',
            top: selectionBox.y + 'px',
            width: selectionBox.width + 'px',
            height: selectionBox.height + 'px'
        }"
    ></div>
    <!-- Info Panel -->
    <div v-if="showInfoPanel" class="info-panel">
      <h3>Debug Info</h3>
      <div class="info-item"><span>Camera Pos:</span> <span>{{ formatVector(infoData.camPos) }}</span></div>
      <div class="info-item"><span>Camera LookAt:</span> <span>{{ formatVector(infoData.camLookAt) }}</span></div>
      <div class="info-item"><span>Camera Up:</span> <span>{{ formatVector(infoData.camUp) }}</span></div>
      <div class="info-item"><span>Cursor Pos:</span> <span>{{ formatVector(infoData.cursorPos) }}</span></div>
      <div class="info-item"><span>FPS:</span> <span>{{ infoData.fps }}</span></div>
      <div class="info-item"><span>Render Size:</span> <span>{{ infoData.renderSize.w }} x {{ infoData.renderSize.h }}</span></div>
      <div class="info-item"><span>Splat Count:</span> <span>{{ infoData.splatCount }}</span></div>
      <div class="info-item"><span>Render Count:</span> <span>{{ infoData.renderCount }}</span></div>
      <div class="info-item"><span>Sort Time:</span> <span>{{ infoData.sortTime }} ms</span></div>
      <div class="info-item"><span>Point Cloud:</span> <span>{{ infoData.pointCloud ? 'ON' : 'OFF' }}</span></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import * as GaussianSplats3D from "@mkkellogg/gaussian-splats-3d";
import * as THREE from "three";

// 定义 props 接收路径
const props = defineProps({
  splatScenePath: {
    type: String,
    required: true,
  },
  cameraOptions: {
    type: Object,
    required: true,
  },
  format: {
    type: Number,
    default: null,
  },
  tool: {
    type: String,
    default: 'view',
  },
});

const emit = defineEmits(['selection-changed']);

const viewerContainer = ref(null);
const renderContainer = ref(null);
let viewer = null; // 存储 viewer 实例
let camera = null; // 存储 camera 实例

// Selection state
const isSelecting = ref(false);
const selectionBox = ref({ x: 0, y: 0, width: 0, height: 0, visible: false });
const startPoint = ref({ x: 0, y: 0 });

const handleMouseDown = (e) => {
  if (props.tool === 'box') {
    isSelecting.value = true;
    const rect = viewerContainer.value.getBoundingClientRect();
    startPoint.value = { 
      x: e.clientX - rect.left, 
      y: e.clientY - rect.top 
    };
    selectionBox.value = {
      x: startPoint.value.x,
      y: startPoint.value.y,
      width: 0,
      height: 0,
      visible: true
    };
  } else if (props.tool === 'select') {
      // Point selection logic could go here
      // For now, we just treat a click as a selection
      emit('selection-changed', true);
  }
};

const handleMouseMove = (e) => {
  if (isSelecting.value && props.tool === 'box') {
    const rect = viewerContainer.value.getBoundingClientRect();
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;
    
    const width = currentX - startPoint.value.x;
    const height = currentY - startPoint.value.y;
    
    selectionBox.value = {
      x: width > 0 ? startPoint.value.x : currentX,
      y: height > 0 ? startPoint.value.y : currentY,
      width: Math.abs(width),
      height: Math.abs(height),
      visible: true
    };
  }
};

const handleMouseUp = () => {
  if (isSelecting.value) {
    isSelecting.value = false;
    if (selectionBox.value.width > 5 || selectionBox.value.height > 5) {
        emit('selection-changed', true);
    } else {
        // Too small, ignore
        selectionBox.value.visible = false;
        emit('selection-changed', false);
    }
  }
};
let renderer = null; // 存储 renderer 实例
let animationId = null;
let lastFrameTime = Date.now();
let frameCount = 0;

// State
const showInfoPanel = ref(true); // Defaults to visible as requested
const infoData = ref({
  camPos: {x:0, y:0, z:0},
  camLookAt: {x:0, y:0, z:0},
  camUp: {x:0, y:0, z:0},
  cursorPos: {x:0, y:0, z:0},
  fps: 0,
  renderSize: {w:0, h:0},
  splatCount: 0,
  renderCount: 0,
  sortTime: 0,
  pointCloud: false,
});

const formatVector = (v) => {
    return `${v.x.toFixed(2)}, ${v.y.toFixed(2)}, ${v.z.toFixed(2)}`;
};

const handleKeyDown = (e) => {
  if (!viewer) return;

  switch (e.code) {
    case 'KeyP':
      if (viewer.splatMesh) {
        const enabled = viewer.splatMesh.getPointCloudModeEnabled();
        viewer.splatMesh.setPointCloudModeEnabled(!enabled);
        infoData.value.pointCloud = !enabled;
      }
      break;
    case 'Equal': // +
      if (viewer.splatMesh) {
        viewer.splatMesh.setSplatScale(viewer.splatMesh.getSplatScale() + 0.05);
      }
      break;
    case 'Minus': // -
      if (viewer.splatMesh) {
        viewer.splatMesh.setSplatScale(viewer.splatMesh.getSplatScale() - 0.05);
      }
      break;
    case 'KeyC':
       // Toggle mesh cursor if needed, usually handled by viewer if not using external camera?
       // But let's assume user might want it. 
       // Viewer doesn't expose setMeshCursorEnabled easily in public API sometimes, but let's check properties.
       // Based on source: this.showMeshCursor = !this.showMeshCursor;
       // We can try setting it if viewer exposes it.
       if (viewer.hasOwnProperty('showMeshCursor')) {
           viewer.showMeshCursor = !viewer.showMeshCursor;
       }
       break;
    case 'KeyU':
       if (viewer.hasOwnProperty('showControlPlane')) {
           viewer.showControlPlane = !viewer.showControlPlane;
       }
       break;
  }
};

const createViewer = () => {
  if (viewer) {
    // 销毁现有 viewer 实例
    if (viewer.splatMesh) viewer.splatMesh.updateTransforms();
    viewer.forceRenderNextFrame();
  }

  const container = renderContainer.value;
  if (!container) return;

  const { clientWidth, clientHeight } = container;

  // 创建 renderer
  renderer = new THREE.WebGLRenderer({ antialias: false });
  renderer.setSize(clientWidth, clientHeight);
  container.innerHTML = ""; // 清空之前的内容
  container.appendChild(renderer.domElement);

  // 创建新的相机
  camera = new THREE.PerspectiveCamera(
    props.cameraOptions.fov,
    clientWidth / clientHeight,
    0.1,
    500
  );

  camera.position.set(
    props.cameraOptions.position.x,
    props.cameraOptions.position.y,
    props.cameraOptions.position.z
  );
  camera.up
    .set(
      props.cameraOptions.up.x,
      props.cameraOptions.up.y,
      props.cameraOptions.up.z
    )
    .normalize();
  camera.lookAt(
    new THREE.Vector3(
      props.cameraOptions.lookAt.x,
      props.cameraOptions.lookAt.y,
      props.cameraOptions.lookAt.z
    )
  );
  const threeScene = new THREE.Scene();
  const boxColor = 0xbbbbbb;
  const boxGeometry = new THREE.BoxGeometry(2, 2, 2);
  const boxMesh = new THREE.Mesh(
    boxGeometry,
    new THREE.MeshBasicMaterial({ color: boxColor })
  );
  boxMesh.position.set(0, 0, 0);

  const axesHelper = new THREE.AxesHelper(3);
  threeScene.add(axesHelper);
  // 创建新的 viewer
  viewer = new GaussianSplats3D.Viewer({
    selfDrivenMode: true,
    renderer,
    camera,
    useBuiltInControls: true,
    threeScene: threeScene,
  });

  updateControlsState();

  // 验证路径
  if (!props.splatScenePath || typeof props.splatScenePath !== "string") {
    console.error("Invalid splatScenePath:", props.splatScenePath);
    return;
  }

  const basePath = "http://127.0.0.1:8000"; // 后端服务的根路径
  const fullPath = props.splatScenePath.startsWith("/media/")
    ? `${basePath}${props.splatScenePath}`
    : props.splatScenePath;

  // 调用 addSplatScene
  const loadOptions = {
    showLoadingUI: true,
    progressiveLoad: true,
    position: [0, 0, -5],
  };
  if (props.format !== null) {
    loadOptions.format = props.format;
  }

  viewer
    .addSplatScene(fullPath, loadOptions)
    .then(() => {
      console.log("Scene loaded successfully!");
      viewer.start();
    })
    .catch((error) => {
      console.error("Error loading scene:", error);
    });
};

const updateDebugInfo = () => {
  if (!viewer || !camera) {
      animationId = requestAnimationFrame(updateDebugInfo);
      return;
  }

  // Update Camera Info
  infoData.value.camPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
  infoData.value.camUp = { x: camera.up.x, y: camera.up.y, z: camera.up.z };
  
  // Calculate LookAt (approximate based on rotation)
  const lookAt = new THREE.Vector3(0, 0, -1);
  lookAt.applyQuaternion(camera.quaternion);
  infoData.value.camLookAt = { x: lookAt.x, y: lookAt.y, z: lookAt.z };

  // Update Performance/Stats
  const now = Date.now();
  frameCount++;
  if (now - lastFrameTime >= 1000) {
    infoData.value.fps = frameCount;
    frameCount = 0;
    lastFrameTime = now;
  }

  if (renderer) {
      const size = new THREE.Vector2();
      renderer.getSize(size);
      infoData.value.renderSize = { w: size.width, h: size.height };
  }

  infoData.value.splatCount = viewer.splatCount || 0;
  infoData.value.renderCount = viewer.splatRenderCount || 0;
  // viewer.sortTime might be available depending on version, often it's lastSortTime
  infoData.value.sortTime = viewer.lastSortTime || 0;

  // Update Point Cloud status
  if (viewer.splatMesh) {
      infoData.value.pointCloud = viewer.splatMesh.getPointCloudModeEnabled();
  }

  animationId = requestAnimationFrame(updateDebugInfo);
};

// Exposed methods
const rotateScene = (axis, angle) => {
    if (viewer && viewer.splatMesh) {
        const rad = THREE.MathUtils.degToRad(angle);
        if (axis === 'x') viewer.splatMesh.rotateX(rad);
        if (axis === 'y') viewer.splatMesh.rotateY(rad);
        if (axis === 'z') viewer.splatMesh.rotateZ(rad);
    }
};

const resetCamera = () => {
    if (camera) {
        camera.position.set(
            props.cameraOptions.position.x,
            props.cameraOptions.position.y,
            props.cameraOptions.position.z
        );
        camera.lookAt(
            new THREE.Vector3(
            props.cameraOptions.lookAt.x,
            props.cameraOptions.lookAt.y,
            props.cameraOptions.lookAt.z
            )
        );
        camera.up.set(
            props.cameraOptions.up.x,
            props.cameraOptions.up.y,
            props.cameraOptions.up.z
        ).normalize();
    }
};

const getViewerInfo = () => {
    if (!viewer) return null;
    return {
        splatCount: viewer.splatCount,
        renderCount: viewer.splatRenderCount
    };
};

defineExpose({
  rotateScene,
  resetCamera,
  getViewerInfo
});

// 在组件挂载时创建 viewer
onMounted(() => {
  createViewer();
  updateDebugInfo();
  window.addEventListener('keydown', handleKeyDown);
  
  // 监听 splatScenePath 的变化并重新加载场景
  watch(
    () => props.splatScenePath,
    async (newPath) => {
      if (viewer.splatMesh && viewer.splatMesh.scenes.length > 0) {
        await viewer.removeSplatScenes([0]); // 正确移除旧场景
      }
      const loadOptions = {
        showLoadingUI: true,
        progressiveLoad: true,
        position: [0, 0, -5],
      };
      if (props.format !== null) {
        loadOptions.format = props.format;
      }
      await viewer.addSplatScene(newPath, loadOptions); // 添加新的场景
    }
  );

  watch(
    () => props.cameraOptions,
    () => {
      createViewer(); // 每次 cameraOptions 更新时重新创建 viewer
    },
    { deep: true } // 深度监听，确保对象内部的变化也会触发
  );

  // Watch for tool changes to enable/disable controls
  watch(
    () => props.tool,
    (newTool) => {
      updateControlsState();
    }
  );
});

const updateControlsState = () => {
  if (viewer && viewer.controls) {
    const shouldEnable = props.tool === 'view';
    viewer.controls.enabled = shouldEnable;
  }
};

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    if (animationId) cancelAnimationFrame(animationId);
    if (viewer) viewer.dispose();
});
</script>


<style scoped>
.viewer-root {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  user-select: none; /* Prevent text selection while dragging */
}

.render-container {
  width: 100%;
  height: 100%;
}

.info-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(28, 33, 40, 0.8);
  color: var(--text-main);
  padding: 10px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  font-family: monospace;
  font-size: 12px;
  pointer-events: none; /* Let clicks pass through */
  z-index: 10;
  backdrop-filter: blur(4px);
}

.info-item {
  margin-bottom: 4px;
}

.selection-box {
  position: absolute;
  border: 2px solid var(--success);
  background-color: rgba(16, 185, 129, 0.2);
  pointer-events: none;
  z-index: 20;
}
</style>
