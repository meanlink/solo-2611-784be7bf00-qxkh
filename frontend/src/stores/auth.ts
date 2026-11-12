import { reactive } from "vue";
import { me } from "../api/auth";
import type { User } from "../types";
export const authState = reactive<{user:User|null}>({user:null});
export async function loadUser(){ try { authState.user = await me(); } catch { authState.user = null; } }
