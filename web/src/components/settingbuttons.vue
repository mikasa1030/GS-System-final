<template>
    <div class="visualization-settings">
      <h3>控制参数</h3>
      <div class="toggle-group">
        <!-- 开关式按钮 -->
        <label class="switch">
          <span>参数1</span>
          <input type="checkbox" v-model="settings.param1" />
          <span class="slider"></span>
        </label>
        <label class="switch">
          <span>参数2</span>
          <input type="checkbox" v-model="settings.param2" />
          <span class="slider"></span>
        </label>
        <label class="switch">
          <span>参数3</span>
          <input type="checkbox" v-model="settings.param3" />
          <span class="slider"></span>
        </label>
        <label class="switch">
          <span>参数4</span>
          <input type="checkbox" v-model="settings.param4" />
          <span class="slider"></span>
        </label>
        <label class="switch">
          <span>参数5</span>
          <input type="checkbox" v-model="settings.param4" />
          <span class="slider"></span>
        </label>
      </div>
  
      <!-- 滑动按钮 -->
      <div class="slider-group">
        
        <label class="slider-row">
          <span>控制1</span>
          <input type="range" v-model="settings.slider1" min="0" max="100" />
          <span class="value">{{ settings.slider1 }}</span>
        </label>
        <label class="slider-row">
          <span>控制2</span>
          <input type="range" v-model="settings.slider2" min="0" max="100" />
          <span class="value">{{ settings.slider2 }}</span>
        </label>
        <label class="slider-row">
          <span>控制3</span>
          <input type="range" v-model="settings.slider3" min="0" max="100" />
          <span class="value">{{ settings.slider3 }}</span>
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "VisualizationSettings",
    data() {
      return {
        settings: {
          param1: false,
          param2: false,
          param3: false,
          param4: false,
          slider1: 50,
          slider2: 50,
          slider3: 50,
        },
      };
    },
  };
  </script>
  
  <style scoped>
  .visualization-settings {
    padding: 15px;
    font-family: Arial, sans-serif;
    color: #333;
    border: 1px solid #d9d9d9;
    background-color: #f9f9f9;
    max-width: 300px;
    border-radius: 5px;
  }
  
  .visualization-settings h3 {
    font-size: 14px;
    margin-bottom: 10px;
    color: #555;
  }
  
  /* 开关组样式 */
  .toggle-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .switch {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #555;
  }
  
  .switch span {
    margin-right: 10px;
  }
  
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .switch .slider {
    position: relative;
    width: 36px;
    height: 18px;
    background-color: #ccc;
    border-radius: 15px;
    transition: background-color 0.3s;
    cursor: pointer;
  }
  
  .switch .slider:before {
    content: "";
    position: absolute;
    width: 14px;
    height: 14px;
    background-color: white;
    border-radius: 50%;
    top: 2px;
    left: 2px;
    transition: transform 0.3s;
  }
  
  .switch input:checked + .slider {
    background-color: #525354;
  }
  
  .switch input:checked + .slider:before {
    transform: translateX(18px);
  }
  
  /* 滑动按钮样式 */
  .slider-group {
    margin-top: 20px;
  }
  
  .slider-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .slider-row span {
    font-size: 12px;
    color: #555;
    white-space: nowrap;
  }
  
  .slider-row input[type="range"] {
    flex: 1;
    max-width: 150px;
    margin: 0 10px;
    appearance: none;
    height: 4px;
    background-color: #ccc;
    border-radius: 2px;
    outline: none;
  }
  
  .slider-row input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 10px;
    height: 10px;
    background-color: #aaaeb2;
    border-radius: 50%;
    cursor: pointer;
  }
  
  .slider-row .value {
    font-size: 12px;
    color: #555;
    width: 30px;
    text-align: center;
  }
  </style>
  