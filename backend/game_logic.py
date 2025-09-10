from typing import List, Optional, Dict, Any
from backend.models import PlayerAction, GameStateInput, NewRule, GameStateUpdates, AIResponse, CurrentScene, SceneObject, SceneEntity

# --- Game State (Simplified for Prototype) ---
# In a real game, this would be a database or more complex state management
game_state = {
    "current_turn": 0,
    "current_scene": {
        "background_image": "backgrounds/hall_circular.png",
        "description": "你身处一个空旷的圆形大厅，中央有一颗发光的水晶，两侧是紧闭的石门。一名守卫在房间中央巡逻。",
        "objects": [
            {"name": "水晶", "image": "objects/crystal_inactive.png", "state": "未激活", "x": 450, "y": 300, "width": 150, "height": 150, "interactive": True},
            {"name": "石门", "image": "objects/door_closed.png", "state": "紧闭", "x": 100, "y": 250, "width": 120, "height": 200, "interactive": True}
        ],
        "entities": [
            {"name": "守卫", "image": "entities/guard_patrolling.png", "state": "清醒", "behavior": "巡逻", "x": 700, "y": 200, "width": 180, "height": 300, "interactive": True}
        ]
    },
    "active_rules": ["规则0: 你不能伤害自己。"],
    "discovered_victory_clues": [],
    "hidden_victory_condition": "激活所有水晶", # This would be randomly generated
    "rule_counter": 0,
}

# --- Helper Functions (Placeholder for AI Logic) ---
def generate_ai_response(game_state_input: GameStateInput) -> AIResponse:
    """
    This function would contain the core AI logic based on system_prompt.md.
    For this prototype, it's a simplified placeholder.
    """
    global game_state

    player_action = game_state_input.player_action
    current_rules = game_state_input.active_rules
    current_rule_counter = game_state["rule_counter"]

    new_rule_content = ""
    ai_feedback = ""
    scene_changes_description = ""
    victory_clue = None

    # Create a mutable copy of the current scene for updates
    updated_scene = CurrentScene(**game_state_input.current_scene.dict())

    # Simplified AI logic based on player action type
    if player_action.type == "Interact":
        if player_action.target == "水晶":
            crystal = next((obj for obj in updated_scene.objects if obj.name == "水晶"), None)
            guard = next((ent for ent in updated_scene.entities if ent.name == "守卫"), None)

            if crystal and crystal.state == "未激活":
                new_rule_content = f"每次触摸水晶后，必须向守卫报告一次，否则水晶失效。"
                ai_feedback = "你的触摸激活了水晶，但守卫似乎注意到了什么。"
                scene_changes_description = "水晶发出微弱的光芒，守卫的巡逻路径略有调整。"
                
                crystal.state = "已激活"
                crystal.image = "objects/crystal_active.png"
                if guard:
                    guard.behavior = "警惕"
                    guard.image = "entities/guard_alert.png"
                
                victory_clue = "你感觉到水晶的激活与某种更深层的目标有关。"
            else:
                new_rule_content = "你已经激活了水晶，重复触摸不会有新的效果。"
                ai_feedback = "水晶已经激活，你的动作没有引起新的变化。"
                scene_changes_description = "没有明显变化。"
        else:
            new_rule_content = f"你不能与{player_action.target}进行无效交互。"
            ai_feedback = f"你尝试与{player_action.target}交互，但没有效果。"
            scene_changes_description = "没有明显变化。"
    elif player_action.type == "Move":
        new_rule_content = "在移动到新区域前，必须先观察当前区域��"
        ai_feedback = "你尝试移动，但迷宫的规则要求你先观察。"
        scene_changes_description = "迷宫的路径似乎变得更加复杂。"
    elif player_action.type == "Observe":
        ai_feedback = "你仔细观察了周围，发现了一些细节。"
        scene_changes_description = "你对场景有了更深的理解。"
        # Example: if observing reveals a clue
        if not game_state["discovered_victory_clues"]:
            victory_clue = "你注意到石门上刻有模糊的符文，似乎与某种力量有关。"
    elif player_action.type == "Declare":
        # For prototype, always say it's wrong for simplicity
        new_rule_content = "你的声明与现有法则不符，请谨慎言行。"
        ai_feedback = "你的声明没有得到法则的认可。"
        scene_changes_description = "空气中弥漫着一丝不悦。"
    elif player_action.type == "Challenge":
        # For prototype, always say no contradiction
        ai_feedback = "规则系统逻辑一致，挑战失败。"
        new_rule_content = "挑战失败后，你必须等待三个回合才能再次挑战。"
        scene_changes_description = "规则的力量似乎更加稳固了。"

    # Update global game state for the next turn
    game_state["current_turn"] += 1
    if new_rule_content:
        game_state["rule_counter"] += 1
        game_state["active_rules"].append(f"规则{game_state['rule_counter']}: {new_rule_content}")
    if victory_clue and victory_clue not in game_state["discovered_victory_clues"]:
        game_state["discovered_victory_clues"].append(victory_clue)
    
    # Apply the updated scene back to the global game_state
    game_state["current_scene"] = updated_scene.dict()


    return AIResponse(
        new_rule=NewRule(
            rule_number=game_state["rule_counter"],
            rule_content=new_rule_content if new_rule_content else "没有新的规则生成。",
            rule_type="强制型" if "必须" in new_rule_content else "禁止型" if "不能" in new_rule_content else "条件型" if "只有在" in new_rule_content else "目标型" if "收集" in new_rule_content else "禁止型" # Simplified type inference
        ),
        ai_response_to_player=ai_feedback,
        game_state_updates=GameStateUpdates(
            scene_changes_description=scene_changes_description,
            updated_scene=updated_scene, # Pass the updated scene
            victory_clue_added=victory_clue
        )
    )