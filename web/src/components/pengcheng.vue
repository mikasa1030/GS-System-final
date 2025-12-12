<template>
    <div id="app">
      <div ref="viewerContainer" style="width: 100%; height: 100vh;"></div>
    </div>
  </template>
  
  <script>
  import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d';
  
  export default {
    name: 'App',
    mounted() {
      // 初始化 Viewer
      const viewer = new GaussianSplats3D.Viewer({
        cameraUp: [0, -1, -0.6],
        initialCameraPosition: [-1, -4, 6],
        initialCameraLookAt: [0, 4, 0],
      });
  
      // 添加 Splat 场景
      viewer
        .addSplatScene('/models/point_cloud_pengcheng.ply', {
          splatAlphaRemovalThreshold: 5,
          showLoadingUI: true,
          position: [0, 1, 0],
          rotation: [0, 0, 0, 1],
          scale: [1.5, 1.5, 1.5],
        })
        .then(() => {
          viewer.start();
        });
  
      // 将 Viewer 绑定到容器
      viewer.setContainer(this.$refs.viewerContainer);
    },
  };
  </script>