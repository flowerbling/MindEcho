<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AssetLibraryModal from './AssetLibraryModal.vue';

const router = useRouter();
const sceneLayouts = ref({}); // This will store the maps fetched from the backend
const showAssetLibrary = ref(false);

const fetchSceneLayouts = async () => {
  try {
    const response = await fetch('http://localhost:8000/assets');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    // Convert the array of maps into an object keyed by map.id for easier lookup
    sceneLayouts.value = data.maps.reduce((acc, map) => {
      acc[map.id] = map;
      return acc;
    }, {});
  } catch (error) {
    console.error('Error fetching scene layouts:', error);
  }
};

const editScene = (sceneName) => {
  router.push({ name: 'SceneEditor', params: { sn: sceneName } });
};

const addNewScene = () => {
  alert('新建场景功能暂未实现，请联系后端开发人员。');
  // TODO: Implement actual add new scene functionality via backend API if available
};

const deleteScene = (sceneName) => {
  alert('删除场景功能暂未实现，请联系后端开发人员。');
  // TODO: Implement actual delete scene functionality via backend API if available
};


onMounted(fetchSceneLayouts);
</script>

<template>
  <div class="manager-container">
    <div class="manager-header">
      <h1>素材与场景管理</h1>
      <div class="actions">
        <button @click="showAssetLibrary = true">打开素材库</button>
        <button @click="addNewScene">新建场景</button>
      </div>
    </div>

    <div class="scene-list">
      <div v-for="(scene, name) in sceneLayouts" :key="name" class="scene-card">
<img :src="scene.background_image ? `/assets/${scene.background_image}` : '/assets/placeholder.png'" class="scene-thumbnail" alt="Scene preview"/>
        <div class="scene-info">
<h3>{{ scene.name }}</h3>
          <p>{{ scene.spawn_points?.length || 0 }} 个刷新点</p>
        </div>
        <div class="scene-actions">
          <button @click="editScene(name)" class="edit-btn">编辑</button>
          <button @click="deleteScene(name)" class="delete-btn">删除</button>
        </div>
      </div>
    </div>

    <AssetLibraryModal :show="showAssetLibrary" @close="showAssetLibrary = false" />
  </div>
</template>

<style scoped>
.manager-container {
  padding: 40px;
  width: 100%;
  height: 100vh;
  box-sizing: border-box;
}
.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  border-bottom: 1px solid #444;
  padding-bottom: 20px;
}
.manager-header h1 {
  color: #ecf0f1;
}
.actions button {
  margin-left: 15px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.scene-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}
.scene-card {
  background-color: #2c3e50;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.scene-thumbnail {
  width: 100%;
  height: 180px;
  object-fit: cover;
  background-color: #34495e;
}
.scene-info {
  padding: 20px;
  flex-grow: 1;
}
.scene-info h3 {
  margin-top: 0;
}
.scene-actions {
  display: flex;
  justify-content: flex-end;
  padding: 10px 20px;
  background-color: #34495e;
}
.scene-actions button {
  margin-left: 10px;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.edit-btn {
  background-color: #2ecc71;
  color: white;
}
.delete-btn {
    background-color: #e74c3c;
    color: white;
}
</style>
