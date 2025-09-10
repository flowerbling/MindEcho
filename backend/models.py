from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PlayerAction(BaseModel):
    type: str # "Observe", "Move", "Interact", "Declare", "Challenge"
    target: Optional[str] = None
    details: Optional[str] = None

class SceneObject(BaseModel):
    name: str
    image: str # Path to the image, e.g., "objects/crystal_inactive.png"
    state: str # e.g., "未激活", "已激活"
    x: int # X coordinate for positioning
    y: int # Y coordinate for positioning
    width: int = 100 # Default width
    height: int = 100 # Default height
    interactive: bool = True

class SceneEntity(BaseModel):
    name: str
    image: str # Path to the image, e.g., "entities/guard_patrolling.png"
    state: str # e.g., "清醒", "警惕"
    behavior: str # e.g., "巡逻"
    x: int
    y: int
    width: int = 150
    height: int = 250
    interactive: bool = True

class CurrentScene(BaseModel):
    background_image: str # Path to the background image, e.g., "backgrounds/hall_circular.png"
    description: str
    objects: List[SceneObject]
    entities: List[SceneEntity]

class GameStateInput(BaseModel):
    current_turn: int
    player_action: PlayerAction
    current_scene: CurrentScene
    active_rules: List[str]
    discovered_victory_clues: List[str]
    hidden_victory_condition: str # AI internal reference

class NewRule(BaseModel):
    rule_number: int
    rule_content: str
    rule_type: str # "禁止型" | "强制型" | "条件型" | "目标型" | "矛盾型"

class GameStateUpdates(BaseModel):
    scene_changes_description: str # Renamed for clarity
    updated_scene: Optional[CurrentScene] = None # New field to send full scene updates
    victory_clue_added: Optional[str] = None

class AIResponse(BaseModel):
    new_rule: NewRule
    ai_response_to_player: str
    game_state_updates: GameStateUpdates