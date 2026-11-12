<template><div class="stat"><div class="stat-label">{{label}}</div><div class="stat-value" :class="toneClass(tone)">{{number(value)}}<small v-if="unit" class="muted"> {{unit}}</small></div></div></template>
<script setup lang="ts">
import { number } from "../../utils/format";
import { toneClass } from "../../utils/tone";
defineProps<{
  label: string;
  value: number | string;
  unit?: string;
  tone?: string;
}>()
</script>
