<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ entity.name }}</h2>
        <button @click="close" class="close-button">&times;</button>
      </div>
      <div class="modal-body">
        <div class="entity-info">
          <img :src="getImageUrl(entity.image)" :alt="entity.name" class="entity-image" />
          <p class="story-background">{{ entity.story_background }}</p>
        </div>
        <div class="chat-history" ref="chatHistory">
          <div v-for="(message, index) in entity.chat_history" :key="index" class="chat-message" :class="message.sender">
            <p>{{ message.message }}</p>
          </div>
        </div>
        <div class="chat-input">
          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  show: Boolean,
  entity: Object,
});

const emit = defineEmits(['close', 'send-message']);

const newMessage = ref('');
const chatHistory = ref(null);

const close = () => {
  emit('close');
};

const sendMessage = () => {
  if (newMessage.value.trim()) {
    emit('send-message', { entityId: props.entity.id, message: newMessage.value });
    newMessage.value = '';
  }
};

const getImageUrl = (path) => {
  if (!path) return '';
  return `/assets/${path}`;
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatHistory.value) {
      chatHistory.value.scrollTop = chatHistory.value.scrollHeight;
    }
  });
};

watch(() => props.entity, (newEntity) => {
  if (newEntity && newEntity.chat_history) {
    scrollToBottom();
  }
}, { deep: true });

watch(() => props.show, (newVal) => {
  if (newVal) {
    scrollToBottom();
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #2c2c2c;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  width: 90%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #444;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.4em;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.8em;
  cursor: pointer;
  color: #aaa;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.entity-info {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #444;
  padding-bottom: 15px;
}

.entity-image {
  width: 120px;
  height: 160px;
  object-fit: cover;
  border-radius: 8px;
  margin-right: 20px;
  border: 2px solid #555;
  flex-shrink: 0;
}

.story-background {
  font-size: 0.95em;
  color: #ccc;
  line-height: 1.5;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  padding-right: 10px;
  max-height: 300px;
}

.chat-message {
  margin-bottom: 12px;
  padding: 10px 15px;
  border-radius: 18px;
  max-width: 80%;
  line-height: 1.4;
}

.chat-message.player {
  background-color: #007bff;
  color: white;
  align-self: flex-end;
  margin-left: auto;
}

.chat-message.npc {
  background-color: #4a4a4a;
  color: #e0e0e0;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  margin-top: auto;
}

.chat-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #555;
  border-radius: 20px;
  background-color: #333;
  color: #e0e0e0;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 20px;
  cursor: pointer;
}
</style>
