import { api } from "./client";
import type { Comment, ListResponse, Run } from "../types";
export const listRuns = () => api<ListResponse<Run>>("/runs");
export const getRun = (id:string) => api<Run>(`/runs/${id}`);
export const listComments = (id:string) => api<Comment[]>(`/runs/${id}/comments`);
export const addComment = (id:string,body:string,decision="pending") => api<Comment>(`/runs/${id}/comments`,{method:"POST",body:JSON.stringify({body,decision})});
