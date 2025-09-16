from pydantic import BaseModel, Field # Import Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import uuid

# 扩展的游戏数据模型

class InteractionType(str, Enum):
    PICKUP = "pickup"
    USE = "use"
    TRADE = "trade"
    BRIBE = "bribe"
    ATTACK = "attack"
    TALK = "talk"
    OBSERVE = "observe"
    ACTIVATE = "activate"

class EntityType(str, Enum):
    NPC = "npc"
    OBJECT = "object"
    ENVIRONMENT = "environment"

class SpawnPointType(str, Enum):
    RANDOM = "random"
    CONDITIONAL = "conditional"
    STORY_DRIVEN = "story_driven"

class GamePhase(str, Enum):
    INITIALIZATION = "initialization"
    EXPLORATION = "exploration"
    CONFLICT = "conflict"
    RESOLUTION = "resolution"
    ENDING = "ending"

# 地图相关模型
class MapTemplate(BaseModel):
    id: str = Field(..., description="地图的唯一标识符")
    name: str = Field(..., description="地图的名称")
    description: str = Field("", description="地图的详细描述")
    background_image: str = Field(..., description="地图背景图片的路径")
    width: int = Field(1920, description="地图的设计宽度（像素）")
    height: int = Field(1080, description="地图的设计高度（像素）")
    theme: str = Field("未知", description="地图的主题（如：古代遗迹、现代都市）")
    difficulty_level: int = Field(1, description="地图的难度等级")
    spawn_points: List['SpawnPoint'] = Field([], description="地图上的刷新点列表")
    connections: List[str] = Field([], description="与该地图相连的其他地图ID列表")

class SpawnPoint(BaseModel):
    id: str = Field(..., description="刷新点的唯一标识符")
    x: float = Field(..., description="刷新点在地图上的相对X坐标（0.0-1.0）")
    y: float = Field(..., description="刷新点在地图上的相对Y坐标（0.0-1.0）")
    width: float = Field(100.0, description="刷新区域的相对宽度（0.0-1.0）")
    height: float = Field(100.0, description="刷新区域的相对高度（0.0-1.0）")
    rotation: float = Field(0.0, description="刷新区域的旋转角度（度）")
    spawn_type: SpawnPointType = Field(SpawnPointType.RANDOM, description="刷新点的类型（随机、条件、剧情驱动）")
    entity_types: List[EntityType] = Field([], description="该刷新点可以刷新的实体类型列表")
    spawn_conditions: Dict[str, Any] = Field({}, description="刷新实体所需的条件（键值对）")
    spawn_probability: float = Field(0.5, description="刷新实体概率（0.0-1.0）")
    max_spawns: int = Field(1, description="该刷新点最大可刷新实体数量")
    cooldown_turns: int = Field(0, description="刷新点再次刷新所需的冷却回合数")

# 实体和主体模型
class EntityTemplate(BaseModel):
    id: str = Field(..., description="实体模板的唯一标识符")
    name: str = Field(..., description="实体的名称")
    description: str = Field(..., description="实体的详细描述")
    entity_type: EntityType = Field(..., description="实体的类型（NPC、物品、环境）")
    image_path: str = Field(..., description="实体图片的路径")
    base_stats: Dict[str, Any] = Field({}, description="实体的基础属性（如生命值、攻击力）")
    interaction_rules: List['InteractionRule'] = Field([], description="实体可进行的互动规则列表")
    spawn_weight: float = Field(1.0, description="实体在刷新点刷新的权重")
    rarity: str = Field("common", description="实体的稀有度（common, uncommon, rare, legendary）")

class InteractionRule(BaseModel):
    interaction_type: InteractionType = Field(..., description="互动类型（如：对话、交易、攻击）")
    conditions: Dict[str, Any] = Field({}, description="触发此互动所需的条件")
    effects: Dict[str, Any] = Field({}, description="互动成功后产生的效果")
    dialogue: Optional[str] = Field(None, description="互动时的对话内容")
    success_rate: float = Field(1.0, description="互动成功的概率（0.0-1.0）")
    cooldown: int = Field(0, description="互动后的冷却时间（回合数）")

