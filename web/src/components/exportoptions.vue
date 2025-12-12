<template>
  <div class="export-options">
    <h3>导出</h3>
    <div class="export-buttons">
      <!-- 第一行 -->
      <div class="button-row">
        <div class="radio-button">
          <input
            type="radio"
            id="image"
            name="row1"
            value="image"
            :checked="selectedRow1 === 'image'"
            @click="toggleButton('image', 1)"
          />
          <label for="image">图像</label>
        </div>
        <div class="radio-button">
          <input
            type="radio"
            id="gaussian"
            name="row1"
            value="gaussian"
            :checked="selectedRow1 === 'gaussian'"
            @click="toggleButton('gaussian', 1)"
          />
          <label for="gaussian">高斯点云</label>
        </div>
      </div>
      <!-- 第二行 -->
      <div class="button-row">
        <div class="radio-button">
          <input
            type="radio"
            id="currentFrame"
            name="row2"
            value="currentFrame"
            :checked="selectedRow2 === 'currentFrame'"
            @click="toggleButton('currentFrame', 2)"
          />
          <label for="currentFrame">当前帧</label>
        </div>
        <div class="radio-button">
          <input
            type="radio"
            id="sequence"
            name="row2"
            value="sequence"
            :checked="selectedRow2 === 'sequence'"
            @click="toggleButton('sequence', 2)"
          />
          <label for="sequence">序列</label>
        </div>
      </div>
    </div>
    <button @click="download">下载</button>
  </div>
</template>

<script>
export default {
  name: "ExportOptions",
  data() {
    return {
      selectedRow1: null, // 第一行选中的选项
      selectedRow2: null, // 第二行选中的选项
    };
  },
  methods: {
    toggleButton(option, row) {
      // 检查是否为当前选中按钮，如果是则取消选中
      if (row === 1) {
        this.selectedRow1 = this.selectedRow1 === option ? null : option;
      } else if (row === 2) {
        this.selectedRow2 = this.selectedRow2 === option ? null : option;
      }
    },
    download() {
      console.log("Download triggered");
      console.log("Selected Row 1:", this.selectedRow1);
      console.log("Selected Row 2:", this.selectedRow2);
    },
  },
};
</script>

<style scoped>
.export-options {
  display: flex;
  margin-top: 5px;
  flex-direction: column;
  justify-content: space-between;
  height: 20%;
  background-color: rgb(251, 251, 251);
  border-radius: 5px;
}

.export-options h3 {
  text-align: center;
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
  margin-top: 5px;
}

/* 按钮容器样式 */
.export-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 每一行的布局 */
.button-row {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 单个圆点按钮和文字的样式 */
.radio-button {
  display: flex;
  align-items: center;
  gap: 10px; /* 圆点和文字的间距 */
  width:45%;
  
}

.radio-button input[type="radio"] {
  appearance: none;
  width: 16px; /* 外圈大小 */
  height: 16px;
  border: 2px solid #ccc;
  border-radius: 50%;
  outline: none;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  background-color: white;
}

/* 选中状态：在中心添加一个小圆点 */
.radio-button input[type="radio"]:checked:before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px; /* 内圈大小 */
  height: 8px;
  background-color: #414243; /* 选中状态的颜色 */
  border-radius: 50%;
  transform: translate(-50%, -50%);
}
/* 非选中状态的边框颜色 */
.radio-button input[type="radio"]:hover {
  border-color: #aaa; /* 鼠标悬停时的外圈颜色 */
}

.radio-button label {
  font-size: 14px;
  color: #333;
  cursor: pointer;
  user-select: none; /* 防止选中文字 */
}

/* 下载按钮样式 */
button {
  width: 90%;
 
  margin: 10px auto;
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  background-color: #2d2c2c;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

button:hover {
  background-color: #005a9e;
}
</style>
