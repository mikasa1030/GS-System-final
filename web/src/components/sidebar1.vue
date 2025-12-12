<template>
  <div class="container">
    <!-- 侧边栏按钮 -->
    <div class="sidebar-button">
      <button
        v-if="!hideButtons.includes('模型')"
        class="menu-button model-button"
        @click="setActiveContent('模型')"
      >模型</button>
      <button
        v-if="!hideButtons.includes('人体模型')"
        class="menu-button model-button"
        @click="setActiveContent('人体模型')"
      >人体模型</button>
      <button
        v-if="!hideButtons.includes('场景模型')"
        class="menu-button model-button"
        @click="setActiveContent('场景模型')"
      >场景模型</button>
      <button
        v-if="!hideButtons.includes('驱动')"
        class="menu-button drive-button"
        @click="setActiveContent('驱动')"
      >驱动</button>
      <button
        v-if="!hideButtons.includes('光照')"
        class="menu-button lighting-button"
        @click="setActiveContent('光照')"
      >光照</button>
    </div>

    <!-- 动态显示的内容区域 -->
    <div class="content">
      <!-- 内容容器 -->
      <div
        v-if="activeContent === '模型'"
        class="model-content-container"
      >
        <!-- 顶部按钮栏 -->

        <!-- 资产内容 -->
        <div class="asset-content">
          <div class="sidebar">
            <div
              class="category"
              v-for="category in modelCategories"
              :key="category.title"
            >
              <div class="model-uptitle">
                <h2>{{ category.title }}</h2>
              </div>
              <div class="model-buttons">
                <button
                  v-for="button in category.buttons"
                  :key="button.name"
                  class="button"
                  @click="handleButtonClick(button)"
                  :style="{ backgroundImage: 'url(' + button.imageUrl + ')',width:'60px',height:'60px'}"
                >
                  {{ button.name }}
                </button>
                <!-- 上传按钮 -->
                <label
                  for="uploadPlyFile"
                  class="button upload-button"
                >
                  <!-- 隐藏实际的文件输入框 -->
                  <input
                    id="uploadPlyFile"
                    type="file"
                    accept=".ply"
                    style="display: none"
                    @change="handlePlyUpload(category)"
                  />
                  <span class="plus-icon">+</span> <!-- 中间的 "+" 号 -->
                </label>
              </div>
            </div>
          </div>
        </div>
        <!-- 重建内容 -->
        <div class="extra-functions">
          <div class="restruct-uptitle">
            <h2>{{ "重建功能" }}</h2>
          </div>
          <p style="font-size: 13px;text-align: center;margin-top: 0px;margin-bottom: 10px;">一段视频重建你的三维数字场景！</p>
          <div
            class="drag-drop-area"
            @dragover.prevent
            @drop.prevent="handleImageDrop"
            @click="triggerFileInput"
          >
            <div class="icon-container">
              <span class="icon">🖼</span>
              <p>上传图片或者视频</p>
            </div>
            <!-- 隐藏文件输入框 -->
            <input
              type="file"
              ref="fileInput"
              accept="image/*,video/*"
              style="display: none;"
              @change="handleImageUpload"
            />
          </div>

          <button
            class="train-button"
            @click="startTraining"
          >一键训练</button>

        </div>

      </div>

      <div
        v-if="activeContent === '驱动'"
        class="content-container"
      >

        <!-- 表情内容 -->
        <div class="asset-content">
          <div class="drivesidebar">
            <div
              class="category"
              v-for="category in faceCategories"
              :key="category.title"
            >
              <div class="model-uptitle">
                <h2>{{ category.title }}</h2>
              </div>
              <div class="model-buttons">
                <button
                  v-for="button in category.buttons"
                  :key="button.name"
                  class="button"
                  @click="handleButtonClick(button)"
                  :style="{color:'black',width:'60px',height:'50px'}"
                >
                  {{ button.name }}
                </button>
              </div>
            </div>
            <div class="audio-upload">

              <Audio @trigger-parent-method="handleAudioUpload"></Audio>

            </div>
            <button
              class="driven-button"
              @click="handleTrainClick"
            >一键驱动</button>
          </div>

        </div>
        <!-- 肢体内容 -->

        <div class="extra-drive-functions">
          <div class="image-preview">
            <h2>动作预览</h2>
            <video
              controls
              autoplay
              muted
              loop
              class="preview-image"
            >
              <source
                src="/动作.mp4"
                type="video/mp4"
              />
            </video>
          </div>
        </div>

      </div>

      <div
        v-if="activeContent === '光照'"
        class="model-content-container"
      >
        <div class="asset-content">
          <div class="sidebar">
            <div
              class="category"
              v-for="category in lightingCategories"
              :key="category.title"
            >
              <div class="model-uptitle">
                <h2>{{ category.title }}</h2>
              </div>
              <div class="model-buttons">
                <button
                  v-for="button in category.buttons"
                  :key="button.name"
                  class="button"
                  :style="{ backgroundImage: 'url(' + button.imageUrl + ')',width:'60px',height:'60px',color:'black'}"
                >
                  {{ button.name }}
                </button>
                <!-- 上传按钮 -->
                <label
                  for="uploadFile"
                  class="button upload-button"
                >
                  <input
                    id="uploadFile"
                    type="file"
                    accept=".hdr, .exr"
                    style="display: none"
                    @change="handlelightUpload"
                  />
                  <span class="plus-icon">+</span>
                </label>
              </div>
            </div>
            <button
              class="relight-button"
              @click="handleTrainClick"
            >重光照</button>
          </div>
        </div>
        <div class="extra-functions">
          <div class="preview-sidebar">
            <div class="restruct-uptitle">
              <h2>{{ "光照预览" }}</h2>
            </div>
            <UploadPreviewComponent
              ref="previewComponent"
              :storedTexture="storedTexture"
              @update-texture="handleTextureUpdate"
            />
          </div>
        </div>
      </div>

      <!-- <functions1 :buttonLabels="functionButtonLabels" /> -->

    </div>

    <!-- 训练进度弹窗 -->
    <div
      v-if="isTraining"
      class="training-popup"
    >
      <div class="popup-content">
        <h4>训练进行中...</h4>
        <div class="progress-container">
          <div class="progress-item">
            <p>colmap估计相机位姿中</p>
            <div class="circle-progress">
              <div
                v-if="flameProgress < 100"
                class="circle"
                :style="{ animationDuration: '2s' }"
              ></div>
              <div
                v-else
                class="circle completed"
              >
                <span>✔️</span>
              </div>
            </div>
          </div>
          <div class="progress-item">
            <p>场景重建中</p>
            <div class="circle-progress">
              <!-- 第二个圆圈的旋转在第一个圆圈完成后才开始 -->
              <div
                v-if="headRefineProgress < 100"
                :class="['circle', { 'start-animation': isFlameCompleted }]"
                :style="{ animationDuration: '2s' }"
              ></div>
              <div
                v-else
                class="circle completed"
              >
                <span>✔️</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
  
