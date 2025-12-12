<template>
    <div class="functions">
      <h3>功能</h3>
      <div class="function-container">
        <!-- 头部细化按钮 -->
        <button @click="togglePopup('headRefine')" class="titlebutton">{{ buttonLabels.headRefine }}</button>
        <div v-if="popupType === 'headRefine'" class="popup">
          <h4>物体编辑</h4>
          <p>选择模型并输入指令实现物体编辑</p>
          <div class="popup-buttons">
            <button>模型选择</button>
            <button>指令输入</button>
          </div>
          <button class="train-button">一键训练</button>
        </div>
      </div>
  
      <div class="function-container">
        <!-- 风格化按钮 -->
        <button @click="togglePopup('stylize')" class="titlebutton">{{ buttonLabels.stylize }}</button>
        <div v-if="popupType === 'stylize'" class="popup">
          <h4>风格化功能</h4>
          <p>上传图片并选择风格进行风格化</p>
          <div class="popup-buttons">
            <button>图片上传</button>
            <button>选择风格</button>
          </div>
          <button class="train-button">一键应用</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "FunctionsPanel",
    props: {
    // 父组件传递的按钮名称
    buttonLabels: {
      type: Object,
      required: true,
    },
  },
    data() {
      return {
        popupType: null, // 控制弹出框的类型
      };
    },
    methods: {
      togglePopup(type) {
        // 如果点击同一个按钮，关闭弹窗；否则切换到新弹窗
        this.popupType = this.popupType === type ? null : type;
      },
    },
  };
  </script>
  
  <style scoped>
  .functions {
    display: flex;
    flex-direction: column;
    margin-bottom: 0px;
    border: 1px solid #ede7e7;
 
    align-items: center;
    height:18%;
    width: 100%;
    background-color: #f9f9f9;
    border-radius: 5px;
    
  }
  .functions h3 {
    font-size: 16px;
    margin-bottom: 5px;
    margin-top: 5px;
  }
  .function-container {
    position: relative; /* 让弹出框的定位基于当前容器 */
    margin-bottom: 5px;
    width:95%;
    height:40px;
 
    
  }
  .titlebutton {
    width: 100%;
    height:90%;
    background-color: #323941;
    border-radius: 5px;
    color: #fff;
  }
  /* 弹出框样式 */
  .popup {
    position: absolute;
    top: -130px; /* 根据需要调整此值让弹出框与按钮对齐 */
    left: -230px; /* 弹出框在按钮左侧 */
    width: 200px;
    padding: 10px;
    background-color: #f9f9f9;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    z-index: 10;
  }
  
  .popup h4 {
    font-size: 14px;
    margin-bottom: 10px;
    text-align: center;
  }
  
  .popup p {
    font-size: 12px;
    margin-bottom: 10px;
    text-align: center;
    color: #666;
  }
  
  .popup-buttons {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .popup-buttons button {
    width: 45%;
    padding: 8px;
    background-color: #ddd;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .popup-buttons button:hover {
    background-color: #ccc;
  }
  
  .train-button {
    width: 100%;
    padding: 8px;
    background-color: #0078d7;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
  }
  
  .train-button:hover {
    background-color: #005a9e;
  }
  </style>
  