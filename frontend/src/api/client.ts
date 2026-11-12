const TOKEN_KEY = "analytics_token";
export function getToken(){ return localStorage.getItem(TOKEN_KEY); }
export function setToken(token:string){ localStorage.setItem(TOKEN_KEY, token); }
export function clearToken(){ localStorage.removeItem(TOKEN_KEY); }
export async function api<T>(path:string, init:RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`/api${path}`, {...init, headers});
  if (!response.ok) {
    const payload = await response.json().catch(() => ({detail:"请求失败"}));
    throw new Error(payload.detail || "请求失败");
  }
  return response.json();
}
