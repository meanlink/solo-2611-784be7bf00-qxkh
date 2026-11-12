<template><button class="button" :class="{primary}" :disabled="disabled"><slot/></button></template>
<script setup lang="ts">
defineProps<{
  primary?: boolean;
  disabled?: boolean;
}>()
</script>
