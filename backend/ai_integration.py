import openai
import json
import random
from typing import Dict, List, Any, Optional
from backend.enhanced_models import *
from backend.models import GameStateInput, AIResponse
from backend.prompt_library import prompt_library
from json_repair import repair_json

def fix_json(text: str):
    text = text.replace("```", "").strip()
    text = text.replace("JSON", "").strip()
    text = text.replace("json", "").strip()
    # 从第一个 { 开始 最后一个 }结束
    text = text[text.find("{") : text.rfind("}") + 1]
    text = repair_json(text)
    try:
        json.loads(text)
        return text
    except:
        print("调用 open ai 接口返回内容格式错误")
        return text
    
class AIGameMaster:
    """AI游戏大师 - 负责所有AI相关的游戏逻辑"""
    
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-4o"):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.conversation_history = []
        
    def generate_dynamic_content(self, game_session: GameSession, player_action: Dict[str, Any]) -> DynamicContent:
        """根据游戏状态和玩家行为生成动态内容"""
        
        context = {
            "current_map_id": game_session.current_map_id,
            "current_phase": game_session.current_phase.value,
            "turn_count": game_session.turn_count,
            "active_entities": [e.name for e in game_session.active_entities],
            "player_action": json.dumps(player_action, ensure_ascii=False)
        }
        prompt = prompt_library.format_user_prompt("content_generation", context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_library.get_system_prompt("content_generation")},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            result_content = response.choices[0].message.content
            fixed_content = fix_json(result_content)
            content_data = json.loads(fixed_content)
            return DynamicContent(**content_data)
            
        except Exception as e:
            print(f"AI内容生成错误: {e}")
            return DynamicContent()
    
    def generate_entity_interaction(self, entity: EntityInstance, interaction_type: InteractionType, 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """为实体生成互动响应"""
        
        prompt_context = {
            "entity_name": entity.name,
            "entity_state": json.dumps(entity.current_state, ensure_ascii=False),
            "interaction_type": interaction_type.value,
            "context": json.dumps(context, ensure_ascii=False)
        }
        prompt = prompt_library.format_user_prompt("entity_interaction", prompt_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_library.get_system_prompt("entity_interaction")},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            result_content = response.choices[0].message.content
            fixed_content = fix_json(result_content)
            return json.loads(fixed_content)
            
        except Exception as e:
            print(f"实体互动生成错误: {e}")
            return {"dialogue": "...", "state_change": {}, "items_given": [], "events_triggered": []}
    
    def generate_storyline(self, theme: str, difficulty: int, available_maps: List[str]) -> MainStoryline:
        """生成主线剧情"""
        prompt_context = {
            "theme": theme,
            "difficulty": difficulty,
            "available_maps": ', '.join(available_maps)
        }
        prompt = prompt_library.format_user_prompt("storyline_generation", prompt_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_library.get_system_prompt("storyline_generation")},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            result_content = response.choices[0].message.content
            fixed_content = fix_json(result_content)
            print(fixed_content)
            storyline_data = json.loads(fixed_content)
            return MainStoryline(**storyline_data)
            
        except Exception as e:
            print(f"剧情生成错误: {e}")
            # 返回默认剧情
            return self._get_default_storyline(theme, available_maps)
    
    def evaluate_game_state(self, game_session: GameSession) -> Dict[str, Any]:
        """评估当前游戏状态，判断是否需要调整难度或推进剧情"""
        
        prompt_context = {
            "turn_count": game_session.turn_count,
            "current_phase": game_session.current_phase.value,
            "player_stats": json.dumps(game_session.player_stats, ensure_ascii=False),
            "discovered_clues_count": len(game_session.discovered_clues),
            "active_entities_count": len(game_session.active_entities)
        }
        prompt = prompt_library.format_user_prompt("game_evaluation", prompt_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_library.get_system_prompt("game_evaluation")},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            result_content = response.choices[0].message.content
            fixed_content = fix_json(result_content)
            return json.loads(fixed_content)
            
        except Exception as e:
            print(f"游戏状态评估错误: {e}")
            return {"difficulty_adjustment": 0, "story_progression": False, "new_challenges": []}
    
    def _get_default_storyline(self, theme: str, available_maps: List[str]) -> MainStoryline:
        """获取默认剧情模板"""
        return MainStoryline(
            id="default_story",
            title=f"{theme}的秘密",
            description="一个神秘的冒险等待着你...",
            theme=theme,
            estimated_turns=50,
            required_maps=available_maps[:3] if len(available_maps) >= 3 else available_maps,
            key_entities=["神秘向导", "守护者", "关键道具"],
            victory_condition="找到并激活所有古代神器",
            failure_conditions=["生命值归零", "时间耗尽"],
            story_beats=[
                {"turn": 10, "event": "遇到第一个关键NPC"},
                {"turn": 25, "event": "发现重要线索"},
                {"turn": 40, "event": "面临最终挑战"}
            ]
        )


class EntityManager:
    """实体管理器 - 负责实体的生成、更新和互动"""
    
    def __init__(self, ai_master: AIGameMaster):
        self.ai_master = ai_master
        self.entity_templates = {}
        self.active_entities = {}
        
    def load_entity_templates(self, templates_data: List[Dict[str, Any]]):
        """加载实体模板"""
        for template_data in templates_data:
            template = EntityTemplate(**template_data)
            self.entity_templates[template.id] = template
    
    def spawn_entity_at_point(self, spawn_point: SpawnPoint, game_context: Dict[str, Any]) -> Optional[EntityInstance]:
        """在刷新点生成实体"""
        
        # 检查生成条件
        if not self._check_spawn_conditions(spawn_point, game_context):
            return None
        
        # 随机选择实体类型
        available_templates = [
            t for t in self.entity_templates.values() 
            if t.entity_type in spawn_point.entity_types
        ]
        
        if not available_templates:
            return None
        
        # 根据权重选择模板
        template = self._weighted_random_choice(available_templates)
        
        # 创建实体实例
        entity = EntityInstance(
            template_id=template.id,
            name=template.name,
            current_state=template.base_stats.copy(),
            position={"x": spawn_point.x, "y": spawn_point.y}
        )
        
        # 使用AI生成个性化属性
        if random.random() < 0.3:  # 30%概率进行AI个性化
            entity = self._personalize_entity_with_ai(entity, game_context)
        
        self.active_entities[entity.id] = entity
        return entity
    
    def handle_entity_interaction(self, entity_id: str, interaction_type: InteractionType, 
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """处理实体互动"""
        
        if entity_id not in self.active_entities:
            return {"error": "实体不存在"}
        
        entity = self.active_entities[entity_id]
        template = self.entity_templates.get(entity.template_id)
        
        if not template:
            return {"error": "实体模板不存在"}
        
        # 检查是否有预定义的互动规则
        matching_rule = None
        for rule in template.interaction_rules:
            if rule.interaction_type == interaction_type:
                if self._check_interaction_conditions(rule, entity, context):
                    matching_rule = rule
                    break
        
        if matching_rule:
            # 使用预定义规则
            result = self._apply_interaction_rule(matching_rule, entity, context)
        else:
            # 使用AI生成互动响应
            result = self.ai_master.generate_entity_interaction(entity, interaction_type, context)
        
        # 更新实体状态
        if "state_change" in result:
            entity.current_state.update(result["state_change"])
        
        # 记录互动历史
        entity.interaction_history.append({
            "type": interaction_type.value,
            "context": context,
            "result": result,
            "timestamp": context.get("turn", 0)
        })
        
        return result
    
    def _check_spawn_conditions(self, spawn_point: SpawnPoint, game_context: Dict[str, Any]) -> bool:
        """检查生成条件"""
        if random.random() > spawn_point.spawn_probability:
            return False
        
        # 检查冷却时间
        last_spawn = game_context.get("last_spawns", {}).get(spawn_point.id, -999)
        if game_context.get("current_turn", 0) - last_spawn < spawn_point.cooldown_turns:
            return False
        
        # 检查最大生成数量
        current_spawns = sum(1 for e in self.active_entities.values() 
                           if e.position["x"] == spawn_point.x and e.position["y"] == spawn_point.y)
        if current_spawns >= spawn_point.max_spawns:
            return False
        
        return True
    
    def _weighted_random_choice(self, templates: List[EntityTemplate]) -> EntityTemplate:
        """根据权重随机选择模板"""
        weights = [t.spawn_weight for t in templates]
        return random.choices(templates, weights=weights)[0]
    
    def _personalize_entity_with_ai(self, entity: EntityInstance, context: Dict[str, Any]) -> EntityInstance:
        """使用AI个性化实体"""
        # 这里可以调用AI来生成独特的属性、对话等
        # 为了简化，暂时返回原实体
        return entity
    
    def _check_interaction_conditions(self, rule: InteractionRule, entity: EntityInstance, 
                                    context: Dict[str, Any]) -> bool:
        """检查互动条件"""
        for condition_key, condition_value in rule.conditions.items():
            if condition_key in entity.current_state:
                if entity.current_state[condition_key] != condition_value:
                    return False
            elif condition_key in context:
                if context[condition_key] != condition_value:
                    return False
        return True
    
    def _apply_interaction_rule(self, rule: InteractionRule, entity: EntityInstance, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """应用互动规则"""
        result = {
            "dialogue": rule.dialogue or "",
            "state_change": rule.effects.copy(),
            "items_given": rule.effects.get("items_given", []),
            "events_triggered": rule.effects.get("events_triggered", [])
        }
        
        # 检查成功率
        if random.random() > rule.success_rate:
            result["dialogue"] = "互动失败了..."
            result["state_change"] = {}
            result["items_given"] = []
        
        return result


class MapManager:
    """地图管理器 - 负责地图的加载、切换和动态修改"""
    
    def __init__(self, ai_master: AIGameMaster):
        self.ai_master = ai_master
        self.map_templates = {}
        self.current_map = None
        
    def load_map_templates(self, templates_data: List[Dict[str, Any]]):
        """加载地图模板"""
        for template_data in templates_data:
            template = MapTemplate(**template_data)
            self.map_templates[template.id] = template
    
    def generate_dynamic_map(self, theme: str, difficulty: int) -> MapTemplate:
        """使用AI生成动态地图"""
        # 这里可以调用AI来生成新的地图布局
        # 为了简化，暂时返回随机选择的现有地图
        available_maps = [m for m in self.map_templates.values() if m.theme == theme]
        if available_maps:
            return random.choice(available_maps)
        else:
            return list(self.map_templates.values())[0] if self.map_templates else None
    
    def switch_to_map(self, map_id: str) -> bool:
        """切换到指定地图"""
        if map_id in self.map_templates:
            self.current_map = self.map_templates[map_id]
            return True
        return False
