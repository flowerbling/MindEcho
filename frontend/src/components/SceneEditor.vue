<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ResponsiveCanvas from './ResponsiveCanvas.vue';

const route = useRoute();
const router = useRouter();

// --- Constants ---
const DESIGN_WIDTH = 1920;
const DESIGN_HEIGHT = 1080;

// --- State Management ---
const sceneLayouts = ref(null);
const assetLibrary = ref({ subjects: [] });
const selectedSpawnPoint = ref(null);
const sceneKey = ref(route.params.sceneName);
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });
const canvasDimensions = ref({ width: 0, height: 0 });

// --- Computed Properties ---
const scene = computed(() => sceneLayouts.value?.[sceneKey.value]);
const subjects = computed(() => assetLibrary.value?.subjects || []);

// --- Coordinate Conversion ---
const toPixels = (val, axis) => {
  if (!canvasDimensions.value.width || !canvasDimensions.value.height) return 0;
  const base = axis === 'x' ? canvasDimensions.value.width : canvasDimensions.value.height;
  return Math.round(val * base);
};

const toRelative = (val, axis) => {
  if (!canvasDimensions.value.width || !canvasDimensions.value.height) return 0;
  const base = axis === 'x' ? canvasDimensions.value.width : canvasDimensions.value.height;
  return val / base;
};

// --- API Communication ---
const fetchData = async () => {
  try {
    const [layoutsRes, libraryRes] = await Promise.all([
      fetch('http://localhost:8000/api/scene_layouts'),
      fetch('http://localhost:8000/api/asset_library')
    ]);
    sceneLayouts.value = await layoutsRes.json();
    assetLibrary.value = await libraryRes.json();
    if (!scene.value) {
      alert('场景不存在！');
      router.push('/asset-manager');
    }
  } catch (error) { console.error('Error fetching data:', error); }
};

const saveSceneLayouts = async () => {
  try {
    await fetch('http://localhost:8000/api/scene_layouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sceneLayouts.value),
    });
    alert('场景配置保存成功！');
  } catch (error) { console.error('Error saving scene layouts:', error); alert('保存失败。'); }
};

// --- Spawn Point Management ---
const addSpawnPoint = (event) => {
  if (!scene.value) return;
  const rect = event.currentTarget.getBoundingClientRect();
  const newPoint = {
    id: Date.now(),
    x: toRelative(event.clientX - rect.left, 'x'),
    y: toRelative(event.clientY - rect.top, 'y'),
    width: 100 / DESIGN_WIDTH,
    height: 100 / DESIGN_HEIGHT,
    rotation: 0,
    subjects_config: [],
    previewingSubjectName: null,
  };
  scene.value.spawn_points.push(newPoint);
  selectSpawnPoint(newPoint);
};

const selectSpawnPoint = (point) => { selectedSpawnPoint.value = point; };

const deleteSelectedSpawnPoint = () => {
  if (!selectedSpawnPoint.value || !scene.value) return;
  const index = scene.value.spawn_points.findIndex(p => p.id === selectedSpawnPoint.value.id);
  if (index > -1) scene.value.spawn_points.splice(index, 1);
  selectedSpawnPoint.value = null;
};

// --- Drag and Drop ---
const startDrag = (event, point) => {
  if (point.previewingSubjectName) return;
  event.preventDefault();
  isDragging.value = true;
  selectSpawnPoint(point);
  const rect = event.currentTarget.parentElement.getBoundingClientRect();
  dragOffset.value = {
    x: (event.clientX - rect.left) - toPixels(point.x, 'x'),
    y: (event.clientY - rect.top) - toPixels(point.y, 'y'),
  };
};

const onDrag = (event) => {
  if (isDragging.value && selectedSpawnPoint.value) {
    const rect = event.currentTarget.getBoundingClientRect();
    selectedSpawnPoint.value.x = toRelative((event.clientX - rect.left) - dragOffset.value.x, 'x');
    selectedSpawnPoint.value.y = toRelative((event.clientY - rect.top) - dragOffset.value.y, 'y');
  }
};

const stopDrag = () => { isDragging.value = false; };

// --- Subject Linking & Preview ---
const getSubjectConfig = (point, name) => point.subjects_config?.find(sc => sc.name === name);

