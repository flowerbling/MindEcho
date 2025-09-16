<script setup>
defineProps({
  message: {
    type: String,
    default: '正在加载...'
  }
});
</script>

<template>
  <div class="loading-overlay">
    <div class="loading-container">
      <div class="spinner"></div>
      <div class="message">{{ message }}</div>
    </div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 20, 40, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(5px);
}

.loading-container {
  text-align: center;
  color: #e0e0e0;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #e94560;
  animation: spin 1s ease-in-out infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.message {
  font-size: 1.5em;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(233, 69, 96, 0.5);
}
</style>
