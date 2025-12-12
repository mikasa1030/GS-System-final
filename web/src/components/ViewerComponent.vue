<template>
    <div ref="viewerContainer" style="width: 400px; height: 300px;"></div>
  </template>
  
  <script>
  import { onMounted, ref } from 'vue';
  import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d';
  
  export default {
    name: 'ViewerComponent',
    setup() {
      const viewerContainer = ref(null);
  
      onMounted(() => {
        const viewer = new GaussianSplats3D.Viewer({
          cameraUp: [0, -1, -0.6],
          initialCameraPosition: [-1, -4, 6],
          initialCameraLookAt: [0, 4, 0],
        });
  
        viewer.addSplatScene('/models/point_cloud.ply', {
          splatAlphaRemovalThreshold: 5,
          showLoadingUI: true,
          position: [0, 1, 0],
          rotation: [0, 0, 0, 1],
          scale: [1.5, 1.5, 1.5],
        }).then(() => {
          viewer.start();
        });
  
        viewerContainer.value.appendChild(viewer.renderer.domElement);
      });
  
      return {
        viewerContainer,
      };
    },
  };
  </script>
  
  <style scoped>
  div {
    width: 100%;
    height: 100%;
  }
  </style>
  