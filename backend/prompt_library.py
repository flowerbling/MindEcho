import json # Import json for schema serialization
from typing import Dict, List
from langchain_core.utils.function_calling import convert_to_json_schema # Import the tool
from backend.enhanced_models import MainStoryline, DynamicContent, MapTemplate # Import models for schema generation

class PromptLibrary:
    """提示词库 - 集中管理所有系统提示词"""
    
    def __init__(self):
        # Generate JSON schemas for relevant models
        self.main_storyline_schema = json.dumps(convert_to_json_schema(MainStoryline), indent=2, ensure_ascii=False)
        self.dynamic_content_schema = json.dumps(convert_to_json_schema(DynamicContent), indent=2, ensure_ascii=False)
        self.map_template_schema = json.dumps(convert_to_json_schema(MapTemplate), indent=2, ensure_ascii=False)

        self.prompts = {
            "map_generation": {
                "system": f"""
                你是一个专业的游戏地图设计师。你的任务是根据游戏的主题、难度和故事情节，
                设计一个有趣且符合逻辑的地图布局。
                
                地图应含多个刷新点（spawn_points），用于放置NPC、物品或敌人。
                刷新点的设计应与故事情节紧密相关。
                
                输出格式必须是有效的JSON，符合MapTemplate模型结构。
                JSON Schema如下:
                {self.map_template_schema}
                """,
                "user_template": """
                游戏主题: {theme}
                难度等级: {difficulty}
                故事情节摘要: {storyline_summary}
                
                请为这个场景设计一个合适的地图。
                """
            },
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
                你是一个顶级的游戏编剧AI。你的任务是根据给定的主题和难度，创作一个包含多个场景(scenes)的完整游戏剧本。

                **核心要求**:
                1.  **多场景结构**: 整个故事必须被分解为至少3个逻辑连贯的场景。
                2.  **场景目标**: 每个场景都必须有一个明确的故事描述(description)和完成条件(completion_condition)。
                3.  **结构化条件**: 场景的`completion_condition`以及最终的`victory_condition`和`failure_conditions`必须使用结构化格式: "type:target:value" 或 "type:target"。
                    - 例如: "player_has_item:ancient_artifact", "entity_state:gatekeeper:defeated", "clue_discovered:secret_code"。
                
                输出格式必是有效的JSON，严格符合MainStoryline模型结构。
                JSON Schema如下:
                {self.main_storyline_schema}
                """,
                "user_template": """
                游戏主题: {theme}
                难度等级: {difficulty}
                
                请创作一个包含多个场景的完整游戏剧本。
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
            },
            "rule_generation": {
                "system": """
                你是一个富有想象力的游戏规则设计师。你的任务是根据游戏的主题和故事背景，
                设计出3-5条独特、有趣且能增强沉浸感的游戏规则。
                
                规则应该是清晰、简洁的句子。
                
                输出格式必须是有效的JSON：
                {
                    "rules": [
                        "规则1",
                        "规则2",
                        "..."
                    ]
                }
                """,
                "user_template": """
                游戏主题: {theme}
                故事背景: {storyline_description}
                
                请为此游戏设计一套独特的法则。
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
