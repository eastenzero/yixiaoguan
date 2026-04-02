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
    <circle cx="11" cy="11" r="8" />
    <path d="m21 21-4.3-4.3" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 24 },
  color: { type: String, default: 'currentColor' },
  customClass: { type: String, default: '' }
})
</script>
