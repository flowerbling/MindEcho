<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const canvasRef = ref(null);
const dimensions = ref({ width: 0, height: 0 });

const emit = defineEmits(['update:dimensions']);

let resizeObserver;

onMounted(() => {
  if (canvasRef.value) {
    resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        const { width, height } = entry.contentRect;
        dimensions.value = { width, height };
        emit('update:dimensions', { width, height });
      }
    });
    resizeObserver.observe(canvasRef.value);
  }
});

onUnmounted(() => {
  if (resizeObserver && canvasRef.value) {
    resizeObserver.unobserve(canvasRef.value);
  }
});
</script>

<template>
  <div class="canvas-container">
    <div ref="canvasRef" class="responsive-canvas">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.canvas-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background-color: #111; /* Dark background to frame the canvas */
}

.responsive-canvas {
  position: relative;
  aspect-ratio: 16 / 9;
  width: 100%;
  /* These two rules ensure it fits within the container without distortion */
  max-width: 100%;
  max-height: 100%;
  background-color: #000; /* Fallback color */
}
</style>
