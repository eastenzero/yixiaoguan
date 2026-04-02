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
    <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 24 },
  color: { type: String, default: 'currentColor' },
  customClass: { type: String, default: '' }
})
</script>
