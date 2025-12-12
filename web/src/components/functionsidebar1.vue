<template>
  <div class="functions">
    <h3>功能</h3>
    <div class="function-container">
      <!-- 头部细化按钮 -->
      <button
        @click="togglePopup('headRefine')"
        class="titlebutton"
      >{{ buttonLabels.headRefine }}</button>
      <div
        v-if="popupType === 'headRefine'"
        class="popup"
      >
        <h4>头部细化</h4>
        <p>上传视频并选择模型进行头部细化</p>
        <div class="popup-buttons">
          <label
            for="file-upload"
            class="upload-button"
          >上传视频</label>
          <input
            type="file"
            id="file-upload"
            accept="video/*"
            style="display: none;"
            @change="handleHeadFile"
          />
          <button>选择模型</button>
        </div>
        <button
          class="train-button"
          @click="startTraining"
        >一键训练</button>
      </div>
    </div>

    <div class="function-container">
      <!-- 风格化按钮 -->
      <button
        @click="togglePopup('stylize')"
        class="titlebutton"
      >{{ buttonLabels.stylize }}</button>
      <div
        v-if="popupType === 'stylize'"
        class="popup"
      >
        <h4>风格化功能</h4>
        <p>上传图片并选择风格进行风格化</p>
        <div class="popup-buttons">
          <button>图片上传</button>
          <button>选择风格</button>
        </div>
        <button
          class="train-button"
          @click="startTraining"
        >一键应用</button>
      </div>
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
            <p>flame转化中</p>
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
            <p>头部细化中</p>
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
export default {
  name: "FunctionsPanel",
  props: {
    buttonLabels: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      lastUploadedFileNames: [],
      popupType: null, // 控制弹出框的类型
      isTraining: false, // 控制训练进度弹窗是否显示
      flameProgress: 0, // 第一个进度条：flame转化的进度
      headRefineProgress: 0, // 第二个进度条：头部细化的进度
      trainingInterval: null, // 用于保存 setInterval 的 ID
      flameInterval: null, // 用于保存第一个进度条的 setInterval
      headRefineInterval: null, // 用于保存第二个进度条的 setInterval
    };
  },
  methods: {
    handleHeadFile(event) {
      const file = event.target.files[0]; // 只获取用户选择的第一个文件
      if (!file) {
        alert("未选择文件");
        return;
      }

      const formData = new FormData();
      formData.append("file", file); // 后端字段改为 "file"，因为只上传一个文件

      fetch("http://127.0.0.1:8000/uploadhead/", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("上传失败");
          }
          return response.json();
        })
        .then((result) => {
          if (result.file_url) {
            alert(`文件上传成功！\n文件名：${file.name}`);
          } else {
            alert(`文件上传成功！`);
          }
        })
        .catch((error) => {
          console.error("上传失败：", error);
          alert("文件上传失败，请稍后重试！");
        });
    },

    togglePopup(type) {
      this.popupType = this.popupType === type ? null : type;
    },

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
          this.finishProcessing();
        }
      }, 100); // 每100ms更新进度1%
    },

    finishProcessing() {
      // 这里写你希望在进度条完成后触发的功能
      console.log("进度条完成，开始执行后续操作...");
      // 你可以添加任何自定义的处理逻辑
      fetch(`http://127.0.0.1:8000/list_uploaded_files/?folder_key=head`)
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
          const newFileNames = result.uploaded_files.map((file) => file.file); // 这里要提取 file 名
          console.log("当前文件名列表：", newFileNames);

          // 找出新增的文件（新列表中存在、但上一次记录中没有的）
          const addedFiles = newFileNames.filter(
            (fileName) => !this.lastUploadedFileNames.includes(fileName)
          );
          console.log("新增文件:", addedFiles);

          if (addedFiles.length > 0) {
            // 获取所有 path 组成的列表
            const pathsList = addedFiles.map((fileName) => {
              const file = result.uploaded_files.find(
                (f) => f.file === fileName
              );
              return file ? file.file_url : ""; // 获取每个新增文件的 URL
            });
            console.log("pathlist:", pathsList);

            // 将 pathsList 传递给父组件
            this.$emit("update-uploaded-paths", pathsList);
          } else {
            console.log("没有新增文件");
          }

          // 更新上一次的文件名列表
          this.lastUploadedFileNames = newFileNames;
          console.log("上一次文件列表:", this.lastUploadedFileNames);
        })
        .catch((error) => console.error("获取文件列表失败:", error));
    },
  },
};
</script>
  
<style scoped>
/* 弹窗样式 */
/* 样式用于创建一个转动的圆圈 */
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

/* 弹窗样式 */
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
.functions {
  display: flex;
  flex-direction: column;
  margin-bottom: 0px;
  border: 1px solid #ede7e7;

  align-items: center;
  height: 18%;
  width: 100%;
  background-color: #f9f9f9;
  border-radius: 5px;
}
.functions h3 {
  font-size: 16px;
  margin-bottom: 5px;
  margin-top: 5px;
}
.function-container {
  position: relative; /* 让弹出框的定位基于当前容器 */
  margin-bottom: 5px;
  width: 95%;
  height: 40px;
}
.titlebutton {
  width: 100%;
  height: 90%;
  background-color: #323941;
  border-radius: 5px;
  color: #fff;
}
/* 弹出框样式 */
.popup {
  position: absolute;
  top: -130px; /* 根据需要调整此值让弹出框与按钮对齐 */
  left: -230px; /* 弹出框在按钮左侧 */
  width: 200px;
  padding: 10px;
  background-color: #f9f9f9;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  z-index: 10;
}

.popup h4 {
  font-size: 14px;
  margin-bottom: 10px;
  text-align: center;
}

.popup p {
  font-size: 12px;
  margin-bottom: 10px;
  text-align: center;
  color: #666;
}

.popup-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.popup-buttons button {
  width: 45%;
  padding: 8px;
  background-color: #ddd;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.popup-buttons button:hover {
  background-color: #ccc;
}
.upload-button {
  width: 45%;
  padding: 5px;
  background-color: #ddd;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  text-align: center;
  display: flex; /* 开启弹性布局 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}
.upload-button:hover {
  background-color: #ccc;
}

.train-button {
  width: 100%;
  padding: 8px;
  background-color: #0078d7;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
}

.train-button:hover {
  background-color: #005a9e;
}
</style>
  