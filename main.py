import json # Import json for file operations
from fastapi import FastAPI, HTTPException, BackgroundTasks # Removed duplicate import
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware

# 导入新的游戏引擎和模型
from backend.game_engine import GameEngine
from backend.enhanced_models import GameConfig, MapTemplate # Import MapTemplate

# 从环境变量或配置文件中获取API密钥和URL
API_KEY = os.getenv("OPENAI_API_KEY", "sk-XpwEM1Np8oLFlEKB755445CcF06c422290F1D0D6A021977b")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://oneapi.huacemedia.com/v1")

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Assuming your frontend runs on port 5173
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化游戏引擎
game_config = GameConfig()
game_engine = GameEngine(config=game_config, api_key=API_KEY, base_url=BASE_URL)

class NewGameRequest(BaseModel):
    theme: str
    difficulty: int

class PlayerActionRequest(BaseModel):
    session_id: str
    action: Dict[str, Any]

# New request model for saving map templates
class SaveMapTemplateRequest(BaseModel):
    map_template: MapTemplate

from fastapi import WebSocket, WebSocketDisconnect
from backend.connection_manager import manager
import uuid

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            action_type = data.get("type")

            if action_type == "start_game":
                theme = data.get("theme", "古代遗迹")
                difficulty = data.get("difficulty", 2)
                
                # 流式发送加载状态
                async for status in game_engine.start_new_game(theme, difficulty):
                    await manager.send_personal_message(status, client_id)

            elif action_type == "player_action":
                session_id = data.get("session_id")
                action = data.get("action")
                
                if not game_engine.game_session or game_engine.game_session.session_id != session_id:
                    await manager.send_personal_message({"status": "error", "message": "游戏会话不存在"}, client_id)
                    continue

                updated_state = await game_engine.process_player_action(action)
                await manager.send_personal_message({"status": "update", "gameState": updated_state}, client_id)

            elif action_type == "chat_message":
                entity_id = data.get("entity_id")
                message = data.get("message")
                
                if not game_engine.game_session:
                    await manager.send_personal_message({"status": "error", "message": "游戏会话不存在"}, client_id)
                    continue

                updated_state = await game_engine.process_chat_message(entity_id, message)
                await manager.send_personal_message({"status": "update", "gameState": updated_state}, client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f"客户端 #{client_id} 断开连接")
    except Exception as e:
        await manager.send_personal_message({"status": "error", "message": f"发生错误: {str(e)}"}, client_id)
        manager.disconnect(client_id)

@app.get("/game_state/{session_id}")
async def get_game_state(session_id: str):
    """获取当前游戏状态"""
    if not game_engine.game_session or game_engine.game_session.session_id != session_id:
        raise HTTPException(status_code=404, detail="游戏会话不存在")
    
    return game_engine.get_game_state()

@app.get("/assets")
async def get_assets():
    """获取所有游戏资产 (地图, 实体)"""
    if not game_engine.map_manager.map_templates or not game_engine.entity_manager.entity_templates:
        # 确保资产已加载
        game_engine._load_assets()
    
    return {
        "maps": [m.model_dump() for m in game_engine.map_manager.map_templates.values()],
        "entities": [e.model_dump() for e in game_engine.entity_manager.entity_templates.values()]
    }

@app.post("/save_map_template")
async def save_map_template(request: SaveMapTemplateRequest):
    """保存地图模板"""
    try:
        maps_file_path = "backend/assets/maps.json"
        
        # Read existing maps
        if os.path.exists(maps_file_path):
            with open(maps_file_path, "r", encoding="utf-8") as f:
                existing_maps_data = json.load(f)
        else:
            existing_maps_data = []

        # Convert existing maps to MapTemplate objects for easier manipulation
        existing_maps = [MapTemplate(**m) for m in existing_maps_data]

        # Find and update the map, or add if new
        updated = False
        for i, m in enumerate(existing_maps):
            if m.id == request.map_template.id:
                existing_maps[i] = request.map_template
                updated = True
                break
        if not updated:
            existing_maps.append(request.map_template)
        
        # Write updated maps back to file
        with open(maps_file_path, "w", encoding="utf-8") as f:
            json.dump([m.dict() for m in existing_maps], f, indent=2, ensure_ascii=False)
        
        # Reload assets in game engine to reflect changes
        game_engine._load_assets()

        return {"message": f"地图模板 '{request.map_template.name}' 保存成功！"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存地图模板失败: {str(e)}")

@app.get("/")
async def root():
    return {"message": "欢迎来到MindEcho动态游戏引擎"}

# 如果直接运行此文件，启动Uvicorn服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
