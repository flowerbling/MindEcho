from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
from typing import Dict, List
import os
import shutil
import random

from backend.models import PlayerAction, GameStateInput, NewRule, GameStateUpdates, AIResponse, CurrentScene, SceneObject, SceneEntity
from backend.game_logic import game_state, generate_ai_response

app = FastAPI()

# --- Constants ---
ASSET_LIBRARY_FILE = "backend/asset_library.json"
SCENE_LAYOUTS_FILE = "backend/scene_layouts.json"
ASSETS_BASE_DIR = "frontend/public/assets"
BACKGROUNDS_DIR = os.path.join(ASSETS_BASE_DIR, "backgrounds")
OBJECTS_DIR = os.path.join(ASSETS_BASE_DIR, "objects")
ENTITIES_DIR = os.path.join(ASSETS_BASE_DIR, "entities")


# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Ensure asset directories exist ---
os.makedirs(BACKGROUNDS_DIR, exist_ok=True)
os.makedirs(OBJECTS_DIR, exist_ok=True)
os.makedirs(ENTITIES_DIR, exist_ok=True)


# --- Asset Management APIs ---

@app.get("/api/asset_library")
async def get_asset_library():
    try:
        with open(ASSET_LIBRARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Asset library file not found.")

@app.post("/api/asset_library")
async def save_asset_library(library: Dict):
    try:
        with open(ASSET_LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
        return {"message": "Asset library saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scene_layouts")
async def get_scene_layouts():
    try:
        with open(SCENE_LAYOUTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Scene layouts file not found.")

@app.post("/api/scene_layouts")
async def save_scene_layouts(layouts: Dict):
    try:
        with open(SCENE_LAYOUTS_FILE, "w", encoding="utf-8") as f:
            json.dump(layouts, f, indent=2, ensure_ascii=False)
        return {"message": "Scene layouts saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/assets/list/{asset_type}")
async def list_assets(asset_type: str) -> List[str]:
    dir_map = {
        "backgrounds": BACKGROUNDS_DIR,
        "objects": OBJECTS_DIR,
        "entities": ENTITIES_DIR
    }
    target_dir = dir_map.get(asset_type)
    if not target_dir or not os.path.isdir(target_dir):
        raise HTTPException(status_code=404, detail="Invalid asset type.")
    
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.mp4'}
    
    try:
        files = os.listdir(target_dir)
        return [
            f for f in files 
            if os.path.isfile(os.path.join(target_dir, f)) 
            and os.path.splitext(f)[1].lower() in allowed_extensions
            and not f.startswith('.')
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload/{asset_type}")
async def upload_asset(asset_type: str, file: UploadFile = File(...)):
    dir_map = {
        "backgrounds": BACKGROUNDS_DIR,
        "objects": OBJECTS_DIR,
        "entities": ENTITIES_DIR
    }
    upload_dir = dir_map.get(asset_type)
    if not upload_dir:
        raise HTTPException(status_code=400, detail="Invalid asset type for upload.")

    file_path = os.path.join(upload_dir, file.filename)
    
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail=f"File '{file.filename}' already exists.")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"File '{file.filename}' uploaded successfully to {asset_type}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {e}")

@app.delete("/api/delete/asset/{asset_type}/{filename}")
async def delete_asset(asset_type: str, filename: str):
    dir_map = {
        "backgrounds": BACKGROUNDS_DIR,
        "objects": OBJECTS_DIR,
        "entities": ENTITIES_DIR
    }
    target_dir = dir_map.get(asset_type)
    if not target_dir:
        raise HTTPException(status_code=400, detail="Invalid asset type.")

    file_path = os.path.join(target_dir, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        os.remove(file_path)
        return {"message": f"File '{filename}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete file: {e}")


# --- Game Logic APIs ---

def generate_scene_instance(scene_name, scene_layout, library):
    """Helper function to generate a single scene instance."""
    spawned_objects = []
    spawned_entities = []
    subjects_map = {s['name']: s for s in library['subjects']}

    for sp in scene_layout.get("spawn_points", []):
        if not sp.get("subjects_config") or not sp["subjects_config"]:
            continue
        
        chosen_subject_config = random.choice(sp["subjects_config"])
        subject_name = chosen_subject_config["name"]
        
        if subject_name in subjects_map:
            subject_template = subjects_map[subject_name]
            is_entity = 'entities/' in subject_template['file_path']
            
            instance = {
                "name": subject_name,
                "image": subject_template['file_path'],
                "state": "default",
                "x": sp['x'],
                "y": sp['y'],
                "width": chosen_subject_config['width'],
                "height": chosen_subject_config['height'],
                "rotation": chosen_subject_config['rotation'],
                "interactive": True
            }
            
            if is_entity:
                instance["behavior"] = "idle"
                spawned_entities.append(instance)
            else:
                spawned_objects.append(instance)

    return {
        "name": scene_name,
        "background_image": scene_layout["background_image"],
        "description": f"你来到了 {scene_name}。",
        "objects": spawned_objects,
        "entities": spawned_entities
    }

@app.get("/game/init")
async def init_game():
    """
    Initializes a new game world with all scenes pre-generated.
    """
    global game_state

    try:
        with open(SCENE_LAYOUTS_FILE, "r", encoding="utf-8") as f:
            layouts = json.load(f)
        with open(ASSET_LIBRARY_FILE, "r", encoding="utf-8") as f:
            library = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Configuration files not found.")

    if not layouts:
        raise HTTPException(status_code=500, detail="No scenes defined in layouts.")

    # 1. Pre-generate all scenes
    world_scenes = {}
    scene_keys = list(layouts.keys())
    
    for i, scene_name in enumerate(scene_keys):
        scene_layout = layouts[scene_name]
        scene_instance = generate_scene_instance(scene_name, scene_layout, library)
        world_scenes[scene_name] = {
            "unlocked": i == 0,  # Unlock the first scene
            "instance": scene_instance
        }

    # 2. Reset and update the global game state
    game_state = {
        "current_turn": 0,
        "world_scenes": world_scenes,
        "active_scene_key": scene_keys[0], # Set the first scene as active
        "active_rules": ["规则0: 你不能伤害自己。"],
        "discovered_victory_clues": [],
        "hidden_victory_condition": "找到出口",
        "rule_counter": 1,
    }

    return {
        "message": "游戏世界已生成！",
        "initial_state": game_state
    }

@app.post("/game/action")
async def player_action(action: PlayerAction):
    """
    Placeholder for player action. Returns a simple acknowledgement without AI logic.
    """
    global game_state
    
    active_scene = game_state["world_scenes"][game_state["active_scene_key"]]["instance"]
    
    # --- Placeholder Logic ---
    # In this testing phase, we don't call the AI.
    # We just acknowledge the interaction and return the current state.
    ai_mock_response = {
        "thought_process": "AI logic is currently disabled for testing.",
        "ai_response_to_player": f"你与 {action.target} 进行了互动。",
        "new_rule_generated": None,
        "game_state_updates": None
    }

    game_state["current_turn"] += 1

    return {
        "current_turn": game_state["current_turn"],
        "active_scene": active_scene,
        "active_rules": game_state["active_rules"],
        "discovered_victory_clues": game_state["discovered_victory_clues"],
        "ai_response": ai_mock_response
    }

@app.get("/game/state")
async def get_game_state():
    return game_state

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
