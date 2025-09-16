<script setup>
import { ref, onMounted, computed } from 'vue';
import InteractionModal from './InteractionModal.vue';
import ClueBubble from './ClueBubble.vue';
import ResponsiveCanvas from './ResponsiveCanvas.vue';
import LoadingIndicator from './LoadingIndicator.vue';

// --- Game State Management ---
const gameState = ref(null);
const loading = ref(true);
const loadingMessage = ref(''); // Dedicated state for loading text
const gameMessage = ref(null); // Used for floating notifications, initialized to null
const canvasDimensions = ref({ width: 0, height: 0 });

// --- UI State ---
const showInteractionModal = ref(false);
const interactionTarget = ref(null);
const showRulesPanel = ref(false);
const showScenesPanel = ref(false);

// --- Computed Properties ---
const currentScene = computed(() => gameState.value?.current_map);
const unlockedScenes = computed(() => {
    if (!gameState.value) return {};
    return gameState.value.unlocked_maps;
});
const activeRules = computed(() => gameState.value?.game_rules || []);
const discoveredVictoryClues = computed(() => gameState.value?.discovered_victory_clues || []);

// --- Coordinate & Asset Handling ---
const toPixels = (val, axis) => {
  if (!canvasDimensions.value.width) return 0;
  const base = axis === 'x' ? canvasDimensions.value.width : canvasDimensions.value.height;
  return Math.round(val * base);
};
const getImageUrl = (path) => {
  if (!path) return '';
  // The backend provides paths like "backgrounds/image.png"
  // The frontend serves static assets from /public/assets/
  // So, we just need to prepend /assets/
  return `/assets/${path}`;
};

// --- WebSocket API ---
const clientId = `client_${Math.random().toString(36).substr(2, 9)}`;
const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

const sendMessage = (payload) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  } else {
    console.error("WebSocket is not open.");
  }
};

ws.onopen = () => {
  console.log("WebSocket connection established.");
  initializeGame();
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received game state:', data);

  if (data.status === 'loading') {
    loadingMessage.value = data.message;
  } else if (data.status === 'done' || data.status === 'update') {
    gameState.value = data.gameState;
    if (data.status === 'done') {
      setGameMessage('游戏世界生成成功！');
    } else {
      setGameMessage(data.gameState.story_context?.last_dialogue || '游戏世界已更新！');
    }
    loading.value = false;
  } else if (data.status === 'error') {
    setGameMessage('发生错误: ' + data.message, true);
    loading.value = false;
  }
};

ws.onclose = () => {
  console.log("WebSocket connection closed.");
  setGameMessage('与服务器的连接已断开。', true);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
  setGameMessage('连接发生错误。', true);
};

const initializeGame = () => {
  loading.value = true;
  loadingMessage.value = '正在创建游戏...';
  sendMessage({
    type: 'start_game',
    theme: '古代遗迹',
    difficulty: 2
  });
};

const performInteraction = (target) => {
  loading.value = true;
  const actionPayload = { 
    type: 'interact', 
    target_id: target.id, 
    interaction_type: 'talk',
    details: `与 ${target.name} 互动` 
  };
  sendMessage({
    type: 'player_action',
    session_id: gameState.value.session_id,
    action: actionPayload
  });
};

// --- UI Logic ---
const changeScene = (mapId) => {
  loading.value = true;
  const actionPayload = {
    type: 'move',
    target_map_id: mapId,
    details: `移动到场景: ${mapId}`
  };
  sendMessage({
    type: 'player_action',
    session_id: gameState.value.session_id,
    action: actionPayload
  });
  showScenesPanel.value = false;
};

const handleAssetClick = (asset) => {
  if (asset.interactive) {
    interactionTarget.value = asset;
    showInteractionModal.value = true;
  }
};

let messageTimeout = null;
const setGameMessage = (msg, isError = false) => {
    gameMessage.value = { text: msg, isError };
    clearTimeout(messageTimeout);
    messageTimeout = setTimeout(() => {
        gameMessage.value = null;
    }, 5000);
};

// onMounted will implicitly handle the connection setup via the script setup's top-level code.
// initializeGame is now called by the ws.onopen event handler.
</script>

