# Spring Boot DolphinScheduler

DolphinScheduler（海豚调度）是一个分布式、易扩展的可视化 DAG 工作流任务调度系统。

## 适用场景

- 数据管道：ETL 数据处理、数据同步、数据清洗。
- 定时作业：报表生成、机器学习模型训练、日志分析。
- 复杂依赖任务：需要严格顺序执行或条件分支的任务流。
- 多云/混合云环境：支持跨集群任务调度（如 Kubernetes、YARN）

## 核心概念

1. 工作流定义: 工作流的静态模板，用于描述任务的组成和依赖关系（DAG 结构）
2. 工作流实例: 工作流定义的一次具体运行（动态执行记录）
3. 任务实例: 工作流中每个任务节点的具体运行记录

## 接口地址
1. 登录页面 `http://localhost:12345/dolphinscheduler/ui/view/login/index.html`
2. API文档地址 `http://localhost:12345/dolphinscheduler/doc.html`

## Spring Boot 集成
