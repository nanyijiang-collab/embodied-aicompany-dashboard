# 具身智能企业标签体系标准 (SOP)

> 基于《标签逻辑.docx》制定的新增公司打标规范

---

## 一、大脑技术路径 (Brain Architecture)

| 标签 | 技术内涵 | 判断关键词 |
|------|----------|------------|
| `[E2E-VLA]` 端到端视言行 | VLA模型、像素到动作、大模型直连泛化 | "端到端"、"VLA"、"视觉→动作"、"Foundation Model" |
| `[World Model]` 物理世界模型 | 视频预测、因果推理、自监督预训练 | "世界模型"、"物理直觉"、"视频预测"、"因果" |
| `[Hierarchical]` 分层架构 | LLM+MPC、任务规划、原子动作、技能库 | "任务规划"、"分层"、"规则+学习" |
| `[Cross-Embodiment]` 跨本体通用 | 硬件无关、跨平台迁移 | "跨本体"、"通用大脑"、"算法授权" |
| `[IL-Teleop]` 模仿学习 | 遥操作、数据工厂 | "遥操作"、"手把手示教"、"数据工厂" |

---

## 二、训练与数据范式 (Data Paradigm)

| 标签 | 数据逻辑 | 判断关键词 |
|------|----------|------------|
| `[IL-Teleop]` 模仿学习 | 依赖人类操作员 | "遥操作"、"示教"、"熟练工数据" |
| `[Sim2Real-RL]` 仿真强化学习 | 数字孪生、仿真 | "仿真"、"数字孪生"、"Isaac"、"几千万小时" |
| `[Synthetic-Data]` 合成数据 | 靠AI生成训练数据 | "生成式数据"、"Sim-to-Sim"、"数据增强" |

**注意**：IL-Teleop 同时出现在 Brain 和 Training 中

---

## 三、商业场景 (Scenario Labels)

| 标签 | 场景描述 | 判断线索 |
|------|----------|----------|
| `[I-Heavy]` 工业-重工 | 汽车白车身、大型产线 | 车企合作、焊接产线 |
| `[I-Precision]` 工业-精密 | 3C组装线、精密插拔 | 3C、精密装配、螺丝 |
| `[L-Logistics]` 仓储物流 | 货架、拣选、搬运 | "拣选"、"搬运"、"物流" |
| `[S-Commercial]` 商业服务 | 写字楼、商场、语音交互 | "语音交互"、"服务"、"商业" |
| `[C-Home]` 家庭场景 | 家用、家庭陪伴 | "家庭"、"陪伴" |
| `[C-Edu]` 教育场景 | 教育、康复 | "教育"、"康复" |
| `[H-Special]` 特种巡检 | 电力、油气、野外 | "巡检"、"防爆"、"野外" |
| `[Agnostic]` 通用领域 | 无特定场景限制 | "通用"、"全场景" |

---

## 四、核心零部件 (Component Identification)

| 标签 | 零部件描述 | 判断关键词 |
|------|------------|------------|
| `[Dexterous Hand]` 灵巧手 | 多指、高自由度、触觉传感器 | "灵巧手"、"多指"、"触觉" |
| `[Actuator/Joint]` 执行器 | 一体化关节、高扭矩密度 | "一体化关节"、"执行器"、"扭矩" |
| `[Force-Sensor]` 力传感器 | 六维力矩、触觉阵列 | "力传感器"、"六维力"、"力觉" |
| `[Reducer]` 减速器 | 谐波减速器、RV减速器 | "谐波"、"减速器"、"RV" |
| `[AI-Silicon]` 专用芯片 | 端侧算力、推理芯片 | "芯片"、"BPU"、"NPU"、"算力芯片" |

---

## 五、新增公司打标流程

1. **读取定位 (positioning)**：从公司PR/官网提炼核心竞争力描述
2. **判断大脑架构**：对照第一部分，选择最匹配的技术路径
3. **判断训练范式**：对照第二部分，选择数据来源类型
4. **判断商业场景**：对照第三部分，选择应用场景（可多选）
5. **判断零部件**：若是零部件供应商，使用第四部分的专业标签

### 输出格式

```javascript
{ 
  name:"公司名 (英文名)", 
  overseas:true/false, 
  brain:"[标签] 标签名", 
  training:"[标签] 标签名", 
  scene:"[标签] 场景名", 
  positioning:"定位描述" 
}
```

---

## 六、已验证的标签清单（77家公司）

### Brain 标签
```
E2E-VLA, World Model, Hierarchical, Hierarchical/RL, 
Cross-Embodiment, IL-Teleop, Integrated-OEM, 
Platform-Hub, Platform-Infra, Sim2Real-RL, Brain-Vision, Component
```

### Training 标签
```
IL-Teleop, Sim2Real-RL, Synthetic-Data, Real-World-RL, 
Video-Pretrain, VLM-Micro-tuning, Foundation-Scale, 
Heterogeneous-Data, Proprietary-IL, Massive-RL, 
High-Precision-IL, Physical-Sim, Zero-Shot-Sim, 
Digital-Twin, Locomotion-Expert, Scenario-Data, 
Tactile-Focus, Field-RL, Human-to-Robot-IL, 
Force-Centric, Force-Control-IL, Real-World-Transfer, 
Self-Supervised, Algorithm-Bench, Open-Harmony, 
Digit-V3, Locomotion-Data, Car-AI-Transfer, 
Bionic-Logic, Rugged-Environ, 3D-Vision-AI, 
Actuator-Innov, Data-Engine, Industry-Control, 
Chip-Level-Opt, Logistics-SOP, Research-Data, 
Inspection-RL, Small-Model, Industrial-RL, 
Walking-RL, Ecosystem-Data, Elastic-Sensing, 
Gen-Data, General-Data, Hierarchical-VLA, 
High-Dynamic, High-Freq-Loop, High-Speed-Sens, 
Human-Demo, Industry-SOP, Integrated-Design, 
MoCap-Data, Policy-Standard, Power-Density, 
Precision-Trans, Real-World-Data, Sensor-Param, 
Sim2Real-3D, Spec-Actuator, Special-Task, 
System-Opt, Tactile-Brain, Unstructured, VLA-Scaling, 
Virtual-Data
```

### Scene 标签
```
Agnostic, C-Edu, C-Home, Component, H-Special, 
I-Heavy, I-Light, I-Precision, L-Log, L-Logistics, 
Medical, Outdoor, Research, S-Comm, S-Commercial
```

---

*文档更新日期：2026-04-28*
