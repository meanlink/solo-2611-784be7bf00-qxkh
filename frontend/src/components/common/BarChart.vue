<template><div v-if="series.length" class="bar-list"><div class="bar-row" v-for="item in series" :key="item.label"><span :title="item.label">{{item.label}}</span><div class="bar-track"><div class="bar-fill" :style="{width:`${Math.max(Math.abs(item.value)/max*100,3)}%`}"/></div><span class="mono">{{number(item.value)}}</span></div></div><div v-else class="empty">当前结果没有可绘制的序列。</div></template>
<script setup lang="ts">
import { computed } from "vue";
import type { Series } from "../../types";
import { number } from "../../utils/format";
const props = defineProps<{
  series: Series[];
}>();
const max = computed(() => Math.max(...props.series.map((item) => Math.abs(item.value)), 1));
</script>