# 动态实体实例
class EntityInstance(BaseModel):
    id: str = Field(None, description="实体实例的唯一标识符，如果为None则自动生成")
    template_id: str = Field(..., description="实体所基于的模板ID")
    name: str = Field(..., description="实体实例的名称")
    current_state: Dict[str, Any] = Field({}, description="实体实例的当前状态")
    position: Dict[str, int] = Field(..., description="实体在地图上的位置坐标 {'x': int, 'y': int}")
    inventory: List[str] = Field([], description="实体持有的物品ID列表")
    active_effects: List[Dict[str, Any]] = Field([], description="实体当前活跃的效果列表")
    interaction_history: List[Dict[str, Any]] = Field([], description="实体与玩家的互动历史")
    
    def __init__(self, **data):
        if data.get('id') is None:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)

# 游戏状态模型
class GameSession(BaseModel):
    session_id: str = Field(..., description="当前游戏会话的唯一标识符")
    current_map_id: str = Field(..., description="玩家当前所在地图的ID")
    current_phase: GamePhase = Field(..., description="当前游戏阶段")
    turn_count: int = Field(0, description="当前游戏回合数")
    player_stats: Dict[str, Any] = Field({}, description="玩家的各项属性和统计数据")
    active_entities: List[EntityInstance] = Field([], description="当前地图中活跃的实体实例列表")
    game_rules: List[str] = Field([], description="当前生效的游戏规则列表")
    victory_conditions: List[str] = Field([], description="当前游戏的胜利条件列表")
    failure_conditions: List[str] = Field([], description="当前游戏的失败条件列表")
    story_context: Dict[str, Any] = Field({}, description="当前游戏的剧情上下文信息")
    discovered_clues: List[str] = Field([], description="玩家已发现的线索列表")

# AI生成内容的模型
class StoryElement(BaseModel):
    type: str = Field(..., description="故事元素的类型（如：dialogue, description, clue, rule）")
    content: str = Field(..., description="故事元素的具体内容")
    context: Dict[str, Any] = Field({}, description="故事元素相关的上下文信息")
    priority: int = Field(1, description="故事元素的优先级，影响其在游戏中的呈现顺序")

class DynamicContent(BaseModel):
    map_modifications: List[Dict[str, Any]] = Field([], description="对地图进行的修改列表")
    new_entities: List[EntityInstance] = Field([], description="新生成的实体实例列表")
    story_elements: List[StoryElement] = Field([], description="AI生成的故事元素列表")
    rule_changes: List[str] = Field([], description="游戏规则的变化列表")
    phase_transitions: Optional[GamePhase] = Field(None, description="如果游戏阶段发生变化，指定新的阶段")

# 主线剧情模板
class MainStoryline(BaseModel):
    id: str = Field(..., description="主线剧情的唯一标识符")
    title: str = Field(..., description="主线剧情的标题")
    description: str = Field(..., description="主线剧情的详细描述")
    theme: str = Field(..., description="主线剧情的主题")
    estimated_turns: int = Field(..., description="完成主线剧情的预估回合数")
    required_maps: List[str] = Field([], description="主线剧情所需的地图ID列表")
    key_entities: List[str] = Field([], description="主线剧情中的关键实体ID列表")
    victory_condition: str = Field(..., description="主线剧情的胜利条件")
    failure_conditions: List[str] = Field([], description="主线剧情的失败条件列表")
    story_beats: List[Dict[str, Any]] = Field([], description="关键剧情节点列表，每个节点包含剧情描述和触发条件")

# AI提示词模板
class PromptTemplate(BaseModel):
    name: str = Field(..., description="提示词模板的名称")
    category: str = Field(..., description="提示词的分类（如：entity_generation, story_progression）")
    template: str = Field(..., description="提示词的文本模板")
    variables: List[str] = Field([], description="模板中可用的变量列表")
    context_requirements: List[str] = Field([], description="生成此提示词所需的上下文信息")

# 游戏配置
class GameConfig(BaseModel):
    max_turns: int = Field(100, description="游戏的最大回合数")
    ai_creativity_level: float = Field(0.7, description="AI生成内容的创意水平（0.0-1.0）")
    difficulty_scaling: bool = Field(True, description="是否启用难度动态调整")
    dynamic_story_generation: bool = Field(True, description="是否启用动态故事生成")
    player_agency_weight: float = Field(0.8, description="玩家行动对游戏走向影响的权重（0.0-1.0）")
    randomness_factor: float = Field(0.3, description="游戏中随机事件发生的频率因子（0.0-1.0）")
