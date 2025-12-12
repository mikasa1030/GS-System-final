<template>
  <div class="audio-visualizer">
    <!-- 上传音频文件 -->
    <input
      type="file"
      id="audioFileInput"
      @change="handleAudioUpload"
      accept="audio/*"
      style="display: none;"
    />
    <!-- 自定义按钮触发文件选择 -->
    <label
      for="audioFileInput"
      class="upload-button"
    >
      选择音频文件
    </label>

    <!-- 音波展示 -->
    <canvas
      ref="visualizerCanvas"
      class="visualizer"
    ></canvas>

    <!-- 音频播放控制 -->
    <div class="controls">
      <button @click="togglePlay">{{ isPlaying ? "暂停" : "播放" }}</button>
      <button>{{ "生成" }}</button>
    </div>

  </div>
</template>
  
  <script>
export default {
  data() {
    return {
      audioContext: null, // Web Audio API 上下文
      audioSource: null, // 音频源
      analyser: null, // 分析器节点
      audioElement: null, // 原生 Audio 元素
      isPlaying: false, // 播放状态
      animationId: null, // 动画帧 ID
    };
  },
  methods: {
    /**
     * 处理音频文件上传
     */
    handleAudioUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        return;
      } else {
        this.$emit("trigger-parent-method", event);
      }

      // 停止当前播放
      this.stop();

      // 创建新的 Audio 元素
      this.audioElement = new Audio(URL.createObjectURL(file));
      this.audioElement.crossOrigin = "anonymous"; // 跨域支持
      this.audioElement.loop = true; // 开启循环播放

      // 初始化 Web Audio API
      this.initAudioContext();

      // 自动播放
      this.togglePlay();
    },

    /**
     * 初始化 Web Audio API
     */
    initAudioContext() {
      if (!this.audioContext) {
        this.audioContext = new (window.AudioContext ||
          window.webkitAudioContext)();
      }

      // 创建分析器节点
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256; // 设置 FFT 大小
      this.analyser.smoothingTimeConstant = 0.85; // 平滑时间常数

      // 连接音频源和分析器
      this.audioSource = this.audioContext.createMediaElementSource(
        this.audioElement
      );
      this.audioSource.connect(this.analyser);
      this.analyser.connect(this.audioContext.destination); // 输出到扬声器
    },

    /**
     * 播放或暂停音频
     */
    togglePlay() {
      if (!this.audioElement) return;

      if (this.isPlaying) {
        this.audioElement.pause();
        cancelAnimationFrame(this.animationId); // 停止动画
      } else {
        this.audioElement.play();
        this.visualize(); // 开始可视化
      }
      this.isPlaying = !this.isPlaying;
    },

    /**
     * 停止音频播放和动画
     */
    stop() {
      if (this.audioElement) {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
      }
      this.isPlaying = false;
      cancelAnimationFrame(this.animationId);
    },

    /**
     * 可视化音频数据
     */
    visualize() {
      const canvas = this.$refs.visualizerCanvas;
      const canvasContext = canvas.getContext("2d");

      // 设置 Canvas 尺寸
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;

      const bufferLength = this.analyser.frequencyBinCount; // 数据长度
      const dataArray = new Uint8Array(bufferLength); // 存储音频数据

      const draw = () => {
        this.analyser.getByteFrequencyData(dataArray); // 获取频谱数据

        // 清除画布
        canvasContext.clearRect(0, 0, canvas.width, canvas.height);

        // 绘制柱状图
        const barWidth = (canvas.width / bufferLength) * 1.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          barHeight = dataArray[i];

          const r = (barHeight + 100) * 2;
          const g = 50;
          const b = 150;

          canvasContext.fillStyle = "#d3d3d3";
          canvasContext.fillRect(
            x,
            canvas.height - barHeight / 2,
            barWidth,
            barHeight / 2
          );

          x += barWidth + 1;
        }

        this.animationId = requestAnimationFrame(draw); // 循环调用
      };

      draw(); // 开始绘制
    },
  },
  beforeDestroy() {
    // 清理资源
    if (this.audioContext) {
      this.audioContext.close();
    }
    cancelAnimationFrame(this.animationId);
  },
};
</script>
  
  <style scoped>
.audio-visualizer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 90%;
  height: 100%; /* 让容器高度跟随父组件 */
  overflow: hidden; /* 防止溢出 */
  box-sizing: border-box;
}

.upload-button {
  width: 60%;
  height: 5%;
  display: inline-block;

  padding: 10px 10px;
  font-size: 12px;
  font-weight: bold;
  color: white;
  background-color: #3b3d3f;
  border: none;
  border-radius: 1px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button:hover {
  background-color: #505255;
}

.controls {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.controls button {
  white-space: nowrap; /* 防止文字换行 */
  width: 30%;
  height: 20%;
  padding: 10px 20px;
  font-size: 8px;
  cursor: pointer;
  border: none;
  border-radius: 1px;
  background-color: #3b3d3f;
  color: #fff;
  /* 关键部分：设置文本居中 */
  display: flex; /* 使用 Flex 布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  text-align: center; /* 文本居中（备用） */
}

.visualizer {
  width: 98%;
  height: auto; /* 自动调整高度以保持比例 */
  aspect-ratio: 16 / 9; /* 固定宽高比 */
  background-color: #ffffff;
  border: 1px solid #444;
  border-radius: 8px;
  margin-bottom: 5px;
  margin-top: 5px;
}
</style>
  