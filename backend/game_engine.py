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
        
    async def start_new_game(self, theme: str, difficulty: int):
        """开始新游戏 (SSE异步生成器)"""
        
        yield {"status": "loading", "message": "正在加载静态资源..."}
        self._load_assets()
        
        yield {"status": "loading", "message": "AI正在生成游戏剧本..."}
        self.storyline = await self.ai_master.generate_storyline(theme, difficulty)
        if not self.storyline or not self.storyline.scenes:
            raise ValueError("AI未能生成有效的主线剧本。")
        
        yield {"status": "loading", "message": "正在初始化游戏会话..."}
        initial_scene = self.storyline.scenes[0]
        self.game_session = GameSession(
            session_id=str(uuid.uuid4()),
            current_scene_id=initial_scene.id,
            current_phase=GamePhase.INITIALIZATION,
            victory_conditions=[self.storyline.victory_condition],
            failure_conditions=self.storyline.failure_conditions,
            story_context={"title": self.storyline.title, "theme": self.storyline.theme}
        )

        yield {"status": "loading", "message": "AI正在生成游戏规则..."}
        game_rules = await self.ai_master.generate_game_rules(self.storyline.theme, self.storyline.description)
        self.game_session.game_rules.extend(game_rules)

        # 正确地迭代异步生成器并转发其产生的状态
        async for status in self._load_scene(initial_scene):
            yield status
        
        self.game_session.current_phase = GamePhase.EXPLORATION
        yield {"status": "done", "gameState": self.get_game_state()}
        
    async def process_player_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """处理玩家行为（V2版 - 异步）"""
        if not self.game_session:
            return {"error": "游戏未开始"}

        self.game_session.turn_count += 1

        action_type = action.get("type")
        if action_type == "interact":
            target_id = action.get("target_id")
            interaction_type_str = action.get("interaction_type")
            
            if not target_id or not interaction_type_str:
                return {"error": "无效的互动请求"}

            interaction_type = InteractionType(interaction_type_str)
            context = {
                "player": self.game_session.player_stats,
                "inventory": self.game_session.player_inventory,
                "turn": self.game_session.turn_count
            }
            
            result = await self.entity_manager.handle_entity_interaction(target_id, interaction_type, context)
            self._apply_interaction_result(result)

        dynamic_content = await self.ai_master.generate_dynamic_content(self.game_session, action)
        self._apply_dynamic_content(dynamic_content)

        if self._should_change_scene():
            await self._change_to_next_scene()
            # 返回新场景的状态
            return self.get_game_state()

        if self._check_game_over():
            return self.get_game_state()

        if self.game_session.turn_count % 5 == 0:
            evaluation = await self.ai_master.evaluate_game_state(self.game_session)
            self._apply_game_evaluation(evaluation)
            
        return self.get_game_state()
        
    def get_game_state(self) -> Dict[str, Any]:
        """获取当前游戏状态（V2版，适配前端）"""
        if not self.game_session:
            return {"error": "游戏未开始"}
        
        current_scene = self.get_current_scene()
        current_map_data = self.map_manager.current_map.dict() if self.map_manager.current_map else {}
        
        # 将实体分类并注入到地图数据中，以匹配前端期望
        if current_map_data:
            entities = []
            objects = []
            for e in self.game_session.active_entities:
                template = self.entity_manager.entity_templates.get(e.template_id)
                if not template:
                    continue
                
                entity_data = e.dict()
                entity_data['image'] = template.image_path
                entity_data['interactive'] = True

                if template.entity_type == EntityType.NPC:
                    entities.append(entity_data)
                else:
                    objects.append(entity_data)
            
            current_map_data['entities'] = entities
            current_map_data['objects'] = objects

        return {
            "session_id": self.game_session.session_id,
            "current_scene": current_scene.dict() if current_scene else None,
            "current_map": current_map_data,
            "game_phase": self.game_session.current_phase.value,
            "turn_count": self.game_session.turn_count,
            "story_context": self.game_session.story_context,
            "discovered_clues": self.game_session.discovered_clues,
            "active_rules": self.game_session.game_rules, # 修复字段名以匹配前端
            "player_inventory": self.game_session.player_inventory
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
        """应用互动结果（重构版）"""
        if "dialogue" in result and result["dialogue"]:
            self.game_session.story_context["last_dialogue"] = result["dialogue"]
        
        if "items_given" in result and result["items_given"]:
            for item_id in result["items_given"]:
                if item_id not in self.game_session.player_inventory:
                    self.game_session.player_inventory.append(item_id)
                    print(f"玩家获得了物品: {item_id}")
        
        if "clues_discovered" in result and result["clues_discovered"]:
            for clue in result["clues_discovered"]:
                if clue not in self.game_session.discovered_clues:
                    self.game_session.discovered_clues.append(clue)
                    print(f"玩家发现了线索: {clue}")
            
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
        
        for map_mod in content.map_modifications:
            # Apply map modifications, e.g., unlock connections, change spawn points
            # This is a simplified example; actual implementation would be more complex
            if map_mod.get("type") == "unlock_connection" and self.map_manager.current_map:
                target_map_id = map_mod.get("target_map_id")
                if target_map_id and target_map_id not in self.map_manager.current_map.connections:
                    self.map_manager.current_map.connections.append(target_map_id)
                    print(f"地图 '{self.map_manager.current_map.name}' 解锁了新连接: {target_map_id}")
            # TODO: Add more complex map modification logic here (e.g., add/remove spawn points, change background)
            
    def _check_game_over(self) -> bool:
        """检查游戏结束条件（重构版）"""
        # 检查胜利条件
        if self._evaluate_condition(self.game_session.victory_conditions[0]):
            self.game_session.current_phase = GamePhase.ENDING
            self.game_session.story_context["ending"] = "恭喜你，任务完成了！"
            print("--- 游戏胜利 ---")
            return True
        
        # 检查失败条件
        for condition in self.game_session.failure_conditions:
            if self._evaluate_condition(condition):
                self.game_session.current_phase = GamePhase.ENDING
                self.game_session.story_context["ending"] = "很遗憾，你失败了。"
                print(f"--- 游戏失败: {condition} ---")
                return True

        # 检查回合数限制
        if self.game_session.turn_count >= self.config.max_turns:
            self.game_session.current_phase = GamePhase.ENDING
            self.game_session.story_context["ending"] = "时间耗尽，冒险失败了。"
            print("--- 游戏失败: 时间耗尽 ---")
            return True
        return False
            
    def _evaluate_condition(self, condition: str) -> bool:
        """评估一个游戏条件是否满足（重构版）"""
        if not condition: return False
        
        parts = condition.split(':')
        condition_type = parts[0]
        
        try:
            if condition_type == "player_has_item":
                item_id = parts[1]
                return item_id in self.game_session.player_inventory
                
            elif condition_type == "entity_state":
                entity_id_or_name = parts[1]
                required_state = parts[2]
                entity = next((e for e in self.game_session.active_entities if e.id == entity_id_or_name or e.name == entity_id_or_name), None)
                return entity and entity.current_state.get("status") == required_state

            elif condition_type == "clue_discovered":
                clue_content = parts[1]
                return any(clue_content in clue for clue in self.game_session.discovered_clues)

            elif condition_type == "player_stat":
                stat_name = parts[1]
                operator = parts[2] # e.g., "ge", "le", "eq"
                value = int(parts[3])
                player_value = self.game_session.player_stats.get(stat_name, 0)
                
                if operator == "ge": return player_value >= value
                if operator == "le": return player_value <= value
                if operator == "eq": return player_value == value
                return False
        except (IndexError, ValueError) as e:
            print(f"评估条件 '{condition}' 时出错: {e}")
            return False

        # Fallback for simple string checks from storyline
        if "找到并激活所有古代神器" in condition and "古代神器已激活" in self.game_session.discovered_clues:
            return True
        if "生命值归零" in condition and self.game_session.player_stats.get("health", 1) <= 0:
            return True
        if "时间耗尽" in condition and self.game_session.turn_count >= self.config.max_turns:
            return True
            
        return False
            
    def _apply_game_evaluation(self, evaluation: Dict[str, Any]):
        """应用游戏状态评估结果"""
        if evaluation.get("difficulty_adjustment", 0) > 0:
            print("AI建议增加难度...")
        
        if evaluation.get("story_progression"):
            print("AI建议推进剧情...")

    def get_current_scene(self) -> Optional[Scene]:
        """获取当前场景对象"""
        if not self.game_session or not self.storyline:
            return None
        return next((s for s in self.storyline.scenes if s.id == self.game_session.current_scene_id), None)

    async def _load_scene(self, scene: Scene):
        """加载并初始化一个新场景 (异步)"""
        yield {"status": "loading", "message": f"正在加载场景: {scene.name}..."}
        self.game_session.current_scene_id = scene.id
        self.game_session.active_entities = []

        yield {"status": "loading", "message": f"AI正在为场景 '{scene.name}' 生成地图..."}
        scene_map = await self.map_manager.generate_dynamic_map(
            scene.map_theme, 1, scene.description
        )
        self.map_manager.map_templates[scene_map.id] = scene_map
        self.map_manager.switch_to_map(scene_map.id)
        self.game_session.current_map_id = scene_map.id

        yield {"status": "loading", "message": f"AI正在为场景 '{scene.name}' 布置实体..."}
        initial_content = await self.ai_master.generate_dynamic_content(self.game_session)
        self._apply_dynamic_content(initial_content)
        
        self.game_session.story_context['current_scene_objective'] = scene.description

    def _should_change_scene(self) -> bool:
        """仅检查当前场景是否完成"""
        current_scene = self.get_current_scene()
        if not current_scene:
            return False
        return self._evaluate_condition(current_scene.completion_condition)

    async def _change_to_next_scene(self):
        """执行场景切换"""
        current_scene = self.get_current_scene()
        print(f"--- 场景 '{current_scene.name}' 已完成! ---")
        
        current_index = self.storyline.scenes.index(current_scene)
        if current_index + 1 < len(self.storyline.scenes):
            next_scene = self.storyline.scenes[current_index + 1]
            # 直接await异步生成器
            async for _ in self._load_scene(next_scene):
                # 在这里可以向客户端发送更精细的加载状态，但目前我们只在内部消费它
                pass
        else:
            print("所有场景已完成。游戏即将结束。")
            # 可以在这里设置一个特殊的游戏状态，表示故事线完成
            self.game_session.story_context["ending"] = "你已完成所有主线场景！"
            self.game_session.current_phase = GamePhase.RESOLUTION
