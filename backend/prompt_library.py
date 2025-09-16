import json # Import json for schema serialization
from typing import Dict, List
from langchain_core.utils.function_calling import convert_to_json_schema # Import the tool
from backend.enhanced_models import MainStoryline, DynamicContent # Import models for schema generation

class PromptLibrary:
    """提示词库 - 集中管理所有系统提示词"""
    
    def __init__(self):
        # Generate JSON schemas for relevant models
        self.main_storyline_schema = json.dumps(convert_to_json_schema(MainStoryline), indent=2, ensure_ascii=False)
        self.dynamic_content_schema = json.dumps(convert_to_json_schema(DynamicContent), indent=2, ensure_ascii=False)

        self.prompts = {
            "content_generation": {
                "system": f"""
                你是一个专业的游戏内容生成AI。你的任务是根据玩家的行为和当前游戏状态，
                生成合适的动态内容，包括新的实体、故事元素、规则变化等。
                
                输出格式必须是有效的JSON，符合DynamicContent模型结构。
                JSON Schema如下:
                {self.dynamic_content_schema}
                """,
                "user_template": """
                当前游戏会话状态:
                - 地图: {current_map_id}
                - 阶段: {current_phase}
                - 回合: {turn_count}
                - 活跃实体: {active_entities}
                
                玩家最后行动: {player_action}
                
                请生成适当的动态内容来响应玩家的行动。
                """
            },
            
            "entity_interaction": {
                "system": """
                你是一个角色扮演AI，负责控制游戏中的各种实体（NPC、物品、环境对象）。
                根据玩家的互动类型和当前上下文，生成合适的响应。
                
                输出格式必须是有效的JSON：
                {
                    "dialogue": "对话内容",
                    "state_change": {"属性": "新值"},
                    "items_given": ["物品ID"],
                    "events_triggered": ["事件描述"]
                }
                """,
                "user_template": """
                实体信息: {entity_name} - {entity_state}
                互动类型: {interaction_type}
                当前上下文: {context}
                
                请生成这个实体对此互动的响应。
                """
            },
            
            "storyline_generation": {
                "system": f"""
                你是一个故事创作AI，负责生成引人入胜的游戏主线剧情。
                考虑主题、难度和可用资源，创造一个完整的故事弧。
                
                输出格式必须是有效的JSON，符合MainStoryline模型结构。
                JSON Schema如下:
                {self.main_storyline_schema}
                """,
                "user_template": """
                主题: {theme}
                难度等级: {difficulty}
                可用地图: {available_maps}
                
                请生成一个完整的主线剧情。
                """
            },
            
            "game_evaluation": {
                "system": """
                你是一个游戏平衡AI，负责评估当前游戏状态并提供调整建议。
                分析玩家的进度、参与度和挑战水平。
                
                输出格式必须是有效的JSON：
                {
                    "difficulty_adjustment": 0,
                    "story_progression": false,
                    "new_challenges": [],
                    "player_engagement": "high/medium/low"
                }
                """,
                "user_template": """
                当前游戏状态:
                - 回合数: {turn_count}
                - 游戏阶段: {current_phase}
                - 玩家统计: {player_stats}
                - 发现的线索: {discovered_clues_count}
                - 活跃实体数: {active_entities_count}
                
                请评估游戏状态并提供建议。
                """
            }
        }
        
    def get_system_prompt(self, category: str) -> str:
        """获取系统提示词"""
        return self.prompts.get(category, {}).get("system", "你是一个游戏AI助手。")
        
    def format_user_prompt(self, category: str, context: Dict[str, any]) -> str:
        """格式化用户提示词"""
        template = self.prompts.get(category, {}).get("user_template", "")
        return template.format(**context)

# 实例化提示词库
prompt_library = PromptLibrary()
