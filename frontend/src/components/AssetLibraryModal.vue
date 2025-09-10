<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  show: Boolean,
});
const emit = defineEmits(['close']);

const assetTypes = ['backgrounds', 'objects', 'entities'];
const selectedType = ref('backgrounds');
const assets = ref([]);
const fileToUpload = ref(null);

const fetchAssets = async () => {
  try {
    const response = await fetch(`http://localhost:8000/api/assets/list/${selectedType.value}`);
    if (!response.ok) throw new Error('Failed to fetch assets');
    assets.value = await response.json();
  } catch (error) {
    console.error(`Error fetching ${selectedType.value}:`, error);
    alert(`加载 ${selectedType.value} 素材失败。`);
  }
};

const handleFileChange = (event) => {
  fileToUpload.value = event.target.files[0];
};

const uploadAsset = async () => {
  if (!fileToUpload.value) {
    alert('请先选择一个文件。');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileToUpload.value);

  try {
    const response = await fetch(`http://localhost:8000/api/upload/${selectedType.value}`, {
      method: 'POST',
      body: formData,
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Upload failed');
    alert('上传成功！');
    fileToUpload.value = null;
    document.getElementById('file-upload-input').value = '';
    fetchAssets(); // Refresh the list
  } catch (error) {
    console.error('Error uploading file:', error);
    alert(`上传失败: ${error.message}`);
  }
};

const deleteAsset = async (filename) => {
  if (!confirm(`确定要删除文件 "${filename}" 吗？此操作不可撤销。`)) {
    return;
  }

  try {
    const response = await fetch(`http://localhost:8000/api/delete/asset/${selectedType.value}/${filename}`, {
      method: 'DELETE',
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Delete failed');
    alert('删除成功！');
    fetchAssets(); // Refresh the list
  } catch (error) {
    console.error('Error deleting file:', error);
    alert(`删除失败: ${error.message}`);
  }
};

const selectAssetType = (type) => {
  selectedType.value = type;
  fetchAssets();
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
        <div v-for="asset in assets" :key="asset" class="asset-item">
          <img :src="`/assets/${selectedType}/${asset}`" :alt="asset" class="preview-image" />
          <p class="asset-name">{{ asset }}</p>
          <button class="delete-button" @click="deleteAsset(asset)">删除</button>
        </div>
        <p v-if="assets.length === 0">该分类下没有素材。</p>
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
