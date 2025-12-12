<template>
  <div ref="threeContainer" class="three-container"></div>
</template>

<script setup>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { onMounted, ref } from "vue";

const threeContainer = ref(null);

onMounted(() => {
  const scene = new THREE.Scene();

  // 创建几何体和材质
  const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
  const cubeMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
  const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
  scene.add(cube);

  // 创建相机
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(5, 5, 5);
  camera.lookAt(scene.position);

  // 创建渲染器
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);

  // 将渲染器的 DOM 元素添加到容器中
  if (threeContainer.value) {
    threeContainer.value.appendChild(renderer.domElement);
  }

  // 创建轨道控制器
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.update();

  // 动态渲染函数
  function render() {
    requestAnimationFrame(render);
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
  render();

  // 监听窗口大小变化，更新相机和渲染器
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
});
</script>

<style>
.three-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
