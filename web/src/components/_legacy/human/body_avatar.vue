<template>
  <div class="app-container">
    <Sidebar
      :modelCategories="modelCategories"
      :faceCategories="faceCategories"
      :bodyCategories="bodyCategories"
      :driveCategories="driveCategories"
      :lightingCategories="lightingCategories"
      :hideButtons="['人体模型', '场景模型']"
      @update-splat-scene="updateSplatScenes"
      @update-camera-options="updateCameraOptions"
      @add-button="handleAddButton"
      :floderkey="'body'"
      @update-uploaded-paths="handleUploadedPaths"
    />
    <MainContent
      :title="title"
      :previewButtons="previewButtons"
      :splatScenes="pathsList"
      :cameraOptions="cameraOptions"
    />
    <SettingsPanel
      :settings="settings"
      @update-camera-options="updateCameraOptions"
      @update-uploaded-paths="handleUploadedPaths"
    />
  </div>
</template>

<script>
import Sidebar from "../sidebar_body.vue";
import MainContent from "../maincontent_body.vue";
import SettingsPanel from "../settingpanel1.vue";

export default {
  name: "BodyAvatar",
  data() {
    return {
      title: "数字人建模",
      previewButtons: [
        "Actor Video",
        "Pose Sequence",
        "Scene Preview",
        "Light Preview",
      ],
      splatScenes: "/models/human/face.ply", // 默认路径
      pathsList: ["/models/human/f3c.ply"],
      cameraOptions: {
        fov: 75,
        position: { x: 0, y: -5, z: -10 },
        up: { x: 0, y: -1, z: 0 },
        lookAt: { x: 0, y: 0, z: 0 },
      },
      settings: {
        brightness: 1.0,
        composePower: 1.0,
      },
      modelCategories: [
        {
          title: "数字资产",
          buttons: [
            {
              name: "Case 1",
              path: "/models/human/m3c.ply",
              cameraOptions: {
                fov: 75,
                position: { x: -0.2, y: 0, z: -3 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: -0.2, y: 0.1, z: 5 },
              },
            },
            {
              name: "Case 2",
              path: "/models/human/f4c.ply",
              cameraOptions: {
                fov: 75,
                position: { x: -0.2, y: 0, z: -3 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: -0.2, y: 0.1, z: 5 },
              },
            },
            {
              name: "Case 3",
              path: "/models/human/dna.ply",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: -0.5, z: -6 },
                up: { x: 0, y: -1, z: 0 },
                lookAt: { x: 0, y: 0, z: 0 },
              },
            },
            {
              name: "Case 4",
              path: "/models/human/zzr1.ply",
              cameraOptions: {
                fov: 75,
                position: { x: 0, y: 3, z: -10 },
                up: { x: -1, y: 0, z: 0 },
                lookAt: { x: 0, y: 0, z: -5 },
              },
            },
          ],
        },
      ],
      faceCategories: [
        {
          title: "驱动资产",
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
      driveCategories: [
        {
          title: "表情",
          buttons: ["case 1", "case 2", "case 3", "case4"],
        },
        {
          title: "肢体",
          buttons: ["case 1", "case 2", "case 3", "case4"],
        },
      ],
      lightingCategories: [
        {
          title: "环境光贴图",
          buttons: ["case 1", "case 2", "case 3", "case4"],
        },
      ],
    };
  },
  components: {
    Sidebar,
    MainContent,
    SettingsPanel,
  },
  methods: {
    handleUploadedPaths(pathsList) {
      // 在父组件中处理接收到的 pathsList
      console.log(pathsList);
      this.pathsList = pathsList;
    },
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
      this.pathsList = [this.splatScenes];
      console.log("现在的pathlist:", this.splatScenes);
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
