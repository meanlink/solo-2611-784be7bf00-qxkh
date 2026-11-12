import { api } from "./client";
import type { Dataset, ListResponse } from "../types";
export const listDatasets = () => api<ListResponse<Dataset>>("/datasets");
