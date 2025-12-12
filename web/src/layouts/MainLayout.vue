<template>
  <div class="main-layout">
    <Sidebar />
    <main class="content-area">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue';
</script>

<style scoped>
.main-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-app);
}

.content-area {
  flex: 1;
  overflow-y: auto;
  background-color: var(--bg-app);
  background-image: radial-gradient(circle at top right, rgba(139, 92, 246, 0.05), transparent 40%);
  padding: 32px;
  color: var(--text-main);
}

/* Custom Scrollbar */
.content-area::-webkit-scrollbar {
  width: 8px;
}

.content-area::-webkit-scrollbar-track {
  background: var(--bg-app);
}

.content-area::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.content-area::-webkit-scrollbar-thumb:hover {
  background: var(--text-dim);
}
</style>