const toggleSubjectForSpawnPoint = (point, subjectName) => {
  if (!point.subjects_config) point.subjects_config = [];
  const index = point.subjects_config.findIndex(sc => sc.name === subjectName);
  if (index > -1) {
    point.subjects_config.splice(index, 1);
    if (point.previewingSubjectName === subjectName) point.previewingSubjectName = null;
  } else {
    point.subjects_config.push({ name: subjectName, width: 150 / DESIGN_WIDTH, height: 150 / DESIGN_HEIGHT, rotation: 0 });
  }
};

const togglePreview = (point, subjectConfig) => {
  point.previewingSubjectName = point.previewingSubjectName === subjectConfig.name ? null : subjectConfig.name;
};

const getSubjectFilePath = (name) => assetLibrary.value.subjects.find(s => s.name === name)?.file_path;

onMounted(fetchData);
</script>

<template>
  <div class="scene-editor-layout">
    <ResponsiveCanvas class="scene-canvas" @update:dimensions="canvasDimensions = $event">
      <div
        v-if="scene && scene.background_image"
        class="scene-background"
        :style="{ backgroundImage: `url(/assets/${scene.background_image})` }"
        @click.self="addSpawnPoint"
        @mousemove="onDrag"
        @mouseup="stopDrag"
        @mouseleave="stopDrag"
      >
        <div
          v-for="point in scene.spawn_points"
          :key="point.id"
          class="spawn-point"
          :class="{ selected: selectedSpawnPoint?.id === point.id, 'is-previewing': point.previewingSubjectName }"
          :style="{
            left: `${toPixels(point.x, 'x')}px`,
            top: `${toPixels(point.y, 'y')}px`,
            width: `${toPixels(point.width, 'x')}px`,
            height: `${toPixels(point.height, 'y')}px`,
            transform: `translate(-50%, -50%) rotate(${point.rotation}deg)`
          }"
          @click.stop="selectSpawnPoint(point)"
          @mousedown.prevent.stop="startDrag($event, point)"
        ></div>
        
        <template v-for="point in scene.spawn_points" :key="`preview-${point.id}`">
          <div
            v-if="point.previewingSubjectName"
            class="subject-preview-on-canvas"
            :style="{
              left: `${toPixels(point.x, 'x')}px`,
              top: `${toPixels(point.y, 'y')}px`,
              width: `${toPixels(getSubjectConfig(point, point.previewingSubjectName).width, 'x')}px`,
              height: `${toPixels(getSubjectConfig(point, point.previewingSubjectName).height, 'y')}px`,
              transform: `translate(-50%, -50%) rotate(${getSubjectConfig(point, point.previewingSubjectName).rotation}deg)`
            }"
          >
            <img :src="`/assets/${getSubjectFilePath(point.previewingSubjectName)}`" :alt="point.previewingSubjectName" />
          </div>
        </template>
      </div>
    </ResponsiveCanvas>

    <div class="controls-panel">
      <router-link to="/asset-manager" class="back-button">返回</router-link>
      <h2 v-if="scene">编辑: {{ sceneKey }}</h2>
      <button @click="saveSceneLayouts" class="save-button">保存</button>

      <div v-if="selectedSpawnPoint">
        <h3>刷新点</h3>
        <!-- We show pixel values for intuitive editing, but store relative values -->
        <label>中心X: <input type="number" :value="Math.round(toPixels(selectedSpawnPoint.x, 'x'))" @input="selectedSpawnPoint.x = toRelative($event.target.value, 'x')"></label>
        <label>中心Y: <input type="number" :value="Math.round(toPixels(selectedSpawnPoint.y, 'y'))" @input="selectedSpawnPoint.y = toRelative($event.target.value, 'y')"></label>
        <label>区域宽: <input type="number" :value="Math.round(toPixels(selectedSpawnPoint.width, 'x'))" @input="selectedSpawnPoint.width = toRelative($event.target.value, 'x')"></label>
        <label>区域高: <input type="number" :value="Math.round(toPixels(selectedSpawnPoint.height, 'y'))" @input="selectedSpawnPoint.height = toRelative($event.target.value, 'y')"></label>
        <label>区域角度: <input type="number" v-model="selectedSpawnPoint.rotation"></label>
        
        <h4>可刷新主体</h4>
        <div v-for="subject in subjects" :key="subject.name" class="subject-config-item">
          <div class="subject-main">
            <input type="checkbox" :id="`toggle-${subject.name}`" :checked="!!getSubjectConfig(selectedSpawnPoint, subject.name)" @change="toggleSubjectForSpawnPoint(selectedSpawnPoint, subject.name)"/>
            <img :src="`/assets/${subject.file_path}`" class="subject-preview" :alt="subject.name" />
            <label :for="`toggle-${subject.name}`">{{ subject.name }}</label>
            <button v-if="getSubjectConfig(selectedSpawnPoint, subject.name)" @click="togglePreview(selectedSpawnPoint, getSubjectConfig(selectedSpawnPoint, subject.name))" class="preview-btn">
              {{ selectedSpawnPoint.previewingSubjectName === subject.name ? '取消' : '预览' }}
            </button>
          </div>
          <div v-if="getSubjectConfig(selectedSpawnPoint, subject.name)" class="subject-props">
            <label>宽: <input type="number" :value="Math.round(toPixels(getSubjectConfig(selectedSpawnPoint, subject.name).width, 'x'))" @input="getSubjectConfig(selectedSpawnPoint, subject.name).width = toRelative($event.target.value, 'x')"></label>
            <label>高: <input type="number" :value="Math.round(toPixels(getSubjectConfig(selectedSpawnPoint, subject.name).height, 'y'))" @input="getSubjectConfig(selectedSpawnPoint, subject.name).height = toRelative($event.target.value, 'y')"></label>
            <label>角度: <input type="number" v-model="getSubjectConfig(selectedSpawnPoint, subject.name).rotation"></label>
          </div>
        </div>
        <button @click="deleteSelectedSpawnPoint" class="delete-button">删除刷新点</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Layout */
