<template>
    <div class="settings-panel">
      <!-- <div class="header">
        <h3>基本信息</h3>
        <p>Running on NVIDIA GeForce RTX 4090</p>
        <p>FPS: 276.246 | Torch VRAM: 11313 MB</p>
        <p>Frame time: 3.620 ms</p>
        
      </div> -->
      <functions :buttonLabels="functionButtonLabels"  @update-camera-options="updateCameraOptions"/>
  
      <!-- <settingbuttons /> -->
      <functions1 :buttonLabels="functionButtonLabels" />
      <exportoptions />
     
    </div>
  </template>
  
  <script>
  import settingbuttons from './settingbuttons.vue'
  import functions from './functionpanel.vue'
  import exportoptions from './exportoptions.vue'
  import functions1 from "./functionsidebar.vue"
  export default {
    name: "SettingsPanel",
    components:{
      settingbuttons,
      functions,
      exportoptions,
      functions1
    },
    props: {
      settings: {
        type: Object,
        required: true,
      },
      cameraOptions: {
      type: Object,
      required: true,
    },


    },
    data() {
      return {
        collectTimings: false,
        visualizationMode: "linear",
        // 定义按钮名称
        functionButtonLabels: {
          headRefine: "物体编辑", // 头部细化按钮名称
          stylize: "场景风格化", // 风格化按钮名称
        },
      };
    },
    methods: {
  
      setVisualizationMode(mode) {
        this.visualizationMode = mode;
      },
      download() {
        console.log("Download triggered");
      },

      updateCameraOptions(newOptions) {
      // 将更新的相机参数发射给父组件
      this.$emit("update-camera-options", newOptions);
    },
    },
  };
  </script>
  
  <style scoped>
  .settings-panel {
    display: flex;
    flex-direction: column;
    width: 14%;
    height: 95%;
    padding: 10px;
    box-shadow: inset 1px 0px 5px rgba(0, 0, 0, 0.1);
    
    background-color: #dbdada;
   
  }
  
  .settings-panel h3 {
    text-align: center;
    margin: 8px 0;
    font-size: 14px;
    color: #333;
    font-weight: bold;
  }
  
  .settings-panel p {
    text-align: center;
    font-size: 10px;
    margin: 4px 0;
    color: #555;
  }
  
  .settings-panel button {
    width: 90%;
    margin: 5px auto;
    padding: 8px;
    font-size: 12px;
    text-align: center;
    color: #fff;
    background-color: #0078d7;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  </style>
  