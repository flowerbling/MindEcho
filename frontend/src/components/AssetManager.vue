<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AssetLibraryModal from './AssetLibraryModal.vue';

const router = useRouter();
const sceneLayouts = ref({});
const showAssetLibrary = ref(false);

const fetchSceneLayouts = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/scene_layouts');
    sceneLayouts.value = await response.json();
  } catch (error) {
    console.error('Error fetching scene layouts:', error);
  }
};

const editScene = (sceneName) => {
  router.push({ name: 'SceneEditor', params: { sn: sceneName } });
};

const addNewScene = () => {
  const newSceneName = prompt('请输入新场景的名称:', `scene_${Object.keys(sceneLayouts.value).length + 1}`);
  if (newSceneName && !sceneLayouts.value[newSceneName]) {
    sceneLayouts.value[newSceneName] = {
      background_image: "", // User should set this in the editor
      spawn_points: []
    };
    // Immediately save the new scene structure
    saveSceneLayouts();
  } else if (newSceneName) {
    alert('场景名称已存在！');
  }
};

const deleteScene = (sceneName) => {
    if (confirm(`确定要删除场景 "${sceneName}" 吗？此操作将删除其所有配置。`)) {
        delete sceneLayouts.value[sceneName];
        saveSceneLayouts();
    }
}

const saveSceneLayouts = async () => {
  try {
    await fetch('http://localhost:8000/api/scene_layouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sceneLayouts.value),
    });
    // No alert needed for background saves, or could be a subtle notification
  } catch (error) {
    console.error('Error saving scene layouts:', error);
    alert('自动保存新场景失败。');
  }
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
          <h3>{{ name }}</h3>
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
