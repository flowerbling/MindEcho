<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  clues: Array,
});

const emits = defineEmits(['toggle']);
</script>

<template>
  <div class="clue-bubble-container" @click="emits('toggle')">
    <div class="clue-bubble">
      <span class="clue-icon">?</span>
      <span class="clue-count">{{ clues.length }}</span>
    </div>
  </div>
</template>

<style scoped>
.clue-bubble-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
  cursor: pointer;
}

.clue-bubble {
  position: relative;
  width: 50px;
  height: 50px;
  background-color: #e94560;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.clue-bubble:hover {
  transform: scale(1.1);
}

.clue-icon {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.clue-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #16213e;
  color: white;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-weight: bold;
  border: 2px solid #e94560;
}
</style>