<script>
import UploadPreviewComponent from "./uploadlight.vue";
import functions1 from "./functionsidebar.vue";
import Audio from "./audio.vue";
import axios from "axios";

export default {
  props: {
    floderkey: {
      type: String,
      required: true,
    },
    hideButtons: {
      type: Array,
      default: () => [], // 默认不隐藏任何按钮
    },
    modelCategories: {
      type: Array,
      required: true,
    },
    faceCategories: {
      type: Array,
      required: true,
    },
    bodyCategories: {
      type: Array,
      required: true,
    },
    driveCategories: {
      type: Array,
      required: true,
    },
    lightingCategories: {
      type: Array,
      required: true,
    },
    hideButtons: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      activeContent: "模型", // 当前激活的内容
      storedTexture: null, // 存储上传的纹理数据
      uploadedButtons: [],
      lastUploadedFileNames: [],
      audioPreviewUrl: "/audio.wav", // 音频预览 URL
      functionButtonLabels: {
        headRefine: "物体编辑", // 头部细化按钮名称
        stylize: "风格化", // 风格化按钮名称
      },
      popupType: null, // 控制弹出框的类型
      isTraining: false, // 控制训练进度弹窗是否显示
      flameProgress: 0, // 第一个进度条：flame转化的进度
      headRefineProgress: 0, // 第二个进度条：头部细化的进度
      trainingInterval: null, // 用于保存 setInterval 的 ID
      flameInterval: null, // 用于保存第一个进度条的 setInterval
      headRefineInterval: null, // 用于保存第二个进度条的 setInterval
    };
  },
  components: {
    UploadPreviewComponent,
    functions1,
    Audio,
  },
  methods: {
    startTraining() {
      this.isTraining = true;
      this.flameProgress = 0;
      this.headRefineProgress = 0;

      // 启动第一个进度条（flame转化）
      this.flameInterval = setInterval(() => {
        if (this.flameProgress < 100) {
          this.flameProgress += 1;
        } else {
          clearInterval(this.flameInterval); // 第一个进度条完成后清除
          this.startHeadRefineProgress(); // 启动第二个进度条
        }
      }, 100); // 每100ms更新进度1%
    },

    startHeadRefineProgress() {
      // 启动第二个进度条（头部细化）
      this.headRefineInterval = setInterval(() => {
        if (this.headRefineProgress < 100) {
          this.headRefineProgress += 1;
        } else {
          clearInterval(this.headRefineInterval); // 完成后清除 interval
          this.isTraining = false; // 关闭弹窗
          alert("训练完成！");
          this.checkForNewFiles();
        }
      }, 100); // 每100ms更新进度1%
    },
    checkForNewFiles() {
      const folderKey = this.floderkey; // 获取 props 传递的 floderkey
      fetch(
        `http://127.0.0.1:8000/list_uploaded_files/?folder_key=${folderKey}`
      )
        .then((response) => response.json())
        .then((result) => {
          if (!result.uploaded_files) {
            console.error("无法获取上传文件列表");
            return;
          }
          // 更新当前按钮列表（仅作参考，也可以不更新）
          this.uploadedButtons = result.uploaded_files.map((file) => ({
            name: file.file.replace(".ply", ""),
            imageUrl: "/default.png",
            path: file.file_url,
            cameraOptions: {
              fov: 75,
              position: { x: 0, y: -5, z: -10 },
              up: { x: 0, y: -1, z: 0 },
              lookAt: { x: 0, y: 0, z: 0 },
            },
          }));
          console.log("当前上传按钮列表：", this.uploadedButtons);

          // 获取当前文件名列表
          const newFileNames = result.uploaded_files.map((file) => file.file);

          // 找出新增的文件（新列表中存在、但上一次记录中没有的）
          const addedFiles = newFileNames.filter(
            (fileName) => !this.lastUploadedFileNames.includes(fileName)
          );

          if (addedFiles.length > 0) {
            result.uploaded_files.forEach((file) => {
              if (addedFiles.includes(file.file)) {
                const newButton = {
                  name: file.file.replace(".ply", ""),
                  imageUrl: "/default.png",
                  path: file.file_url,
                  cameraOptions: {
                    fov: 75,
                    position: { x: 0, y: -5, z: -10 },
                    up: { x: 0, y: -1, z: 0 },
                    lookAt: { x: 0, y: 0, z: 0 },
                  },
                };

                // 这里直接通知父组件新增按钮
                this.$emit("add-button", {
                  categoryTitle: "数字资产", // 或者使用 this.category.title（确保 category 定义）
                  button: newButton,
                });
              }
            });
          } else {
            console.log("没有新增文件");
          }

          // 更新上一次的文件名列表
          this.lastUploadedFileNames = newFileNames;
        })
        .catch((error) => console.error("获取文件列表失败:", error));
    },

    handleAudioUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.audioPreviewUrl = URL.createObjectURL(file); // 生成音频预览 URL
        this.uploadFiles([file]);
      }
    },
    setActiveContent(name) {
      this.activeContent = name; // 更新当前显示的内容
      if (name === "模型") {
        this.activeModelTab = "重建"; // 默认切换到资产子页面
      }
      if (name === "驱动") {
        this.activeModelTab = "动作"; // 默认切换到资产子页面
      }
    },
    setActiveModelTab(tabName) {
      this.activeModelTab = tabName; // 切换重建和资产
    },
    handlelightUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // 使用 ref 调用子组件的 uploadFile 方法
        this.$refs.previewComponent.uploadFile(file);
        this.uploadFiles([file]);
      }
    },
    handleTextureUpdate(texture) {
      this.storedTexture = texture; // 更新存储的纹理数据
    },
    handlePlyUpload(category) {
      const fileInput = event.target;
      const file = fileInput.files[0];

      if (file) {
        const formData = new FormData();
        formData.append("files", file);

        fetch("http://127.0.0.1:8000/upload/", {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("上传失败");
            }
            return response.json(); // 后端返回 JSON
          })
          .then((result) => {
            console.log("上传成功：", result);

            // 创建新的按钮
            const newButtonName = file.name.replace(".ply", ""); // 按钮名称取文件名
            const uploadedFile = result.uploaded_files[0];
            const newButton = {
              name: newButtonName,
              imageUrl: "/default.png", // 默认背景图片路径
              path: uploadedFile.file_url, // 使用后端返回的 URL
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            };

            // 通知父组件新增按钮
            this.$emit("add-button", {
              categoryTitle: category.title,
              button: newButton,
            });

            // 清空文件输入框值（为了支持重复上传同一文件）
            fileInput.value = "";
          })
          .catch((error) => {
            console.error("上传失败：", error);
            alert("文件上传失败，请稍后重试！");
          });
      }
    },

    handleButtonClick(button) {
      console.log(`Button clicked: ${button.name}`);
      this.$emit("update-splat-scene", {
        path: button.path,
        cameraOptions: button.cameraOptions || null,
      });
    },

    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadFiles(file);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleImageDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        alert(`Dropped ${files.length} file(s)`); // 显示文件数量
        // 调用 uploadFiles 函数，传入所有拖拽过来的文件
        this.uploadFiles(files);
      }
    },

    handleButtonClick(button) {
      // 向父组件触发事件，并传递路径
      console.log("Emitting path:", button.path); // 添加调试日志
      // this.$emit("update-splat-scene", path);
      this.$emit("update-splat-scene", {
        path: button.path,
        cameraOptions: button.cameraOptions || null, // 确保兼容没有 cameraOptions 的按钮
      });
    },
    // uploadFile(file) {
    //   const formData = new FormData();
    //   formData.append("file", file);

    //   fetch("http://127.0.0.1:8000/upload/", {
    //     method: "POST",
    //     body: formData,
    //   })
    //     .then((response) => {
    //       if (!response.ok) {
    //         throw new Error("上传失败");
    //       }
    //       return response.json(); // 假设后端返回 JSON
    //     })
    //     .then((result) => {
    //       console.log("上传成功：", result);
    //       alert("文件上传成功！存储路径：" + result.url);
    //     })
    //     .catch((error) => {
    //       console.error("上传失败：", error);
    //       alert("文件上传失败，请稍后重试！");
    //     });
    // },
    uploadFiles(files) {
      const formData = new FormData();

      // 将所有选中的文件添加到 formData 中
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]); // 'files' 是字段名称，可以与后端一致
      }

      fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("上传失败");
          }
          return response.json(); // 假设后端返回 JSON
        })
        .then((result) => {
          console.log("上传成功：", result);

          // 计算上传成功和失败的文件
          let successCount = 0;
          let errorCount = 0;
          let successFiles = [];
          let errorFiles = [];

          result.uploaded_files.forEach((fileInfo) => {
            if (fileInfo.file_url) {
              successCount++;
              successFiles.push(fileInfo.file);
            } else {
              errorCount++;
              errorFiles.push(fileInfo.file);
            }
          });

          // 构建上传结果提示
          let message = `文件上传完成！\n成功上传：${successCount} 个文件`;
          if (errorCount > 0) {
            message += `\n失败上传：${errorCount} 个文件`;
            message += `\n失败的文件：\n` + errorFiles.join("\n");
          } else {
            message += "\n所有文件上传成功！";
          }

          alert(message); // 统一提示上传结果
        })
        .catch((error) => {
          console.error("上传失败：", error);
          alert("文件上传失败，请稍后重试！");
        });
    },
  },
  // mounted() {
  //   this.fetchUploadedFiles();
  //   setInterval(this.fetchUploadedFiles, 5000); // 每 5 秒刷新一次
  // },
};
</script>
  

