<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  show: Boolean,
});
const emit = defineEmits(['close']);

const assetTypes = ['maps', 'entities']; // Adjusted to match backend's /assets response
const selectedType = ref('maps');
const allAssets = ref({ maps: [], entities: [] }); // Store all fetched assets
const displayedAssets = ref([]); // Assets filtered by selectedType
const fileToUpload = ref(null);

const fetchAssets = async () => {
  try {
    const response = await fetch(`http://localhost:8000/assets`);
    if (!response.ok) throw new Error('Failed to fetch assets');
    const data = await response.json();
    allAssets.value.maps = data.maps;
    allAssets.value.entities = data.entities;
    // Filter assets based on selectedType
    displayedAssets.value = allAssets.value[selectedType.value] || [];
  } catch (error) {
    console.error(`Error fetching all assets:`, error);
    alert(`加载素材失败。`);
  }
};

const handleFileChange = (event) => {
  fileToUpload.value = event.target.files[0];
};

const uploadAsset = async () => {
  alert('上传素材功能暂未实现，请联系后端开发人员。');
  // TODO: Implement actual upload functionality via backend API if available
};

const deleteAsset = async (filename) => {
  alert('删除素材功能暂未实现，请联系后端开发人员。');
  // TODO: Implement actual delete functionality via backend API if available
};

const selectAssetType = (type) => {
  selectedType.value = type;
  displayedAssets.value = allAssets.value[selectedType.value] || [];
};

onMounted(() => {
  fetchAssets();
});
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">
      <button class="close-button" @click="emit('close')">×</button>
      <h2>素材库管理</h2>

      <div class="tabs">
        <button
          v-for="type in assetTypes"
          :key="type"
          :class="{ active: selectedType === type }"
          @click="selectAssetType(type)"
        >
          {{ type }}
        </button>
      </div>

      <div class="upload-section">
        <h4>上传新素材到 "{{ selectedType }}"</h4>
        <input type="file" @change="handleFileChange" id="file-upload-input" />
        <button @click="uploadAsset">上传</button>
      </div>

      <div class="asset-grid">
<div v-for="asset in displayedAssets" :key="asset.id" class="asset-item">
<img :src="`/assets/${selectedType === 'maps' ? asset.background_image : asset.image_path}`" :alt="asset.name" class="preview-image" />
          <p class="asset-name">{{ asset.name }}</p>
          <button class="delete-button" @click="deleteAsset(asset.id)">删除</button>
        </div>
        <p v-if="displayedAssets.length === 0">该分类下没有素材。</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background-color: #2c3e50;
  padding: 30px;
  border-radius: 8px;
  width: 80%;
  max-width: 1000px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  position: relative;
}
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}
.tabs button {
  padding: 10px 15px;
  border: 1px solid #555;
  background-color: transparent;
  color: #ccc;
  cursor: pointer;
  border-radius: 4px;
}
.tabs button.active {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}
.upload-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #34495e;
  border-radius: 4px;
}
.upload-section h4 {
  margin-top: 0;
}
.asset-grid {
  flex-grow: 1;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  padding: 10px;
}
.asset-item {
  background-color: #34495e;
  border-radius: 4px;
  padding: 10px;
  text-align: center;
}
.preview-image {
  width: 100%;
  height: 100px;
  object-fit: contain;
  margin-bottom: 10px;
}
.asset-name {
  word-wrap: break-word;
  font-size: 14px;
  color: #ecf0f1;
}
.delete-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}
</style>
