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
import { EXRLoader } from "three/examples/jsm/loaders/EXRLoader";
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader";
import * as THREE from "three";

export default {
  name: "UploadPreviewComponent",
  props: {
    // 接收父组件传入的文件路径
    texturePath: { type: String, default: '' },
  },
  mounted() {
    if (this.texturePath) {
      this.loadTextureFromPath(this.texturePath);
    }
  },
  watch: {
    // 当路径变化时重新加载纹理文件
    texturePath(newPath) {
      if (newPath) {
        this.loadTextureFromPath(newPath);
      }
    },
  },
  methods: {
    loadTextureFromPath(path) {
      const fileExtension = path.split(".").pop().toLowerCase();
      try {
        if (fileExtension === "exr") {
          this.loadEXR(path);
        } else if (fileExtension === "hdr") {
          this.loadHDR(path);
        } else {
          alert("请上传正确的 .hdr 或 .exr 文件！");
        }
      } catch (error) {
        console.error("文件加载失败:", error);
      }
    },
    loadHDR(path) {
      const loader = new RGBELoader();
      loader.load(
        path,
        (texture) => {
          // 成功加载后渲染纹理
          this.renderToCanvas(texture);
        },
        undefined,
        (err) => {
          console.error("加载 HDR 文件失败", err);
        }
      );
    },
    loadEXR(path) {
      const loader = new EXRLoader();
      loader.load(
        path,
        (texture) => {
          // 成功加载后渲染纹理
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
      // 获取容器尺寸
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;

      // 创建渲染器并设置 canvas 大小
      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
      renderer.setSize(containerWidth, containerHeight);

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x2b3a4a);

      // 使用正交相机，让视口与容器尺寸对应
      const camera = new THREE.OrthographicCamera(
        -containerWidth / 2,  // left
        containerWidth / 2,   // right
        containerHeight / 2,  // top
        -containerHeight / 2, // bottom
        0.1,
        1000
      );
      camera.position.z = 1;

      // 创建与容器尺寸匹配的平面几何体
      const geometry = new THREE.PlaneGeometry(containerWidth, containerHeight);
      const material = new THREE.MeshBasicMaterial({ map: texture });
      const mesh = new THREE.Mesh(geometry, material);
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
  width: 90%; /* 保证宽度适应父容器 */
  height: 100%;
  max-width: 400px; /* 限制最大宽度 */
  margin: 0 auto; /* 水平居中 */
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
  max-width: 400px; /* 限制最大宽度 */
  aspect-ratio: 1/1; /* 保持宽高比 1:1 */
  border: 1px solid #ccc;
  overflow: hidden; /* 防止溢出 */
  display: flex;
  background-color: black;
}

.preview-canvas {
  width: 100%;
  height: auto;
  display: block;
}
</style>
  