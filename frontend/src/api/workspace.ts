import { api } from "./client";
import type { Workspace } from "../types";
export const getWorkspace = () => api<Workspace>("/workspace");
