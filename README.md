# 🧠 MindEcho - AI-Powered Adventure Game

MindEcho is a dynamic, story-driven adventure game powered by a large language model (LLM). It features an AI Game Master that generates a unique storyline, characters, and challenges for each playthrough, creating a new and immersive experience every time.

## ✨ Project Features

*   **Dynamic Story Generation:** The AI Game Master creates a unique storyline, victory conditions, and game rules based on a selected theme and difficulty.
*   **Interactive Dialogue:** Engage in real-time conversations with AI-powered characters who respond dynamically to your messages.
*   **Explorable Worlds:** Navigate through different scenes and interact with objects and characters to uncover clues and advance the story.
*   **Real-time Gameplay:** The game uses WebSockets for seamless, real-time communication between the frontend and the backend.
*   **Vue.js Frontend:** A responsive and modern user interface built with Vue 3 and Vite.
*   **FastAPI Backend:** A high-performance, asynchronous backend powered by FastAPI.

## 🚀 Technology Stack

### Backend

*   **Python 3.8+**
*   **FastAPI:** For building high-performance, asynchronous APIs.
*   **Uvicorn:** As an ASGI server for running the FastAPI application.
*   **WebSockets:** For real-time, bidirectional communication with the client.

### Frontend

*   **Vue 3:** For building the user interface.
*   **Vite:** As the frontend build tool.
*   **Vue Router:** For client-side routing.

## 📦 Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/flowerbling/MindEcho.git
cd MindEcho
```

### 2. Backend Setup

#### Prerequisites

*   Python 3.8 or higher
*   An OpenAI API key (or a compatible API endpoint)

#### Installation

1.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```
    If a `requirements.txt` file is not available, install the packages manually:
    ```bash
    pip install fastapi "uvicorn[standard]" websockets pydantic openai
    ```

3.  **Configure your API key:**

    Set the `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables. You can do this by creating a `.env` file in the root of the project:

    ```
    OPENAI_API_KEY="your-api-key"
    OPENAI_BASE_URL="your-api-base-url"
    ```

    The application will automatically load these variables.

#### Running the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend server will be available at `http://localhost:8000`.

### 3. Frontend Setup

#### Prerequisites

*   Node.js (LTS version recommended)
*   npm or yarn

#### Installation

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install the dependencies:**

    ```bash
    npm install
    ```

#### Running the Frontend

```bash
npm run dev
```

The frontend development server will be available at `http://localhost:5173`.

### 4. Playing the Game

Open your browser and navigate to `http://localhost:5173`. The game will automatically connect to the backend and start a new session.

## 🛠️ Project Structure

```
MindEcho/
├── backend/
│   ├── assets/
│   │   ├── entities.json       # Entity templates
│   │   └── maps.json           # Map templates
│   ├── ai_integration.py     # Handles communication with the LLM
│   ├── connection_manager.py # Manages WebSocket connections
│   ├── game_engine.py        # Core game logic
│   ├── enhanced_models.py    # Pydantic models for the game state
│   └── main.py               # FastAPI application entry point
├── frontend/
│   ├── public/
│   │   └── assets/             # Static assets (images, etc.)
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameView.vue    # Main game component
│   │   │   ├── ChatModal.vue   # Chat interface for NPCs
│   │   │   └── ...             # Other UI components
│   │   ├── router/
│   │   │   └── index.js        # Vue Router configuration
│   │   └── App.vue             # Root Vue component
│   └── ...
└── README.md
```

## 🤝 Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.
