<template><section class="panel"><div class="panel-head"><h3>{{title}}</h3><slot name="action"/></div><slot/></section></template>
<script setup lang="ts">
defineProps<{
  title: string;
}>()
</script>