.scene-editor-layout { display: flex; height: 100vh; font-family: sans-serif; }
.scene-canvas { flex-grow: 1; position: relative; background-color: #2c3e50; }
.controls-panel { width: 350px; padding: 20px; background-color: #f0f2f5; color: #333; overflow-y: auto; }

/* Canvas Elements */
.scene-background { width: 100%; height: 100%; background-size: cover; background-position: center; }
.spawn-point { position: absolute; border: 2px dashed #ff4757; cursor: grab; box-sizing: border-box; }
.spawn-point.selected { border-color: #44bd32; border-style: solid; }
.spawn-point.is-previewing { cursor: not-allowed; border-color: #f39c12; border-style: solid; }
.subject-preview-on-canvas { position: absolute; pointer-events: none; opacity: 0.75; }
.subject-preview-on-canvas img { width: 100%; height: 100%; object-fit: fill; }

/* Control Panel General */
.controls-panel h3, .controls-panel h4 { color: #2c3e50; }
.controls-panel label { display: block; margin-bottom: 5px; font-size: 14px; font-weight: bold; }
.controls-panel input[type="number"] { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.back-button { display: inline-block; margin-bottom: 20px; color: #3498db; text-decoration: none; font-weight: bold; }
.save-button { display: block; width: 100%; padding: 12px; margin-bottom: 20px; background-color: #2ecc71; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
.delete-button { margin-top: 15px; width: 100%; background-color: #e74c3c; color: white; border: none; padding: 10px 12px; cursor: pointer; border-radius: 4px; }

/* Subject Config Specifics */
.subject-config-item { background-color: #e9ecef; padding: 10px; border-radius: 4px; margin-top: 10px; }
.subject-main { display: flex; align-items: center; gap: 10px; }
.subject-preview { width: 40px; height: 40px; object-fit: contain; background-color: #fff; border-radius: 4px; border: 1px solid #ccc; }
.preview-btn { margin-left: auto; padding: 4px 8px; font-size: 12px; background-color: #3498db; color: white; border: none; border-radius: 3px; cursor: pointer; }
.subject-props { margin-top: 10px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.subject-props label { font-size: 12px; }
.subject-props input { padding: 4px; font-size: 12px; }
</style>
