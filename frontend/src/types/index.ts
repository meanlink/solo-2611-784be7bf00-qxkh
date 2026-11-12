export type Role = "admin" | "analyst" | "reviewer";
export interface User { id:string; email:string; display_name:string; role:Role }
export interface Workspace { id:string; name:string; client_name:string; context_note:string; }
export interface Dataset { id:string; name:string; source:string; status:string; row_count:number; checksum:string; description:string; workspace_id:string; created_by:string; }
export interface Analysis { id:string; name:string; kind:string; status:string; hypothesis:string; config:Record<string,unknown>; dataset_id:string; workspace_id:string; created_by:string; }
export interface Metric { label:string; value:number|string; unit?:string; tone?:string; }
export interface Series { label:string; value:number; }
export interface RunResult { headline:string; narrative:string; metrics:Metric[]; series:Series[]; table:Record<string,unknown>[]; method:string; caveat:string; }
export interface Run { id:string; status:string; result:RunResult; metrics:Metric[]; error_message:string; checksum:string; analysis_id:string; created_at:string; }
export interface Audit { id:string; action:string; resource_type:string; resource_id:string; actor_id:string; detail:Record<string,unknown>; created_at:string; }
export interface Comment { id:string; body:string; decision:string; run_id:string; author_id:string; created_at:string; }
export interface ListResponse<T> { items:T[]; total:number; }
