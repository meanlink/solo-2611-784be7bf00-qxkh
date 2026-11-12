export const number = (value:number|string) => typeof value === "number" ? new Intl.NumberFormat("zh-CN",{maximumFractionDigits:3}).format(value) : value;
export const dateTime = (value:string) => value ? new Intl.DateTimeFormat("zh-CN",{dateStyle:"medium",timeStyle:"short"}).format(new Date(value)) : "—";
export const checksum = (value:string) => value ? `${value.slice(0,8)}…${value.slice(-4)}` : "—";
