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
    <rect width="7" height="7" x="3" y="3" rx="1" />
    <rect width="7" height="7" x="14" y="3" rx="1" />
    <rect width="7" height="7" x="14" y="14" rx="1" />
    <rect width="7" height="7" x="3" y="14" rx="1" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 24 },
  color: { type: String, default: 'currentColor' },
  customClass: { type: String, default: '' }
})
</script>
