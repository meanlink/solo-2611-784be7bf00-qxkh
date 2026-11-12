import { onMounted } from "vue";
import { authState, loadUser } from "../stores/auth";
export function useAuth(){ onMounted(loadUser); return authState; }
