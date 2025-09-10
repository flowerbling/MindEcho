import { createRouter, createWebHistory } from 'vue-router';
import GameView from '../components/GameView.vue';
import AssetManager from '../components/AssetManager.vue';
import SceneEditor from '../components/SceneEditor.vue';

const routes = [
  {
    path: '/',
    name: 'Game',
    component: GameView,
  },
  {
    path: '/asset-manager',
    name: 'AssetManager',
    component: AssetManager,
  },
  {
    path: '/scene-editor/:sceneName',
    name: 'SceneEditor',
    component: SceneEditor,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
