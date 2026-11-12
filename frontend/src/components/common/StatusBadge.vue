<template><span class="status" :class="negative?'negative':positive?'positive':'neutral'">{{STATUS_LABELS[status]||status}}</span></template>
<script setup lang="ts">
import { computed } from "vue";
import { STATUS_LABELS } from "../../constants/enums";
const props = defineProps<{
  status: string;
}>();
const positive = computed(() => ["ready", "completed"].includes(props.status));
const negative = computed(() => props.status === "failed");
</script>
