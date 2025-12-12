<template>
    <div ref="threeContainer" class="three-container"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
  import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d';
  
  export default {
    name: 'ThreeScene',
    mounted() {
      this.initThree();
    },
    methods: {
      initThree() {
        const container = this.$refs.threeContainer;
        const width = container.clientWidth;
        const height = container.clientHeight;
  
        // 创建场景
        const scene = new THREE.Scene();
  
        // 创建相机
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.z = 5;
  
        // 创建渲染器
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(width, height);
        container.appendChild(renderer.domElement);
  
        // 创建 OrbitControls 控制器
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // 启用阻尼效果
        controls.dampingFactor = 0.05; // 阻尼系数
        controls.screenSpacePanning = false; // 禁止屏幕空间平移
        controls.minDistance = 1; // 最小缩放距离
        controls.maxDistance = 1000; // 最大缩放距离
        controls.maxPolarAngle = Math.PI / 2; // 最大垂直旋转角度
  
        // 创建一个简单的立方体
        const geometry = new THREE.BoxGeometry();
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const cube = new THREE.Mesh(geometry, material);
        // scene.add(cube);
  
        // 创建 GaussianSplats3D Viewer
        const viewer = new GaussianSplats3D.DropInViewer({
          gpuAcceleratedSort: false,
          useBuiltInControls: false,
          sharedMemoryForWorkers: false,
          
        });
  
        // 添加点云场景
        viewer.addSplatScenes([
          {
            path: '/models/point_cloud.ply',
            splatAlphaRemovalThreshold: 20,
            'showLoadingUI': true,
            rotation: [0.14824434, -0.0761755, 0.1410657, 0.976020],
            scale: [1.5, 1.5, 1.5],
            position: [-3, -2, -3.2],
          },
        ]);
  
        scene.add(viewer);
  
        // 动画循环
        const animate = () => {
          requestAnimationFrame(animate);
          cube.rotation.x += 0.01;
          cube.rotation.y += 0.01;
          controls.update(); // 更新控制器
          renderer.render(scene, camera);
        };
  
        animate();
  
        // 监听窗口大小变化
        window.addEventListener('resize', this.onWindowResize);
      },
      onWindowResize() {
        const container = this.$refs.threeContainer;
        const width = container.clientWidth;
        const height = container.clientHeight;
  
        this.renderer.setSize(width, height);
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
      },
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.onWindowResize);
    },
  };
  </script>
  
  <style scoped>
  .three-container {
    width: 100%;
    height: 100%;
    background-color: #000;
  }
  </style>
  