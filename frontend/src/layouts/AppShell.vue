<template><div class="app-shell"><aside class="sidebar"><div class="brand"><div class="brand-mark">Δ</div><div><strong>{{PROJECT_NAME}}</strong><small>{{CLIENT_NAME}}</small></div></div><nav class="nav-list"><RouterLink v-for="item in NAV_ITEMS" :key="item.path" :to="item.path" class="nav-link" active-class="active"><b class="mono">{{item.icon}}</b><span>{{item.label}}</span></RouterLink></nav><div class="sidebar-foot"><div class="user-line"><span>{{auth.user?.display_name||"读取中"}}</span><span class="mono">{{auth.user?ROLES[auth.user.role]:"—"}}</span></div><AppButton @click="logout">退出登录</AppButton></div></aside><main class="main-stage"><RouterView/></main></div></template>
<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from "vue-router";
import { clearToken } from "../api/client";
import { NAV_ITEMS, ROLES } from "../constants/enums";
import { CLIENT_NAME, PROJECT_NAME } from "../constants/domain";
import { useAuth } from "../hooks/useAuth";
import AppButton from "../components/common/AppButton.vue";
const auth = useAuth();
const router = useRouter();
const logout = () => {
  clearToken();
  router.push("/login");
};
</script>