<style scoped>
.circle-progress {
  position: relative;
  width: 50px;
  height: 50px;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 5px solid #ccc;
  border-top-color: #4caf50;
  animation: spin 2s linear infinite; /* 添加旋转动画 */
  transition: all 0.5s ease;
}

.start-animation {
  animation: spin 2s linear infinite; /* 在第二个圆圈开始时添加旋转动画 */
}

.completed {
  border-color: #4caf50;
  animation: none;
  background-color: #4caf50;
  display: flex;
  justify-content: center;
  align-items: center;
}

.completed span {
  color: white;
  font-size: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.training-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background-color: white;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
  width: 300px;
}

.progress-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.progress-item {
  text-align: center;
}

progress {
  width: 100%;
  height: 20px;
  margin: 10px 0;
}
/* 总容器样式 */
.container {
  display: flex;
  height: 100vh;
  /* 确保主容器占满整个屏幕 */
  width: 20%;
  justify-content: flex-start;
}

/* 侧边栏按钮样式 */
.sidebar-button {
  top: 0;
  left: 0;
  width: 15%;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

/* 按钮样式 */
.menu-button {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  writing-mode: vertical-rl;
  text-orientation: upright;
}

.model-button {
  background-color: rgb(165, 171, 178);
}

.drive-button {
  background-color: rgb(78, 79, 80);
}

.lighting-button {
  background-color: rgb(117, 117, 117);
}

.human-button {
  background-color: #e91e63;
}

/* 鼠标悬停效果 */
.menu-button:hover {
  opacity: 0.8;
}

/* 内容区域样式 */
.content {
  width: 85%;
  flex-direction: column;
  margin-left: 0px;
  /* 修改为与侧边栏宽度一致 */

  flex: 1;
  display: flex;
  background-color: #dbdada;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
}

/* 动态内容容器 */
.content-container {
  width: 90%;
  height: 100%;
  /* 高度等于整个视口高度 */
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  justify-content: flex-start;
  /* 水平方向居中 */
  align-items: center;
  /* 垂直方向居中 */
  background-color: #ffffff;
  overflow-y: auto;
  /* 如果内容超出高度，允许滚动 */
  padding: 7px;

  margin-bottom: 5%;
  margin-top: 3%;
  border-radius: 5px;
}

.model-content-container {
  width: 90%;
  height: 100%;
  /* 高度等于整个视口高度 */
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  justify-content: flex-start;
  /* 水平方向居中 */
  align-items: center;
  /* 垂直方向居中 */
  background-color: #f9f9f9;
  overflow-y: auto;
  /* 如果内容超出高度，允许滚动 */
  padding: 7px;

  margin-bottom: 5%;
  margin-top: 3%;
  border-radius: 5px;
}

.extra-functions {
  height: 40%;
  width: 98%;
  margin-top: 15px;
  margin-bottom: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: 1px solid lightgray; /* 边框颜色设置为浅灰色 */
  border-radius: 5px; /* 圆角边框 */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  background-color: white; /* 可选：背景色为白色，增强视觉效果 */
}

.extra-drive-functions {
  height: 30%;
  width: 98%;
  margin-top: 15px;
  margin-bottom: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: 1px solid lightgray; /* 边框颜色设置为浅灰色 */
  border-radius: 5px; /* 圆角边框 */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  background-color: white; /* 可选：背景色为白色，增强视觉效果 */
}
.asset-content {
  height: 85%;
  width: 98%;
  margin-top: 10px;
  border: 1px solid lightgray; /* 边框颜色设置为浅灰色 */
  border-radius: 5px; /* 圆角边框 */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  background-color: white; /* 可选：背景色为白色，增强视觉效果 */
}

/* sidebar 样式 */
.sidebar {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: space-between;
}
.drivesidebar {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: space-between;
}
.preview-sidebar {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  align-items: center;
}
.category {
  display: flex;
  flex-direction: column;
  width: 100%;

  margin-bottom: 20px;
  justify-content: center;
  align-items: center;
}

.model-uptitle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  height: 20%;
  width: 85%;
  border-radius: 12px;
  margin-top: 10px;
}
.model-uptitle h2 {
  font-size: 16px;
}

