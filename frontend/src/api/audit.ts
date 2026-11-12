import { api } from "./client";
import type { Audit, ListResponse } from "../types";
export const listAudit = () => api<ListResponse<Audit>>("/audit");
