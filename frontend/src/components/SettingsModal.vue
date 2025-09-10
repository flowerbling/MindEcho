<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: Boolean,
  apiKey: String,
  apiBaseUrl: String,
});

const emits = defineEmits(['update:apiKey', 'update:apiBaseUrl', 'close']);

const localApiKey = ref(props.apiKey);
const localApiBaseUrl = ref(props.apiBaseUrl);

const saveSettings = () => {
  emits('update:apiKey', localApiKey.value);
  emits('update:apiBaseUrl', localApiBaseUrl.value);
  emits('close');
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emits('close')">
    <div class="modal-content">
      <h2>设置</h2>
      <div class="config-item">
        <label for="apiKey">API KEY:</label>
        <input type="password" id="apiKey" v-model="localApiKey" placeholder="您的 API Key" />
      </div>
      <div class="config-item">
        <label for="apiBaseUrl">API Base URL:</label>
        <input type="text" id="apiBaseUrl" v-model="localApiBaseUrl" placeholder="http://localhost:8000" />
      </div>
      <div class="modal-actions">
        <button @click="saveSettings" class="save-button">保存</button>
        <button @click="emits('close')" class="close-button">关闭</button>
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
  background-color: #1a1a2e;
  padding: 30px;
  border-radius: 10px;
  border: 1px solid #0f3460;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  width: 90%;
  max-width: 500px;
}

h2 {
  color: #e94560;
  margin-top: 0;
  margin-bottom: 20px;
}

.config-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.config-item label {
  margin-bottom: 5px;
  color: #a0a0a0;
}

.config-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #0f3460;
  border-radius: 5px;
  background-color: #16213e;
  color: #e0e0e0;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.save-button, .close-button {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button {
  background-color: #e94560;
  color: white;
}

.save-button:hover {
  background-color: #ff6b81;
}

.close-button {
  background-color: #16213e;
  color: #e0e0e0;
  border: 1px solid #0f3460;
}

.close-button:hover {
  background-color: #0f3460;
}
</style>