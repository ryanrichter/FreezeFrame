<script setup lang="ts">
import Accordion from './components/Accordion.vue'
import type { AccordionItem } from './data/accordion-data'
import { ref } from 'vue'

const videoRef = ref<HTMLVideoElement | null>(null)
const isSleepActive = ref(false)
const accordionData = ref<AccordionItem[]>([])
const loading = ref(false)
const error = ref(false)

const handlePause = async () => {
  if (!videoRef.value) {
    console.error('Video element not found')
    return
  }

  if (isSleepActive.value) {
    console.log('Screenshot is on cooldown. Please wait 5 minutes between screenshots.')
    return
  }

  try {
    const canvas = document.createElement('canvas')
    canvas.width = videoRef.value.videoWidth
    canvas.height = videoRef.value.videoHeight

    const ctx = canvas.getContext('2d')
    if (!ctx) {
      console.error('Could not get canvas context')
      return
    }

    // Draw current frame
    ctx.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height)

    const dataUrl = canvas.toDataURL('image/png')
    const base64Image = dataUrl.split(',')[1]
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const filename = `video-screenshot-${timestamp}.png`

    // Upload to Flask
    console.log('Uploading screenshot...')
    loading.value = true
    const uploadRes = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_data: base64Image,
        filename: filename
      })
    })

    if (!uploadRes.ok) throw new Error('Upload failed')

    // Fetch AI results from /output
    console.log('Fetching AI output...')
    const outputRes = await fetch('http://localhost:5000/output')
    const data = await outputRes.json()

    if (!Array.isArray(data)) {
      throw new Error('Invalid AI response format')
    }

    // Map results into accordion items
    accordionData.value = data.map((item: Omit<AccordionItem, 'id'>, index: number) => ({
      ...item,
      id: index + 1
    }))

    console.log('Accordion data loaded.')

    // Cooldown timer
    isSleepActive.value = true
    setTimeout(() => {
      isSleepActive.value = false
      console.log('Cooldown finished.')
    }, 5 * 60 * 1000) // 5 minutes

  } catch (err) {
    console.error('Error during screenshot/analysis:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app">
    <h1>Fox Freeze Frame</h1>

    <div class="video-container">
      <video 
        ref="videoRef"
        controls
        @pause="handlePause"
        crossorigin="anonymous"
      >
        <source src="/public/videos/Jalen Hurts on Super Bowl loss  you either win or you learn  _ Super Bowl LVII.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>

    <div v-if="isSleepActive" class="cooldown-message">
      Please wait 5 minutes before taking another screenshot.
    </div>

    <div v-if="loading" class="status-message">Analyzing image...</div>
    <div v-if="error" class="status-message error">Failed to process image.</div>

    <Accordion v-if="accordionData.length" :items="accordionData" />
  </div>
</template>

<style scoped>
.app {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.video-container {
  margin-bottom: 2rem;
  width: 100%;
  aspect-ratio: 16/9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.video-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cooldown-message {
  text-align: center;
  color: #ff9800;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: rgba(255, 152, 0, 0.1);
  border-radius: 4px;
}

.status-message {
  text-align: center;
  color: white;
  margin-bottom: 1rem;
  font-weight: bold;
}

.status-message.error {
  color: #ff4c4c;
}
</style>


