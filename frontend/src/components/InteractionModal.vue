<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: Boolean,
  target: Object,
});

const emits = defineEmits(['interact', 'close']);

const handleInteract = () => {
  emits('interact', props.target);
  emits('close');
};
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emits('close')">
    <div class="modal-content">
      <h2>与 {{ target?.name }} 互动</h2>
      <p>你想要如何与 {{ target?.name }} 互动？</p>
      <div class="modal-actions">
        <button @click="handleInteract" class="interact-button">互动</button>
        <button @click="emits('close')" class="close-button">取消</button>
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
  max-width: 400px;
  text-align: center;
}

h2 {
  color: #e94560;
  margin-top: 0;
  margin-bottom: 15px;
}

p {
  margin-bottom: 25px;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.interact-button, .close-button {
  padding: 10px 25px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.interact-button {
  background-color: #e94560;
  color: white;
}

.interact-button:hover {
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