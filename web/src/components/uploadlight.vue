<template>
  <div class="upload-light">
    <!-- 移除上传按钮 -->
    <!-- 预览区域 -->
    <div class="image-preview">
      <div
        ref="previewContainer"
        class="preview-container"
      >
        <canvas
          ref="previewCanvas"
          class="preview-canvas"
        ></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader";
import { EXRLoader } from "three/examples/jsm/loaders/EXRLoader";
import * as THREE from "three";

export default {
  name: "UploadPreviewComponent",
  props: {
    storedTexture: { type: Object, default: null }, // 接收父组件传递的纹理
  },
  mounted() {
    // 如果父组件传递了纹理，则重新渲染
    if (this.storedTexture) {
      this.renderToCanvas(this.storedTexture);
    }
  },
  watch: {
    // 当父组件 currentTexture 变化时，自动重绘
    storedTexture(newTex) {
      if (newTex) {
        this.renderToCanvas(newTex);
      }
    }
  },
  methods: {
    /**
     * 直接处理上传文件的方法
     */
    uploadFile(file) {
      const fileName = file.name.toLowerCase();

      try {
        if (fileName.endsWith(".hdr")) {
          this.loadHDR(file);
        } else if (fileName.endsWith(".exr")) {
          this.loadEXR(file);
        } else {
          alert("请上传正确的 .hdr 或 .exr 文件！");
        }
      } catch (error) {
        console.error("文件加载失败:", error);
      }
    },

    loadHDR(file) {
      const url = URL.createObjectURL(file);
      const loader = new RGBELoader();
      loader.load(
        url,
        (texture) => {
          this.$emit("update-texture", texture); // 将纹理传递给父组件
          this.renderToCanvas(texture);
        },
        undefined,
        (err) => {
          console.error("加载 HDR 文件失败", err);
        }
      );
    },

    loadEXR(file) {
      const url = URL.createObjectURL(file);
      const loader = new EXRLoader();
      loader.load(
        url,
        (texture) => {
          this.$emit("update-texture", texture); // 将纹理传递给父组件
          this.renderToCanvas(texture);
        },
        undefined,
        (err) => {
          console.error("加载 EXR 文件失败", err);
        }
      );
    },

    renderToCanvas(texture) {
      const canvas = this.$refs.previewCanvas;
      const container = this.$refs.previewContainer;

      if (!canvas || !container) {
        console.error("Canvas 或容器未找到");
        return;
      }

      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;

      const renderer = new THREE.WebGLRenderer({ canvas });
      renderer.setSize(containerWidth, containerHeight);

      const scene = new THREE.Scene();
      // 设置背景颜色为您想要的颜色，例如浅灰色
      scene.background = new THREE.Color(0x2b3a4a); // 设置为浅灰色 (可以改为其他颜色)
      const camera = new THREE.PerspectiveCamera(
        50,
        containerWidth / containerHeight,
        0.1,
        1000
      );
      camera.position.z = 1;

      const material = new THREE.MeshBasicMaterial({ map: texture });
      const plane = new THREE.PlaneGeometry(1, 1);
      const mesh = new THREE.Mesh(plane, material);
      scene.add(mesh);

      renderer.render(scene, camera);
    },
  },
};
</script>


<style scoped>
.upload-light {
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  justify-content: center; /* 垂直居中 */
  width: 90%; /* 确保子组件宽度适应父容器 */
  height: 80%;
  max-width: 400px; /* 限制最大宽度 */
  margin: 0 auto; /* 使组件水平居中 */
}

.image-preview {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  max-height: 336px;
  flex-direction: column;
  align-items: center;
}

.image-preview h2 {
  font-size: 16px;
  margin-bottom: 10px;
}

.preview-container {
  position: relative;
  width: 90%;
  height: 90%;
  max-width: 400px; /* 最大宽度 */
  aspect-ratio: 1/1; /* 保持宽高比 1:1 */
  border: 1px solid #ccc;
  overflow: hidden; /* 防止内容溢出 */
  display: flex;
  background-color: black;
}

.preview-canvas {
  width: 100%;
  height: auto;
  display: block;
}
</style>
