<template>
  <div class="functions">
    <h3>相机参数设置</h3>
    <div class="function-container">
      <!-- 相机 up 参数 -->
      <label for="camera-up">相机朝向:</label>
      <input id="camera-up" type="text" v-model="cameraParameters.up" @input="updateCameraOptions"
        placeholder="0, 1, 0" />
    </div>

    <div class="function-container">
      <!-- 相机 position 参数 -->
      <label for="camera-position">相机位置:</label>
      <input id="camera-position" type="text" v-model="cameraParameters.position" @input="updateCameraOptions"
        placeholder="0, 1, 0" />
    </div>

    <div class="function-container">
      <!-- 相机 look-at 参数 -->
      <label for="camera-look-at">相机观察点:</label>
      <input id="camera-look-at" type="text" v-model="cameraParameters.lookAt" @input="updateCameraOptions"
        placeholder="1, 0, 0" />
    </div>

    <div class="toggle-group">
      <!-- 使用单选按钮实现互斥 -->
      <label class="switch">
        <span>轨迹1</span>
        <input type="radio" name="trajectory" value="param1" v-model="selectedTrajectory" />
        <span class="slider"></span>
      </label>
      <label class="switch">
        <span>轨迹2</span>
        <input type="radio" name="trajectory" value="param2" v-model="selectedTrajectory" />
        <span class="slider"></span>
      </label>
      <label class="switch">
        <span>轨迹3</span>
        <input type="radio" name="trajectory" value="param3" v-model="selectedTrajectory" />
        <span class="slider"></span>
      </label>
    </div>

    <div class="preview-window">
      <!-- 动态绑定图片 -->
      <img :src="previewImage" alt="预览图片" />
    </div>

    <label class="slider-row">
      <span>焦距</span>
      <input type="range" v-model="settings.slider3" min="0" max="100" />
      <span class="value">{{ settings.slider3 }}</span>
    </label>
  </div>
</template>

<script>
export default {
  name: "FunctionsPanel",
  props: {
    initialCameraOptions: {
      type: Object,
      default: () => ({
        up: { x: 0, y: -1, z: 0 },
        position: { x: 0, y: 0, z: -2 },
        lookAt: { x: 0, y: 0, z: 0 },
      }),
    },
  },
  data() {
    return {
      // 初始化 cameraParameters，确保它的结构和模板中的绑定一致
      cameraParameters: {
        up: `${this.initialCameraOptions.up.x}, ${this.initialCameraOptions.up.y}, ${this.initialCameraOptions.up.z}`,
        position: `${this.initialCameraOptions.position.x}, ${this.initialCameraOptions.position.y}, ${this.initialCameraOptions.position.z}`,
        lookAt: `${this.initialCameraOptions.lookAt.x}, ${this.initialCameraOptions.lookAt.y}, ${this.initialCameraOptions.lookAt.z}`,
      },

      settings: {
        slider1: 50,
        slider2: 50,
        slider3: 50,
      },

      // 用于互斥的轨迹选择
      selectedTrajectory: "param1", // 当前选中的轨迹，默认轨迹1

      // 新增预览图片的路径
      previewImage: "/轨迹1.png", // 默认轨迹1的预览图片
    };
  },
  watch: {
    // 监听 selectedTrajectory 的变化
    selectedTrajectory(newVal) {
      switch (newVal) {
        case "param1":
          this.previewImage = "/轨迹1.png"; // 轨迹1的图片路径
          break;
        case "param2":
          this.previewImage = "/轨迹2.png"; // 轨迹2的图片路径
          break;
        case "param3":
          this.previewImage = "/轨迹3.png"; // 轨迹3的图片路径
          break;
        default:
          this.previewImage = "/default.png"; // 默认图片路径
      }
    },
  },
  methods: {
    // 更新相机参数并向父组件发出更新事件
    updateCameraOptions() {
      const parseVector = (str) => {
        const [x, y, z] = str.split(",").map(Number);
        return { x, y, z };
      };

      const updatedOptions = {
        up: parseVector(this.cameraParameters.up),
        position: parseVector(this.cameraParameters.position),
        lookAt: parseVector(this.cameraParameters.lookAt),
      };

      // 发射事件传递给父组件
      this.$emit("update-camera-options", updatedOptions);
    },
  },
};

</script>

<style scoped>
.functions {
  display: flex;
  flex-direction: column;
  margin-bottom: 5px;
  border: 1px solid #dfdbdb;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  width: 90%;
  height: 60%;
  border-radius: 5px;
}

.functions h3 {
  margin-top: 0px;
  font-size: 14px;
  margin-bottom: 10px;
  text-align: center;
}

.function-container {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  margin-bottom: 15px;
  width: 100%;
}

.function-container label {
  font-size: 12px;
  color: #333;
}

.function-container input {
  width: 60%;
  padding: 2px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.function-container input:focus {
  outline: none;
  border-color: #0078d7;
  box-shadow: 0 0 3px rgba(0, 120, 215, 0.5);
}

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.switch {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #333;
}

.switch input[type="radio"] {
  display: none;
  /* 隐藏单选按钮的默认样式 */
}

.switch .slider {
  position: relative;
  width: 36px;
  height: 18px;
  background-color: #ccc;
  border-radius: 15px;
  transition: background-color 0.3s;
  cursor: pointer;
}

.switch .slider:before {
  content: "";
  position: absolute;
  width: 14px;
  height: 14px;
  background-color: white;
  border-radius: 50%;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
}

.switch input:checked+.slider {
  background-color: #525354;
}

.switch input:checked+.slider:before {
  transform: translateX(18px);
}

.slider-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.slider-row span {
  font-size: 12px;
  color: #333;
}

.slider-row input[type="range"] {
  flex: 1;
  max-width: 150px;
  margin: 0 8px;
  appearance: none;
  height: 4px;
  background-color: #ccc;
  border-radius: 2px;
  outline: none;
}

.slider-row input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 10px;
  height: 10px;
  background-color: #aaaeb2;
  border-radius: 50%;
  cursor: pointer;
}

.slider-row .value {
  font-size: 12px;
  color: #333;
  width: 30px;
  text-align: center;
}

.preview-window {
  width: 90%;
  height: 40%;
  max-height: 60%;
  margin-top: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: rgb(255,255,255);
  padding: 10px;
}

.preview-window img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 5px;
}
</style>