<template>
  <div class="game-view-wrapper">
    <LoadingIndicator v-if="loading" :message="loadingMessage" />
    
    <template v-if="gameState">
      <header class="game-header">
        <div class="header-title">法则迷宫</div>
        <div class="header-actions">
          <button @click="showScenesPanel = true">切换场景</button>
          <button @click="showRulesPanel = true">查看法则</button>
        </div>
      </header>

      <main class="game-main">
        <ResponsiveCanvas class="scene-display" @update:dimensions="canvasDimensions = $event">
          <transition name="fade" mode="out-in">
            <div
              v-if="currentScene && currentScene.background_image"
              :key="currentScene.name"
              class="scene-background"
              :style="{ backgroundImage: `url(${getImageUrl(currentScene.background_image)})` }"
            >
              <div class="scene-elements">
                <img
                  v-for="(obj, index) in currentScene.objects"
                  :key="`obj-${index}-${obj.name}`"
                  :src="getImageUrl(obj.image)" :alt="obj.name"
                  class="scene-element"
                  :style="{ left: `${toPixels(obj.x, 'x')}px`, top: `${toPixels(obj.y, 'y')}px`, width: `${toPixels(obj.width, 'x')}px`, height: `${toPixels(obj.height, 'y')}px`, transform: `translate(-50%, -50%) rotate(${obj.rotation || 0}deg)` }"
                  @click="handleAssetClick(obj)"
                  :class="{ interactive: obj.interactive }"
                />
                <img
                  v-for="(entity, index) in currentScene.entities"
                  :key="`entity-${index}-${entity.name}`"
                  :src="getImageUrl(entity.image)" :alt="entity.name"
                  class="scene-element"
                  :style="{ left: `${toPixels(entity.x, 'x')}px`, top: `${toPixels(entity.y, 'y')}px`, width: `${toPixels(entity.width, 'x')}px`, height: `${toPixels(entity.height, 'y')}px`, transform: `translate(-50%, -50%) rotate(${entity.rotation || 0}deg)` }"
                  @click="handleAssetClick(entity)"
                  :class="{ interactive: entity.interactive }"
                />
              </div>
            </div>
          </transition>
        </ResponsiveCanvas>
      </main>

      <transition name="fade">
        <div v-if="gameMessage" class="floating-message" :class="{ error: gameMessage.isError }">
          {{ gameMessage.text }}
        </div>
      </transition>

      <!-- Panels as Overlays -->
      <transition name="fade">
        <div v-if="showScenesPanel" class="panel-overlay" @click.self="showScenesPanel = false">
          <div class="panel">
            <h3>切换场景</h3>
            <button v-for="(data, key) in unlockedScenes" :key="key" @click="changeScene(key)" :disabled="gameState.active_scene_key === key">{{ key }}</button>
          </div>
        </div>
      </transition>
      <transition name="fade">
        <div v-if="showRulesPanel" class="panel-overlay" @click.self="showRulesPanel = false">
          <div class="panel">
            <h3>当前法则</h3>
            <ul><li v-for="rule in activeRules" :key="rule">{{ rule }}</li></ul>
          </div>
        </div>
      </transition>

      <InteractionModal :show="showInteractionModal" :target="interactionTarget" @close="showInteractionModal = false" @interact="performInteraction" />
    </template>
  </div>
</template>

<style scoped>
.game-view-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #1a1a2e;
  color: #e0e0e0;
}
.loading-overlay { z-index: 10; /* ... */ }

.game-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #0f3460;
  border-bottom: 2px solid #e94560;
}
.header-title { font-size: 1.5em; font-weight: bold; }
.header-actions button { margin-left: 10px; padding: 8px 12px; }

.game-main {
  flex-grow: 1;
  position: relative; /* Needed for message positioning */
  overflow: hidden; /* Hide anything that might spill out */
}

.scene-display { width: 100%; height: 100%; }
.scene-background { width: 100%; height: 100%; background-size: cover; background-position: center; }
.scene-elements { position: relative; width: 100%; height: 100%; }
.scene-element { position: absolute; object-fit: fill; cursor: default; transition: transform 0.2s ease; }
.scene-element.interactive:hover { transform: scale(1.05) translate(-50%, -50%); cursor: pointer; filter: drop-shadow(0 0 10px #fff); }

.floating-message {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0,0,0,0.8);
  padding: 15px 25px;
  border-radius: 8px;
  border-left: 5px solid #3498db;
  z-index: 5;
  max-width: 80%;
  text-align: center;
}
.floating-message.error {
  border-left-color: #e74c3c;
}

.panel-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0,0,0,0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 20;
}
.panel {
  width: 90%;
  max-width: 500px;
  background-color: #16213e;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e94560;
  box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
}
.panel h3 { 
  margin-top: 0; 
  color: #e94560; 
  border-bottom: 1px solid #e94560;
  padding-bottom: 10px;
}
.panel button { 
  display: block; 
  width: 100%; 
  padding: 12px; 
  margin-top: 10px; 
  background-color: #2c3e50; 
  color: #ecf0f1; 
  border: 1px solid #34495e;
  border-radius: 4px;
  cursor: pointer; 
  transition: background-color 0.2s;
}
.panel button:hover:not(:disabled) {
  background-color: #34495e;
}
.panel button:disabled { 
  background-color: #e94560; 
  color: white;
  cursor: default;
}
.panel ul {
  padding-left: 20px;
  line-height: 1.6;
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
