# 冷链传感器相关室

沧澜冷链（18 座区域仓）的数据分析工作台。药品冷链仓同时采集温度、湿度、门磁和压缩机振动，运维希望定位彼此相关且值得现场排查的传感组合。

## 真实场景

- 当前工作流：值守员每天下载四套网关 CSV，在脚本里算皮尔逊系数，再把可疑组合贴进维修群。
- 痛点：传感器不同步造成伪相关；多重比较未校正；线性系数掩盖单调非线性关系。
- 上游：业务导出、实验室复核或历史归档数据。
- 本系统：统一资产登记、分析编排、Python 计算、结果复核与审计。
- 下游：业务负责人、数据管理员与复核员在周会/评审中使用结果。

## 功能

- 相关态势：核心指标、数据状态与近期运行。
- 传感资产：资产列表、样本量与校验摘要。
- 诊断编排：从资产创建分析方案并触发运行。
- 相关矩阵结果：查看真实 Python 计算结果、方法、限制与表格。
- 治理审计：审计日志、复核意见与角色权限追踪。

## 快速启动

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec backend python -m scripts.seed_demo
```

访问：

- 前端：http://localhost:18201
- 后端接口：http://localhost:19201/api/health
- 数据库映射：localhost:17701

## 演示账号

| 角色 | 邮箱 | 密码 | 权限 |
|---|---|---|---|
| 数据管理员 | admin@batchdemo.dev | Demo123! | 全部页面、创建与运行 |
| 分析员 | analyst@batchdemo.dev | Demo123! | 创建资产、方案与运行 |
| 业务复核员 | reviewer@batchdemo.dev | Demo123! | 只读结果、提交复核意见 |

## 技术栈

| 服务 | 技术 |
|---|---|
| frontend | vue + TypeScript + Vite + Nginx |
| backend | Python 3.11 + FastAPI + SQLAlchemy |
| worker | Celery + Redis |
| db | mysql |
| redis | Redis 7 |

## 枚举位置

- 后端：`backend/src/constants/enums.py`
- 后端业务标签：`backend/src/constants/domain.py`
- 前端：`frontend/src/constants/enums.ts`
- 前端业务标签：`frontend/src/constants/domain.ts`

## 目录

```text
frontend/       # 页面、组件、store、API
backend/        # routes/controllers/services/models/schemas/middlewares
test-artifacts/ # 由批次 QA 放在项目目录之外
```

## 环境变量

见 `.env.example`。`.env` 不提交。接口统一由 Nginx `/api/` 代理。

## 算法口径

Pearson 与 Spearman 双相关分析：后端按输入样本真实计算并返回效应、区间或评分。

Benjamini-Hochberg 多重检验校正：作为第二层诊断；结果、方法和限制同时返回，前端不硬编码图形数据。

## License

MIT
