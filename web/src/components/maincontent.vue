<template>
  <div class="main-content" tabindex="0">
    <h1>{{ title }}</h1>
    <div class="preview-info">
      <!-- 删除了按钮切换部分 -->
      <div class="preview-section">
        <div class="preview-window">
          <!-- 只保留需要展示的内容 -->
          <div>
            <GaussianSplatsViewer :splatScenePath="splatScenes" :cameraOptions="cameraOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GaussianSplatsViewer from './GaussianSplatsViewer.vue';

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
      type: String,
      required: true,
    },
    cameraOptions: {
      type: Object,
      required: true, // 让这个属性成为必需
    },
  },
  components: {
    GaussianSplatsViewer,
  },
};
</script>



<style scoped>
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
  height: 100%; /* 确保占满父容器的剩余空间 */
  margin-top: 10px;
  box-sizing: border-box;
}

/* 预览窗口样式 */
.preview-window {
  display: flex;
  width: 99%;
  height: 95%; /* 确保占满父容器 */
  
  background-color: #fdfdfd;
  overflow: hidden; /* 防止内容溢出 */
}

/* 预览窗口的子元素样式 */
.preview-window > * {
  width: 100%;
  height: 100%;
  display: block; /* 确保以块级元素形式展示 */
}

.preview-window  video {
  width: 100%;
  height: 100%;
  display: block; /* 确保以块级元素形式展示 */
}

/* 时间轴样式 */
.timeline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.timeline-slider {
  width: 90%;
}
</style>

    