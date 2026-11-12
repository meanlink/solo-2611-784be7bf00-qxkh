<template><div v-if="rows.length" style="overflow-x:auto"><table class="table"><thead><tr><th v-for="column in columns" :key="column">{{column}}</th></tr></thead><tbody><tr v-for="(row,index) in rows.slice(0,20)" :key="index"><td v-for="column in columns" :key="column">{{display(row[column])}}</td></tr></tbody></table></div><div v-else class="empty">暂无明细。检查数据字段后重新运行。</div></template>
<script setup lang="ts">
import { computed } from "vue";
const props = defineProps<{
  rows: Record<string, unknown>[];
}>();
const columns = computed(() => Array.from(new Set(props.rows.flatMap(Object.keys))).slice(0, 8));
const display = (value: unknown) => typeof value === "object" ? JSON.stringify(value) : String(value ?? "—");
</script>