.restruct-uptitle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0px;
  height: 10%;
  width: 85%;
  border-radius: 12px;
  margin-top: 10px;
}
.restruct-uptitle h2 {
  font-size: 16px;
}

.model-buttons {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: start;
}
.model-buttons button {
  display: inline-block; /* 设置为块级元素 */
  background-size: cover;
  background-position: center;
  border: none;
  cursor: pointer;
  text-align: center;
  color: white;
  font-size: 14px;
  position: relative;
}

.model-buttons button::after {
  content: attr(data-name); /* 显示按钮的名字 */
  position: absolute;
  bottom: 5px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 14px;
  color: white;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* 让文本更容易阅读 */
}

.upload-button {
  width: 60px;
  height: 60px;
  background-color: #d3d3d3; /* 浅灰色背景 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  cursor: pointer; /* 鼠标手型 */
  border-radius: 10px; /* 圆角 */
  border: none; /* 去除默认边框 */
  font-size: 16px;
}

.upload-button:hover {
  background-color: #c0c0c0; /* 鼠标悬停时的颜色 */
}

.plus-icon {
  font-size: 30px; /* "+" 号大小 */
  color: #555; /* "+" 号颜色 */
  font-weight: bold;
}

.category button {
  padding: 10px;
  margin: 5px;
  width: 40%;
  height: 40px;
  background-color: #fdfdfd;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  cursor: pointer;
}

