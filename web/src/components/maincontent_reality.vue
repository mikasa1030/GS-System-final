<template>
  <div
    class="main-content"
    tabindex="0"
  >
    <h1>{{ title }}</h1>
    <div class="preview-info">

      <!-- 预览窗口 -->
      <div class="preview-section">
        <div class="preview-window">

          <div class="video-container">
            <!-- 使用 <video> 标签播放视频 -->
            <video class="my-video" :key="videoPath" autoplay muted playsinline loop>
              <source
                :src="videoPath + '?t=' + new Date().getTime()"
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



export default {
  name: "MainContent",
  props: {
    videoPath: String, // 接收父组件传递的 videoPath
    title: {
      type: String,
      required: true,
    },
    previewButtons: {
      type: Array,
      required: true,
    },
  },
  components: {
    
  },
  data() {
    return {
      currentView: "3dViewer", // 当前视图状态（默认为 3D Viewer）

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
    // 可选：监控 videoPath 的变化
    videoPath(newPath) {
      console.log("视频路径已更新:", newPath);
      this.$nextTick(() => {
        if (this.$refs.videoPlayer) {
          this.$refs.videoPlayer.load();
        }
      });
    },
  },
  mounted() {
    console.log("Received splatScenes:", this.splatScenes); // 添加调试日志
    console.log("Received cameraOptions:", this.cameraOptions); // 添加调试日志
    console.log("视频路径已更新:", this.videoPath);
  },
};
</script>
    
    <style scoped>
/* video 标签样式 */
video {
  display: flex;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持视频纵横比并裁剪填充容器 */
}

.my-video {
  display: block;         /* 去除默认的 inline 块间隙 */
  width: 100%;           /* 让视频宽度自适应父容器 */
  height: auto;          /* 等比例自动计算高度 */
}
/* 设置视频容器样式 */
.video-container {
  width: 100%;
  height: 100%;
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
  width: 50%;
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
  height: 95%; /* 确保占满父容器的剩余空间 */
  margin-top: 10px;
  box-sizing: border-box;
 
}

/* 预览窗口样式 */
.preview-window {
  display: flex;
  width: 99%;
  height: 100%; /* 确保占满父容器 */

  background-color: #ced0d2;
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
    
        