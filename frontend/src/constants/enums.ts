export const ROLES = { admin: "数据管理员", analyst: "分析员", reviewer: "业务复核员" } as const;
export const STATUS_LABELS: Record<string,string> = { draft:"草稿", ready:"就绪", running:"运行中", completed:"已完成", failed:"失败" };
export const NAV_ITEMS = [
  { path:"/overview", icon:"01", label:"总览" },
  { path:"/datasets", icon:"02", label:"资产" },
  { path:"/analyses", icon:"03", label:"编排" },
  { path:"/governance", icon:"04", label:"治理" },
] as const;
