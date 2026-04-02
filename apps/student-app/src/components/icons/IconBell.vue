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
    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 24 },
  color: { type: String, default: 'currentColor' },
  customClass: { type: String, default: '' }
})
</script>