.category button:hover {
  background-color: #f0f0f0;
  border-color: #bbb;
}

/* 额外功能区域样式 */
.driven-button {
  margin-top: 5px;
  /* 按钮与上方内容的间距 */
  margin-bottom: 5px;

  width: 60%;
  /* 按钮宽度填满容器 */
  padding: 10px;
  /* 按钮内边距 */
  font-size: 14px;
  /* 按钮文字大小 */
  font-weight: bold;
  /* 加粗文字 */
  color: rgb(235, 233, 233);
  /* 按钮文字颜色 */
  background-color: #3b3d3f;
  /* 按钮背景色 */
  border: none;
  /* 移除边框 */
  border-radius: 8px;
  /* 圆角 */
  cursor: pointer;
  /* 鼠标悬停时变成手型 */
  transition: background-color 0.3s ease;
  /* 动态效果 */
}

.driven-button:hover {
  background-color: #005a9e;
  /* 悬停时的按钮背景色 */
}
.relight-button {
  margin-top: 20px;
  /* 按钮与上方内容的间距 */
  margin-bottom: 15px;

  width: 60%;
  /* 按钮宽度填满容器 */
  padding: 10px;
  /* 按钮内边距 */
  font-size: 14px;
  /* 按钮文字大小 */
  font-weight: bold;
  /* 加粗文字 */
  color: rgb(235, 233, 233);
  /* 按钮文字颜色 */
  background-color: #3b3d3f;
  /* 按钮背景色 */
  border: none;
  /* 移除边框 */
  border-radius: 8px;
  /* 圆角 */
  cursor: pointer;
  /* 鼠标悬停时变成手型 */
  transition: background-color 0.3s ease;
  /* 动态效果 */
}

