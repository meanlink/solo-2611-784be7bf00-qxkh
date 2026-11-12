import { api } from "./client";
import type { Analysis, ListResponse, Run } from "../types";
export const listAnalyses = () => api<ListResponse<Analysis>>("/analyses");
export const createAnalysis = (payload:{name:string;dataset_id:string;kind:string;hypothesis:string;config:Record<string,unknown>}) => api<Analysis>("/analyses",{method:"POST",body:JSON.stringify(payload)});
export const executeAnalysis = (id:string) => api<Run>(`/analyses/${id}/run`,{method:"POST"});
