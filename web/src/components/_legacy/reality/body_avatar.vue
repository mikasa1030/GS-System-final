<template>
  <div class="app-container">
    <Sidebar :modelCategories="modelCategories" :faceCategories="faceCategories" :bodyCategories="bodyCategories"
      :humanCategories="humanCategories" :lightingCategories="lightingCategories" :hideButtons="['人体模型', '场景模型']"
      @update-splat-scene="updateSplatScenes" @update-video-path="updateVideoPath"  ></Sidebar>/>
    <MainContent :title="title" :previewButtons="previewButtons" :videoPath="currentVideoPath" />
    <!-- <SettingsPanel :settings="settings"  @update-camera-options="updateCameraOptions"/> -->
  </div>
</template>

<script>
// import Sidebar from "../sidebar1.vue";
import MainContent from "../maincontent_reality.vue";
import Sidebar from "../sidebar_reality.vue";
export default {
  name: "BodyAvatar",
  data() {
    return {
      title: "虚实融合",
      currentVideoPath:"/videos/origin.mp4",
      previewButtons: ["Actor Video", "Pose Sequence", "Scene Preview", "Light Preview"],
      splatScenes: "/models/scene/shibei.ply", // 默认路径
      settings: {
        brightness: 1.0,
        composePower: 1.0,
      },
      cameraoptions:{
        fov: 75,
        position: { x: 0.054, y: -0.219, z: 2.72 },
        up: { x: 0, y: -1, z: 0 },
        lookAt: { x: 0.025, y: -0.03, z: 4.85 },
      },
      modelCategories: [
        {
          title: "场景资产",
          buttons: [
            {
              name: "garden",
              path: "/models/scene/garden.ply",
              imageUrl: "/garden.png",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
            {
              name: "bonsai",
              path: "/models/scene/bonsai.ply",
              imageUrl: "/bonsai.JPG",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
            {
              name: "sofa",
              path: "/models/scene/replica.ply",
              imageUrl: "/sofa.png",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
            {
              name: "factory",
              path: "/models/scene/point_cloud.ply",
              imageUrl: "/factory.png",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
            {
              name: "stone",
              path: "/models/scene/shibei.ply",
              imageUrl: "/shibei.png",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -5, z: -10 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
          ],
        },
      ],
      faceCategories: [

        {
          title: "资产库",
          buttons: [
            { name: "表情 1", path: "/models/scene/beach.ply" },
            { name: "表情 2", path: "/models/scene/park.ply" },
            { name: "动作 1", path: "/models/scene/road.ply" },
            { name: "动作 2", path: "/models/scene/desert.ply" },
          ],
        },
      ],
      bodyCategories: [

        {
          title: "资产库",
          buttons: [
            { name: "Case 1", path: "/models/scene/beach.ply" },
            { name: "Case 2", path: "/models/scene/park.ply" },
            { name: "Case 3", path: "/models/scene/road.ply" },
            { name: "Case 4", path: "/models/scene/desert.ply" },
          ],
        },
      ],
      humanCategories: [
      {
          title: "自定义",
          buttons: [
            { name: "Case 1", path: "/models/scene/garden.ply" },
            { name: "Case 2", path: "/models/scene/bonsai.ply" },
            { name: "Case 3", path: "/models/scene/replica.ply" },
            { name: "Case 4", path: "/models/scene/point_cloud.ply" },
          ],
        },
        {
          title: "资产库",
          buttons: [
            { name: "Case 1", path: "/models/scene/beach.ply" },
            { name: "Case 2", path: "/models/scene/park.ply" },
            { name: "Case 3", path: "/models/scene/road.ply" },
            { name: "Case 4", path: "/models/scene/desert.ply" },
          ],
        },
      ],
      lightingCategories: [
        {
          title: "数字人资产",
          buttons: ["case 1", "case 2", "case 3"],
        },
      ],
    };
  },
  components: {
    Sidebar,
    MainContent,
  },
  methods: {
    // 更新视频路径的方法
    updateVideoPath(newPath) {
      console.log("Updating videoScenes to:", newPath);
      this.currentVideoPath = newPath;
    },
    updateSplatScenes(newPath) {
      // 更新 splatScenes 的路径
      console.log("Updating splatScenes to:", newPath);
      this.splatScenes = newPath;
    },

    updateCameraOptions(newOptions) {
      // 更新 cameraOptions 并打印日志
      console.log("Camera options updated to:", newOptions);
      this.cameraOptions = newOptions;
    },
  },
};
</script>

<style scoped>
/* 全局样式 */
.app-container {
  display: flex;
  min-width: 100vw;
  height: 100vh;
  background-color: #ced0d2;
  justify-content: center;
  align-items: center;
}
</style>
