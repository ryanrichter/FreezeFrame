<script setup lang="ts">
import { ref } from 'vue'
import type { AccordionItem } from '../data/accordion-data'
import { FontAwesomeIcon } from '../plugins/font-awesome'

// Receive items from App.vue
const props = defineProps<{
  items: AccordionItem[]
}>()

const activeItemId = ref<number | null>(null)

const toggleItem = (id: number) => {
  activeItemId.value = activeItemId.value === id ? null : id
}
</script>

<script lang="ts">
export default {
  name: 'Accordion',
}
</script>

<template>
  <div class="accordion">
    <div v-if="!items.length" class="loading">Waiting for AI results...</div>
    <div v-else>
      <div v-for="item in items" :key="item.id" class="accordion-item">
        <div 
          class="accordion-header"
          :class="{ 'active': activeItemId === item.id }"
          @click="toggleItem(item.id)"
        >
          <div class="product-info">
            <font-awesome-icon :icon="['fas', 'shopping-cart']" class="cart-icon" />
            <span class="product-name">{{ item.product_name }}</span>
          </div>
          <span class="accordion-icon">{{ activeItemId === item.id ? '▲' : '▼' }}</span>
        </div>
        <transition name="slide-up">
          <div class="accordion-data" v-if="activeItemId === item.id">
            <div
              v-for="retailer in item.potential_retailers" 
              :key="retailer"
              class="accordion-content"
            >
              {{ retailer }}
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.accordion {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.accordion-item {
  border-bottom: 1px solid #e0e0e0;
}

.accordion-item:last-child {
  border-bottom: none;
}

.accordion-header {
  padding: 1rem;
  background-color: #000000;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.product-name {
  font-size: 15px;
  font-weight: bold;
  color: white;
}

.accordion-header:hover {
  background-color: #000000;
}

.accordion-header.active {
  background-color: black;
  border-bottom: 1px solid #e0e0e0;
}

.accordion-icon {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.accordion-data {
  background-color: black;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.accordion-content {
  padding: 5px;
  gap: 5px;
  display: flex;
  flex-direction: row;
  background-color: black;
  position: relative;
  z-index: 1;
}

.cart-icon {
  color: white;
  font-size: 1rem;
}

/* Transition animations */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
  max-height: 300px;
}

.slide-up-enter-from,
.slide-up-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.loading {
  color: white;
  text-align: center;
  padding: 1rem;
  font-weight: bold;
}
</style>
