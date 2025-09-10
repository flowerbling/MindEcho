# 🎮 法则迷宫 (The Labyrinth of Laws) - 素材管理与游戏框架

大模型完成规则怪谈游戏。这是一个用于开发“法则迷宫”游戏的素材管理界面和基础游戏框架。它允许开发者通过可视化的方式配置游戏场景、管理素材，并提供了一个响应式的游戏游玩界面。

## ✨ 项目特性

*   **素材库管理：** 统一管理游戏中的背景、物体和实体图片素材，支持上传、预览和删除。
*   **多场景编辑：** 为不同的游戏场景（背景）独立配置刷新点，每个刷新点可关联多个可刷新的主体。
*   **精细化配置：** 支持为刷新点区域设置独立的宽高、角度，并为每个刷新点内的可刷新主体设置独立的生成宽高和角度。
*   **实时预览：** 在场景编辑器中，可手动开启刷新点内主体的实时预览，直观调整布局。
*   **响应式布局：** 游戏和编辑器界面均采用 16:9 比例的响应式设计，确保在不同设备和屏幕尺寸下都能保持一致的视觉效果。
*   **态游戏世界：** 游戏启动时，后端会根据配置随机生成一个包含多个场景的游戏世界，并允许玩家在已解锁的场景间切换。

## 🚀 技术栈

### 后端 (Backend)

*   **Python:** 主要开发语言。
*   **FastAPI:** 用于构建高性能的异步 API 服务。
*   **Uvicorn:** ASGI 服务器，用于运行 FastAPI 应用。
*   **JSON:** 用于存储游戏场景布局和素材库配置。
*   **文件系统操作:** 用于处理素材文件的上传和删除。

### 前端 (Frontend)

*   **Vue 3:** 渐进式 JavaScript 框架，用于构建用户界面。
*   **Vite:** 极速的下一代前端工具。
*   **Vue Router:** 用于前端路由管理，实现页面导航。
*   **CSS (Scoped):** 用于组件样式，确保样式隔离。
*   **JavaScript (ESNext):** 客户端逻辑。

## 📦 部署与运行

### 1. 克隆项目

```bash
git clone [你的项目仓库地址]
cd MindEcho
```

### 2. 后端部署

#### 环境准备

确保你安装了 Python 3.8+ 和 `pip`。

```bash
# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装后端依赖
pip install -r requirements.txt # 如果有 requirements.txt
# 或者手动安装：
# pip install fastapi uvicorn python-multipart
```

#### 运行后端服务

```bash
# 在项目根目录运行
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 `http://localhost:8000` 运行。

### 3. 前端部署

#### 环境准备

确保你安装了 Node.js (推荐 LTS 版本) 和 npm 或 yarn。

```bash
# 进入前端目录
cd frontend

# 安装前端依赖
npm install # 或者 yarn install
```

#### 运行前端开发服务器

```bash
# 在 frontend 目录运行
npm run dev # 或者 yarn dev
```

前端开发服务器通常会在 `http://localhost:5173` 运行。

### 4. 访问应用

*   **素材管理界面：** 打开浏览器访问 `http://localhost:5173/asset-manager`
*   **游戏游玩界面：** 打开浏览器访问 `http://localhost:5173/`

确保后端服务 (`http://localhost:8000`) 正在运行，否则前端将无法获取数据。

## 🛠️ 开发指南

### 文件结构

```
MindEcho/
├── backend/
│   ├── asset_library.json      # 全局素材库配置 (背景图列表, 主体/实体定义)
│   ├── scene_layouts.json      # 场景布局配置 (每个场景的背景图路径, 刷新点配置)
│   ├── game_logic.py           # 游戏核心逻辑 (AI规则生成, 状态更新等)
│   ├── models.py               # Pydantic 模型定义
│   └── main.py                 # FastAPI 后端主入口, API定义
├── frontend/
│   ├── public/
│   │   └── assets/             # 静态素材文件 (图片等)
│   │       ├── backgrounds/
│   │       ├── objects/
│   │       └── entities/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssetManager.vue        # 素材管理主页 (场景列表, 打开素材库)
│   │   │   ├── AssetLibraryModal.vue   # 素材库管理模态框 (上传, 删除, 预览)
│   │   │   ├── SceneEditor.vue         # 单场景编辑器 (刷新点配置, 预览)
│   │   │   ├── ResponsiveCanvas.vue    # 响应式画布核心组件
│   │   │   └── GameView.vue            # 游戏游玩界面
│   │   ├── router/
│   │   │   └── index.js                # Vue Router 配置
│   │   └── App.vue                     # Vue 根组件
│   └── ... (其他 Vite/Vue 相关文件)
├── migration_script.py         # 用于将旧的像素坐标转换为相对坐标的迁移脚本
└── README.md                   # 项目说明文档
```

### 后端 API 概览

*   `GET /api/asset_library`: 获取全局素材库配置。
*   `POST /api/asset_library`: 保存全局素材库配置。
*   `GET /api/scene_layouts`: 获取所有场景布局配置。
*   `POST /api/scene_layouts`: 保存所有场景布局配置。
*   `GET /api/assets/list/{asset_type}`: 获取指定类型（`backgrounds`, `objects`, `entities`）的素材文件列表。
*   `POST /api/upload/{asset_type}`: 上传素材文件。
*   `DELETE /api/delete/asset/{asset_type}/{filename}`: 删除素材文件。
*   `GET /game/init`: 初始化游戏世界，返回包含所有预生成场景的初始状态。
*   `POST /game/action`: 玩家执行动作（目前为测试模式，不触发AI逻辑）。
*   `GET /game/state`: 获取当前游戏状态。

## 🤝 贡献

欢迎对项目进行贡献！如果您有任何建议或发现Bug，请随时提出。
