# 🧠 MindEcho - AI 驱动的冒险游戏

MindEcho 是一款由大型语言模型 (LLM) 驱动的动态、故事驱动的冒险游戏。它设有一个 AI 游戏大师，可以为每次游戏生成独特的故事情节、角色和挑战，每次都能创造出全新且身临其境的体验。

## ✨ 项目特色

*   **动态故事生成：** AI 游戏大师根据选定的主题和难度，创建独特的故事情节、胜利条件和游戏规则。
*   **互动对话：** 与 AI 驱动的角色进行实时对话，他们会动态回应你的消息。
*   **可探索的世界：** 在不同场景中穿梭，与物体和角色互动，揭开线索，推进故事。
*   **实时游戏体验：** 游戏使用 WebSockets 实现前端和后端之间的无缝实时通信。
*   **Vue.js 前端：** 使用 Vue 3 和 Vite 构建的响应式现代化用户界面。
*   **FastAPI 后端：** 由 FastAPI 驱动的高性能异步后端。

## 🚀 技术栈

### 后端

*   **Python 3.8+**
*   **FastAPI：** 用于构建高性能的异步 API。
*   **Uvicorn：** 作为 ASGI 服务器运行 FastAPI 应用。
*   **WebSockets：** 用于与客户端进行实时的双向通信。

### 前端

*   **Vue 3：** 用于构建用户界面。
*   **Vite：** 作为前端构建工具。
*   **Vue Router：** 用于客户端路由。

## 📦 安装与设置

### 1. 克隆仓库

```bash
git clone https://github.com/flowerbling/MindEcho.git
cd MindEcho
```

### 2. 后端设置

#### 先决条件

*   Python 3.8 或更高版本
*   一个 OpenAI API 密钥（或兼容的 API 端点）

#### 安装

1.  **创建并激活虚拟环境：**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # 在 Windows 上, 使用 `.venv\Scripts\activate`
    ```

2.  **安装所需包：**

    ```bash
    pip install -r requirements.txt
    ```
    如果 `requirements.txt` 文件不可用，请手动安装包：
    ```bash
    pip install fastapi "uvicorn[standard]" websockets pydantic openai
    ```

3.  **配置您的 API 密钥：**

    设置 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 环境变量。您可以在项目根目录下创建一个 `.env` 文件来完成此操作：

    ```
    OPENAI_API_KEY="your-api-key"
    OPENAI_BASE_URL="your-api-base-url"
    ```

    应用程序将自动加载这些变量。

#### 运行后端

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务器将在 `http://localhost:8000` 上可用。

### 3. 前端设置

#### 先决条件

*   Node.js (推荐 LTS 版本)
*   npm 或 yarn

#### 安装

1.  **导航到前端目录：**

    ```bash
    cd frontend
    ```

2.  **安装依赖：**

    ```bash
    npm install
    ```

#### 运行前端

```bash
npm run dev
```

前端开发服务器将在 `http://localhost:5173` 上可用。

### 4. 开始游戏

打开浏览器并导航到 `http://localhost:5173`。游戏将自动连接到后端并开始新的会话。

## 🛠️ 项目结构

```
MindEcho/
├── backend/
│   ├── assets/
│   │   ├── entities.json       # 实体模板
│   │   └── maps.json           # 地图模板
│   ├── ai_integration.py     # 处理与 LLM 的通信
│   ├── connection_manager.py # 管理 WebSocket 连接
│   ├── game_engine.py        # 核心游戏逻辑
│   ├── enhanced_models.py    # 游戏状态的 Pydantic 模型
│   └── main.py               # FastAPI 应用程序入口
├── frontend/
│   ├── public/
│   │   └── assets/             # 静态资源 (图片等)
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameView.vue    # 主游戏组件
│   │   │   ├── ChatModal.vue   # NPC 聊天界面
│   │   │   └── ...             # 其他 UI 组件
│   │   ├── router/
│   │   │   └── index.js        # Vue Router 配置
│   │   └── App.vue             # 根 Vue 组件
│   └── ...
└── README.md
```

## 🤝 贡献

欢迎贡献！如果您有任何建议或发现任何错误，请随时提出问题或提交拉取请求。
