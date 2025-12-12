<template>
  
  <div class="app-container">
    <div class="center-content">
      <h1 class="title">虚实融合系统</h1>
      <div class="main-content">
        <div class="card-container">
          <!-- 左侧卡片：图片 + 按钮 -->
          <div class="card">
            <video controls autoplay muted loop class="card-video">
              <source src="/cover_scene.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <button class="card-button" @click="navigateTo('NVS')">
              数字场景
            </button>
          </div>

          <!-- 中间卡片：视频 + 按钮 -->
          <div class="card">
            <video controls autoplay muted loop class="card-video">
              <source src="/cover_human.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <button class="card-button" @click="navigateTo('body-avatar')">
              数字人
            </button>
          </div>

          <!-- 右侧卡片：图片 + 按钮 -->
          <div class="card">
            <video controls autoplay muted loop class="card-video">
              <source src="/cover_vs1.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <button class="card-button" @click="navigateTo('reality')">
              虚实融合
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      title: "Digital Human System",
      previewButtons: ["Actor Video", "Pose Sequence", "Scene Preview", "Light Preview"],
    };
  },
  methods: {
    navigateTo(routeName) {
      // 使用 Vue Router 的 push 方法跳转到指定页面
      this.$router.push({ name: routeName });
    },
  },
};
</script>


<style scoped>
.app-container {
  display: flex;
  min-width: 100vw;  /* 让容器的宽度等于浏览器的宽度 */
  height: 100vh; /* 让容器的高度等于浏览器的高度 */
  justify-content : space-around;
  align-items: center;
  background-image: url('/background.png');
  background-size: cover;
  background-position: center;

}

.center-content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height:100%;
  width:60%;
  background-color: rgb(180, 180, 180);
}
.main-content {
  display: flex;
  flex-direction: column;
  width: 90%;
  height:100%;
  padding: 0px;
  background-color: rgb(180, 180, 180);
  border: 1px solid rgb(190, 192, 194);  /* 设置边框 */
  border-radius: 15px;  /* 设置圆角半径 */
}

.main-content h1 {
    text-align: center;  /* 水平居中h3 */
    
}

.card-container {
    display: flex;
    height:90%;
    width:100%;
    gap: 20px;
    justify-content: space-between;
    flex-wrap: nonwrap;
    
  }
  
  .card {
    display: flex;
    height:100%;
    width: 30%;
    flex-direction: column;
    align-items: center;
    background-color: rgb(180, 180, 180);
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);

  }
  
  .card-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }
  
  .card-video {
    width: 100%;
    height: 100%;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    object-fit: cover;
  }
  
  .card-button {
    padding: 10px;
    font-size: 16px;
    font-weight: bold;
    background-color: #fdfdfd;
    color: rgb(13, 13, 13);
    border: none;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    text-align: center;
    margin-top: 10px;
  }
  
  .card-button:hover {
    background-color: #ccc;
  }
</style>
