<template>
    <div class="category">
      <div class="uptitle">
        <h2>{{ category.title }}</h2>
      </div>
      <div class="buttons">
        <button
          v-for="button in category.buttons"
          :key="button.name || button"
          class="button"
          @click="handleClick(button.path || button)"
        >
          {{ button.name || button }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      category: {
        type: Object,
        required: true, // 每个分类的数据
      },
    },
    methods: {
      handleClick(path) {
        this.$emit("button-click", path); // 向父组件传递按钮点击的事件
      },
    },
  };
  </script>
  
  <style scoped>
  .category {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 20px;
    justify-content: center;
    align-items: center;
  }
  
  .uptitle {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    width: 85%;
    height: 50%;
    background-color: rgb(165, 171, 178);
    border-radius: 12px;
    margin-top: 10px;
  }
  
  .uptitle h2 {
    font-size: 16px;
  }
  
  .buttons {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    align-items: center;
    justify-content: center;
  }
  
  .category button {
    padding: 10px;
    margin: 5px;
    width: 40%;
    height: 40px;
    background-color: #fdfdfd;
    border: 1px solid #e0e0e0;
    border-radius: 15px;
    cursor: pointer;
  }
  
  .category button:hover {
    background-color: #f0f0f0;
    border-color: #bbb;
  }
  </style>
  