.relight-button:hover {
  background-color: #005a9e;
  /* 悬停时的按钮背景色 */
}
.train-button {
  margin-top: 10px;
  /* 按钮与上方内容的间距 */
  margin-bottom: 15px;

  width: 60%;
  /* 按钮宽度填满容器 */
  padding: 10px;
  /* 按钮内边距 */
  font-size: 14px;
  /* 按钮文字大小 */
  font-weight: bold;
  /* 加粗文字 */
  color: white;
  /* 按钮文字颜色 */
  background-color: #3b3d3f;
  /* 按钮背景色 */
  border: none;
  /* 移除边框 */
  border-radius: 8px;
  /* 圆角 */
  cursor: pointer;
  /* 鼠标悬停时变成手型 */
  transition: background-color 0.3s ease;
  /* 动态效果 */
}

.train-button:hover {
  background-color: #005a9e;
  /* 悬停时的按钮背景色 */
}
/* 拖拽区域样式 */
.drag-drop-area {
  width: 70%;
  aspect-ratio: 1 / 1; /* 宽高比为 1:1，确保正方形 */
  background-color: #2b3a4a;
  border: 2px dashed #fff;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.drag-drop-area:hover {
  background-color: #3c4d5e;
}

.icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #fff;
}

.icon {
  font-size: 30px;
}

.icon-container p {
  margin-top: 5px;
  font-size: 14px;
}

.audio-upload {
  display: flex;
  flex-direction: column;
  width: 93%;
  height: 40%;
  align-items: center;
  justify-content: start;
  margin-top: 0px;

  border: 1px solid lightgray; /* 边框颜色设置为浅灰色 */
  border-radius: 5px; /* 圆角边框 */
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  background-color: white; /* 可选：背景色为白色，增强视觉效果 */
}

audio {
  width: 100%; /* 音频控件占满父容器宽度 */
  height: 65%;
  max-width: 300px; /* 限制最大宽度 */
}

.image-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 95%;
  height: 90%;
  gap: 10px;

  overflow: hidden;
  /* 隐藏超出范围的内容 */
}

.image-preview video {
  width: 100%;
  /* 匹配父容器宽度 */
  height: 100%;
  /* 匹配父容器高度 */
  object-fit: cover;
  /* 确保视频缩放时保持比例 */
}

.image-preview h2 {
  font-size: 16px;
  margin: 0;
}

.preview-image {
  width: 98%;
  height: 100%;
  object-fit: cover;
  /* 确保图片充满窗口而不变形 */
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
  /* 防止溢出 */
}

/* 顶部按钮栏样式 */
</style>
  