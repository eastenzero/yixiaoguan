<template>
  <svg 
    viewBox="0 0 24 24" 
    :width="size" 
    :height="size" 
    fill="none" 
    :stroke="color"
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
    :class="customClass"
  >
    <path d="m14 13-7.5 7.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 10" />
    <path d="m16 16 6-6" />
    <path d="m8 8 6-6" />
    <path d="m9 7 8 8" />
    <path d="m21 3-8 8" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 24 },
  color: { type: String, default: 'currentColor' },
  customClass: { type: String, default: '' }
})
</script>
