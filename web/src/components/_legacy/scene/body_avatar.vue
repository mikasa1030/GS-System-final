<template>
  <div class="app-container">
    <Sidebar1
      :modelCategories="modelCategories"
      :humanCategories="humanCategories"
      :sceneCategories="sceneCategories"
      :driveCategories="driveCategories"
      :lightingCategories="lightingCategories"
      :hideButtons="['人体模型', '驱动', '场景模型']"
      @update-splat-scene="updateSplatScenes"
      @add-button="handleAddButton"
      :floderkey="'scene'"
    />
    <MainContent
      :title="title"
      :previewButtons="previewButtons"
      :splatScenes="splatScenes"
      :cameraOptions="cameraOptions"
    />
    <SettingsPanel
      :settings="settings"
      @update-camera-options="updateCameraOptions"
    />
  </div>
</template>

<script>

import MainContent from "../maincontent.vue";
import SettingsPanel from "../settingpanel.vue";
import Sidebar1 from "../sidebar1.vue";

export default {
  name: "BodyAvatar",

  data() {
    return {
      title: "数字场景建模",
      previewButtons: [
        "Actor Video",
        "Pose Sequence",
        "Scene Preview",
        "Light Preview",
      ],
      splatScenes: "/models/scene/garden.ply", // 默认路径
      settings: {
        brightness: 1.0,
        composePower: 1.0,
      },
      cameraOptions: {
        fov: 75,
        position: { x: 0, y: -0.5, z: -3 },
        up: { x: 0, y: -1, z: 0 },
        lookAt: { x: -10, y: 5, z: 0 },
      },
      modelCategories: [
        {
          title: "数字资产",
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
      driveCategories: [
        {
          title: "资产库",
          buttons: ["case 1", "case 2", "case 3", "case4"],
        },
      ],
      lightingCategories: [
        {
          title: "环境光贴图",
          buttons: [
            { name: "光照 1" ,imageUrl: "/light1.png",},
            { name: "光照 2" ,imageUrl: "/light1.png",},
            { name: "光照 3" ,imageUrl: "/light1.png",},
            { name: "光照 4" ,imageUrl: "/light1.png",},
          ],
        },
      ],
    };
  },

  components: {

    MainContent,
    SettingsPanel,
    Sidebar1,
  },
  methods: {
    handleAddButton({ categoryTitle, button }) {
      const category = this.modelCategories.find(
        (cat) => cat.title === categoryTitle
      );
      if (category) {
        category.buttons.unshift(button); // 将新按钮添加到当前分类的按钮数组开头
      }
    },
    updateSplatScenes({ path, cameraOptions }) {
      console.log("Updating splatScenes to:", path);
      this.splatScenes = path;

      if (cameraOptions) {
        console.log("Updating cameraOptions to:", cameraOptions);
        this.cameraOptions = cameraOptions;
      }
    },
    updateCameraOptions(newOptions) {
      // 更新 cameraOptions 并打印日志
      console.log("Camera options updated to:", newOptions);
      this.cameraOptions = newOptions;
    },
    update() {
      console.log("Camera Options in Parent:", this.cameraOptions);
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
  background-color: rgb(255, 255, 255);
  justify-content: space-around;
  align-items: center;
}
</style>
