import { api } from "./client";
import type { User } from "../types";
export async function login(email:string,password:string){ return api<{access_token:string}>("/auth/login",{method:"POST",body:JSON.stringify({email,password})}); }
export function me(){ return api<User>("/auth/me"); }
