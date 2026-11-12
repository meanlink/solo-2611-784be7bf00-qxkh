import { reactive } from "vue";
export function useAsync<T>(loader:()=>Promise<T>) {
  const state = reactive({
    data: null,
    error: "",
    loading: true,
    reload: async () => {
      state.loading = true;
      state.error = "";
      try {
        state.data = (await loader()) as never;
      } catch (error) {
        state.error = (error as Error).message;
      } finally {
        state.loading = false;
      }
    }
  }) as unknown as {
    data: T | null;
    error: string;
    loading: boolean;
    reload: () => Promise<void>;
  };
  state.reload();
  return state;
}
