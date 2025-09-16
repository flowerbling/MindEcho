import json
import random
from typing import Dict, List, Any
from backend.enhanced_models import *
from backend.ai_integration import AIGameMaster, EntityManager, MapManager

class GameEngine:
    """游戏引擎 - 负责整个游戏流程的控制"""
    
    def __init__(self, config: GameConfig, api_key: str, base_url: str):
        self.config = config
        self.ai_master = AIGameMaster(api_key, base_url)
        self.entity_manager = EntityManager(self.ai_master)
        self.map_manager = MapManager(self.ai_master)
        self.game_session = None
        self.storyline = None
        
    def start_new_game(self, theme: str, difficulty: int):
        """开始新游戏"""
        
        # 加载资源
        self._load_assets()
        
        # 生成主线剧情
        self.storyline = self.ai_master.generate_storyline(
            theme, difficulty, list(self.map_manager.map_templates.keys())
        )
        
        # 初始化游戏会话
        initial_map_id = self.storyline.required_maps[0]
        self.map_manager.switch_to_map(initial_map_id)
        
        self.game_session = GameSession(
            session_id=str(uuid.uuid4()),
            current_map_id=initial_map_id,
            current_phase=GamePhase.INITIALIZATION,
            victory_conditions=[self.storyline.victory_condition],
            failure_conditions=self.storyline.failure_conditions,
            story_context={"title": self.storyline.title, "theme": self.storyline.theme}
        )
        
        # 初始化地图实体
        self._initialize_map_entities()
        
        self.game_session.current_phase = GamePhase.EXPLORATION
        
        return self.get_game_state()
        
    def process_player_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """处理玩家行为"""
        
        if not self.game_session:
            return {"error": "游戏未开始"}
        
        # 更新回合数
        self.game_session.turn_count += 1
        
        # 处理具体行为
        action_type = action.get("type")
        if action_type == "interact":
            result = self.entity_manager.handle_entity_interaction(
                action.get("target_id"),
                InteractionType(action.get("interaction_type")),
                {"player": self.game_session.player_stats, "turn": self.game_session.turn_count}
            )
            # 更新游戏状态
            self._apply_interaction_result(result)
        
        # AI生成动态内容
        dynamic_content = self.ai_master.generate_dynamic_content(self.game_session, action)
        self._apply_dynamic_content(dynamic_content)
        
        # 检查游戏结束条件
        self._check_game_over()
        
        # 评估游戏状态
        if self.game_session.turn_count % 5 == 0:
            evaluation = self.ai_master.evaluate_game_state(self.game_session)
            self._apply_game_evaluation(evaluation)
            
        return self.get_game_state()
        
    def get_game_state(self) -> Dict[str, Any]:
        """获取当前游戏状态"""
        if not self.game_session:
            return {"error": "游戏未开始"}
        
        return {
            "session_id": self.game_session.session_id,
            "current_map": self.map_manager.current_map.dict() if self.map_manager.current_map else None,
            "active_entities": [e.dict() for e in self.game_session.active_entities],
            "game_phase": self.game_session.current_phase.value,
            "turn_count": self.game_session.turn_count,
            "story_context": self.game_session.story_context,
            "discovered_clues": self.game_session.discovered_clues,
            "game_rules": self.game_session.game_rules
        }
        
    def _load_assets(self):
        """加载游戏资源"""
        with open("backend/assets/maps.json", "r", encoding="utf-8") as f:
            maps_data = json.load(f)
        self.map_manager.load_map_templates(maps_data)
        
        with open("backend/assets/entities.json", "r", encoding="utf-8") as f:
            entities_data = json.load(f)
        self.entity_manager.load_entity_templates(entities_data)
        
    def _initialize_map_entities(self):
        """初始化地图上的实体"""
        
        if not self.map_manager.current_map:
            return
            
        self.game_session.active_entities = []
        
        for sp in self.map_manager.current_map.spawn_points:
            entity = self.entity_manager.spawn_entity_at_point(sp, self.game_session.dict())
            if entity:
                self.game_session.active_entities.append(entity)
                
    def _apply_interaction_result(self, result: Dict[str, Any]):
        """应用互动结果"""
        if "dialogue" in result and result["dialogue"]:
            self.game_session.story_context["last_dialogue"] = result["dialogue"]
        
        if "items_given" in result:
            # 添加物品到玩家背包
            pass
            
    def _apply_dynamic_content(self, content: DynamicContent):
        """应用AI生成的动态内容"""
        
        for new_entity in content.new_entities:
            self.game_session.active_entities.append(new_entity)
            
        for story_element in content.story_elements:
            if story_element.type == "clue":
                self.game_session.discovered_clues.append(story_element.content)
            elif story_element.type == "rule":
                self.game_session.game_rules.append(story_element.content)
            else:
                self.game_session.story_context[f"story_{self.game_session.turn_count}"] = story_element.content
                
        if content.phase_transitions:
            self.game_session.current_phase = content.phase_transitions
            
    def _check_game_over(self):
        """检查游戏结束条件"""
        # 这里应该有更复杂的逻辑来检查胜利和失败条件
        if self.game_session.turn_count >= self.config.max_turns:
            self.game_session.current_phase = GamePhase.ENDING
            self.game_session.story_context["ending"] = "时间耗尽，冒险失败了。"
            
    def _apply_game_evaluation(self, evaluation: Dict[str, Any]):
        """应用游戏状态评估结果"""
        if evaluation.get("difficulty_adjustment", 0) > 0:
            # 增加难度，例如生成更强的敌人
            pass
        
        if evaluation.get("story_progression"):
            # 推进剧情，例如触发关键事件
            pass
