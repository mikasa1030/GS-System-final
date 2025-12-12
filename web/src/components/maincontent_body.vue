<template>
  <div
    class="main-content"
    tabindex="0"
  >
    <h1>{{ title }}</h1>
    <div class="preview-info">
      <!-- 按钮切换 -->
      <div class="button-group">
        <button
          @click="currentView = '3dViewer'"
          :class="{ active: currentView === '3dViewer' }"
        >3D Viewer</button>
        <button
          @click="currentView = 'video'"
          :class="{ active: currentView === 'video' }"
        >Video</button>
      </div>

      <!-- 预览窗口 -->
      <div class="preview-section">
        <div class="preview-window">
          <!-- 条件渲染 -->
          <div v-if="currentView === '3dViewer'">
            <GaussianSplatsViewer
              :splatScenePath="splatScenes[currentSceneIndex]"
              :cameraOptions="cameraOptions"
            />
            <!-- 进度条 -->
            <div class="progress-bar">
              <div
                v-for="(scene, index) in splatScenes"
                :key="index"
                class="progress-step"
                :class="{ active: index === currentSceneIndex }"
                @click="updateScene(index)"
              >
                {{ index + 1 }}
              </div>
            </div>
          </div>
          <div
            v-else-if="currentView === 'video'"
            class="video-container"
          >
            <!-- 使用 <video> 标签播放视频 -->
            <video controls>
              <source
                :src="videoPath"
                type="video/mp4"
              />
              您的浏览器不支持 HTML5 视频。
            </video>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
import ThreeScene from "./ThreeViewer.vue";
import GaussianSplatsViewer from "./GaussianSplatsViewer.vue";
import ViewerComponent from "./ViewerComponent.vue";

export default {
  name: "MainContent",
  props: {
    title: {
      type: String,
      required: true,
    },
    previewButtons: {
      type: Array,
      required: true,
    },
    splatScenes: {
      type: Array, // 改为 Array 类型来存储多个 splatScenes
      required: true,
    },
    cameraOptions: {
      type: Object,
      required: true, // 让这个属性成为必需
    },
  },
  components: {
    ThreeScene,
    GaussianSplatsViewer,
    ViewerComponent,
  },
  data() {
    return {
      currentView: "3dViewer", // 当前视图状态（默认为 3D Viewer）
      videoPath: "/women.mp4", // 视频路径，替换为实际路径
      currentSceneIndex: 0, // 当前展示的 splatScene 索引
    };
  },
  methods: {
    // 更新当前的 splatScene
    updateScene(index) {
      this.currentSceneIndex = index;
    },
  },
  watch: {
    cameraOptions: {
      handler(newVal) {
        console.log("cameraOptions updated in MainContent:", newVal);
      },
      immediate: true,
      deep: true,
    },
  },
  mounted() {
    console.log("Received splatScenes:", this.splatScenes); // 添加调试日志
    console.log("Received cameraOptions:", this.cameraOptions); // 添加调试日志
  },
};
</script>
  
  <style scoped>
.progress-bar {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  background-color: #e0e0e0; /* 进度条背景色 */
  padding: 5px;
  height: 10px; /* 更窄的高度 */
  align-items: center;
}

.progress-step {
  width: 15px; /* 圆点的宽度 */
  height: 15px; /* 圆点的高度 */
  background-color: lightgray; /* 默认的圆点颜色 */
  border-radius: 50%; /* 圆形 */
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 11px;
  text-align: center;
}

.progress-step.active {
  background-color: rgb(20, 20, 30); /* 激活时的圆点颜色 */
  color: white;
}

/* 按钮组样式 */
.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px; /* 按钮组和下方内容的间距 */
  justify-content: space-between;
}

.button-group button {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  background-color: #ebe7e7;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.button-group button.active {
  background-color: #525354;
  color: #fff;
}

/* video 标签样式 */
video {
  display: flex;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持视频纵横比并裁剪填充容器 */
}

/* 设置视频容器样式 */
.video-container {
  width: 100%;
  height: 80%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* 设置视频自适应 */
.video-container video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 保持视频比例 */
}

/* 主容器样式 */
.main-content {
  display: flex;
  flex-direction: column;
  width: 63%;
  height: 98%;
  padding: 20px;
  background-color: #ced0d2;
  border: 1px solid #ebf1ea;
  box-sizing: border-box; /* 确保内边距不影响宽度 */
}

/* 标题样式 */
.main-content h1 {
  text-align: center;
}

/* 预览信息区域 */
.preview-info {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: calc(100% - 60px); /* 动态减去按钮组的高度 */
  box-sizing: border-box;
}

/* 预览区域 */
.preview-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  height: 90%; /* 确保占满父容器的剩余空间 */
  margin-top: 10px;
  box-sizing: border-box;
}

/* 预览窗口样式 */
.preview-window {
  display: flex;
  width: 99%;
  height: 95%; /* 确保占满父容器 */

  background-color: #fdfdfd;
  overflow: visible; /* 防止内容溢出 */
}

/* 预览窗口的子元素样式 */
.preview-window > * {
  width: 100%;
  height: 100%;
  display: block; /* 确保以块级元素形式展示 */
}

.preview-window video {
  width: 100%;
  height: 100%;
  display: block; /* 确保以块级元素形式展示 */
}

</style>
  
      