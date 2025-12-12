import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from './layouts/MainLayout.vue';
import HomeView from './views/HomeView.vue';
import DataView from './views/DataView.vue';
import TaskView from './views/TaskView.vue';
import EditorView from './views/EditorView.vue';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: HomeView
      },
      {
        path: 'data',
        name: 'Data',
        component: DataView
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: TaskView
      },
      {
        path: 'editor',
        name: 'Editor',
        component: EditorView
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
