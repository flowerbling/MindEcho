<template>
  <div v-if="show" class="debug-panel">
    <h3>Debug Information</h3>
    <pre>{{ formattedData }}</pre>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  gameData: {
    type: Object,
    default: () => null,
  },
});

const formattedData = computed(() => {
  return JSON.stringify(props.gameData, null, 2);
});
</script>

<style scoped>
.debug-panel {
  position: absolute;
  top: 60px; /* Adjusted to not overlap the header */
  right: 10px;
  background-color: rgba(0, 0, 0, 0.8);
  color: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #444;
  max-width: 450px;
  max-height: calc(100vh - 80px);
  overflow: auto;
  z-index: 1000;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.85em;
}
h3 {
  margin-top: 0;
  color: #e94560;
  border-bottom: 1px solid #e94560;
  padding-bottom: 10px;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
