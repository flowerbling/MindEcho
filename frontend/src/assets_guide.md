# 游戏资产（图片、素材）说明文档

本文档旨在为《法则迷宫》游戏的前端界面提供视觉资产（图片、素材）的制作指南，包括图片内容、大致大小和建议的存放位置。**所有图片都应采用像素风格（Pixel Art）**，以 PNG 格式为主，支持透明背景，以便于叠加。

## 1. 图片存放位置

所有游戏相关图片素材建议存放在 `frontend/public/assets/` 目录下，并根据类型进一步细分：

*   **`frontend/public/assets/backgrounds/`**: 场景背景图
*   **`frontend/public/assets/objects/`**: 各种可交互物体
*   **`frontend/public/assets/entities/`**: 各种角色（实体）
*   **`frontend/public/assets/states/`**: 环境状态图标或效果
*   **`frontend/public/assets/rules/`**: 规则节点相关图片
*   **`frontend/public/assets/ui/`**: UI 界面元素（按钮、面板背景、图标等）

## 2. 场景背景图 (Backgrounds)

用于表示不同的迷宫区域或房间。这些背景图应是完整的场景，包含地板、墙壁、天花板等基本结构，但没有可交互的物体或角色。

*   **内容**:
    *   **`hall_circular.png` (圆形大厅)**: 一个宽敞的圆形房间，中央有圆形图案的地板，四周是高大的石柱和拱形入口。整体色调偏冷，营造神秘感。
    *   **`corridor_dark.png` (黑暗走廊)**: 一条狭窄而漫长的走廊，两侧是粗糙的石墙，地面湿滑。光线昏暗，仅有远处微弱的光源。
    *   **`sanctuary_glowing.png` (发光神殿)**: 一个古老的神殿内部，墙壁上刻有发光的符文，中央可能有一个祭坛或能量核心。光线明亮，充满神圣感。
    *   **`data_stream_space.png` (数据流空间)**: 一个由蓝色或绿色光线构成的抽象空间，背景是流动的二进制代码或电路板纹理。
*   **大致大小**: 建议为 `1920x1080` 像素或更高分辨率，以适应不同屏幕尺寸。
*   **存放位置**: `frontend/public/assets/backgrounds/`

## 3. 物体图片 (Objects)

所有可交互的静态或动态物体。每个物体可能需要多个状态的图片，以像素风格绘制。

*   **内容**:
    *   **门**:
        *   `door_closed.png`: 一扇紧闭的厚重石门，表面有古老的雕刻。
        *   `door_open.png`: 石门向内敞开，露出黑暗的通道。
        *   `door_locked.png`: 石门上有一个明显的锁孔或符文锁。
    *   **按钮**:
        *   `button_off.png`: 一个未被按下的圆形或方形按钮，颜色暗淡。
        *   `button_on.png`: 按钮被按下，发出微光或改变颜色。
        *   `button_red.png`: 红色按钮，未按下状态。
        *   `button_blue.png`: 蓝色按钮，未按下状态。
    *   **水晶**:
        *   `crystal_inactive.png`: 一颗透明或暗淡的水晶，没有光泽。
        *   `crystal_active.png`: 水晶发出明亮的光芒，颜色鲜艳。
        *   `crystal_broken.png`: 水晶破碎成几块，失去光泽。
    *   **镜子**:
        *   `mirror_clean.png`: 一面清晰的镜子，反射出模糊的场景。
        *   `mirror_cracked.png`: 镜子表面有裂痕。
    *   **书籍**:
        *   `book_closed.png`: 一本合上的厚重古书。
        *   `book_open.png`: 书籍翻开，显示模糊的文字或图案。
        *   `book_glowing.png`: 书籍发出微弱的光芒，可能暗示其重要性。
    *   **容器**:
        *   `container_empty.png`: 一个空的木箱或石罐。
        *   `container_full.png`: 容器中装有物品（如发光的药水、钥匙等）。
    *   **光源**:
        *   `light_off.png`: 一个熄灭的火把或灯笼。
        *   `light_on.png`: 火把或灯笼发出温暖的光芒。
    *   **钥匙**:
        *   `key_bronze.png`: 一把古朴的青铜钥匙。
        *   `key_silver.png`: 一把闪亮的银色钥匙。
        *   `key_gold.png`: 一把华丽的金色钥匙。
*   **大致大小**: 根据物体在场景中的重要性和大小，建议 `100x100` 到 `400x400` 像素不等。关键物体可以更大。
*   **存放位置**: `frontend/public/assets/objects/`

## 4. 角色图片 (Entities)

所有具有简单 AI 的角色。每个角色可能需要多个行为或状态的图片，以像素风格绘制。

*   **内容**:
    *   **守卫**:
        *   `guard_patrolling.png`: 身穿盔甲的守卫，手持武器，正在巡逻。
        *   `guard_alert.png`: 守卫警惕地看向某个方向，可能摆出防御姿态。
        *   `guard_sleeping.png`: 守卫靠墙睡着，武器放在一旁。
        *   `guard_hostile.png`: 守卫举起武器，面露敌意。
    *   **向导**:
        *   `guide_standing.png`: 一个神秘的人物，身披斗篷，静静站立。
        *   `guide_talking.png`: 向导做出说话的姿态，可能伴有手势。
        *   `guide_disappearing.png`: 向导身体逐渐透明，即将消失。
    *   **幽灵**:
        *   `ghost_idle.png`: 一个半透明的幽灵，在空中缓慢飘浮。
        *   `ghost_moving.png`: 幽灵快速移动，留下残影。
        *   `ghost_transparent.png`: 幽灵几乎完全透明，难以察觉。
    *   **机械体**:
        *   `robot_idle.png`: 一个金属质感的机器人，静止不动，眼睛发出微光。
        *   `robot_moving.png`: 机器人移动，关节处有机械运动的痕迹。
        *   `robot_broken.png`: 机器人倒在地上，冒出火花或烟雾。
*   **大致大小**: 建议 `150x250` 到 `300x500` 像素，以保持角色在场景中的可见性。
*   **存放位置**: `frontend/public/assets/entities/`

## 5. 环境状态图标/效果 (States)

用于视觉化表示环境状态的变化，以像素风格绘制。

*   **内容**:
    *   **光明/黑暗**:
        *   `state_light.png`: 一个柔和的光照叠加效果，使场景变亮。
        *   `state_dark.png`: 一个半透明的黑色叠加层，使场景变暗。
    *   **寂静/嘈杂**:
        *   `state_silent.png`: 一个带有交叉线的音符图标，表示寂静。
        *   `state_noisy.png`: 多个声波图案的图标，表示嘈杂。
    *   **有序/混乱**:
        *   `state_order.png`: 多个整齐排列的齿轮或方块图标，表示有序。
        *   `state_chaos.png`: 破碎的几何图形或随机散落的碎片图标，表示混乱。
*   **大致大小**: 图标类 `50x50` 像素，全屏效果类 `1920x1080` 像素。
*   **存放位置**: `frontend/public/assets/states/`

## 6. 规则节点图片 (Rule Nodes)

玩家触碰后可获得规则提示的视觉元素，以像素风格绘制。

*   **内容**:
    *   `rune_floating.png`: 一个漂浮在空中的发光符文。
    *   `tablet_glowing.png`: 一块刻有文字并发出微光的石碑。
    *   `scroll_mysterious.png`: 一个卷起的神秘卷轴。
    *   `hologram_rule.png`: 一个蓝色或绿色调的全息投影，显示抽象符号。
*   **大致大小**: 建议 `80x80` 到 `200x200` 像素。
*   **存放位置**: `frontend/public/assets/rules/`

## 7. UI 界面元素 (UI)

游戏界面的通用组件，以像素风格绘制。

*   **内容**:
    *   **按钮**:
        *   `button_normal.png`: 标准按钮样式，如一个带有边框的矩形。
        *   `button_hover.png`: 鼠标悬停在按钮上时的样式，可能颜色变亮或有边框发光效果。
        *   `button_pressed.png`: 按钮被按下时的样式，可能颜色变暗或有凹陷效果。
    *   **面板背景**:
        *   `panel_background.png`: 用于规则面板、线索面板、AI 回应面板等的背景纹理，可以是带有像素纹理的半透明矩形。
    *   **图标**:
        *   `icon_observe.png`: 眼睛或放大镜图标。
        *   `icon_move.png`: 箭头或脚印图标。
        *   `icon_interact.png`: 手指点击或齿轮图标。
        *   `icon_declare.png`: 对话气泡或卷轴图标。
        *   `icon_challenge.png`: 闪电或破碎的盾牌图标。
    *   **加载动画**:
        *   `loading_spinner.gif`: 一个像素风格的旋转加载图标。
        *   `loading_bar.png`: 一个像素风格的加载进度条。
*   **大致大小**: 按钮 `60x40` 像素，面板背景可根据需要调整，图标 `32x32` 像素。
*   **存放位置**: `frontend/public/assets/ui/`

## 8. 动态元素状态管理与素材

前端界面需要能够动态改变界面中元素的可见性、位置、图片源等。这意味着对于每种可能的状态，都需要有对应的像素风格视觉素材。

**示例：守卫的状态变化**

如果守卫有“巡逻”、“警惕”、“沉睡”三种状态，则需要：
*   `guard_patrolling.png`: 守卫在巡逻时的像素图。
*   `guard_alert.png`: 守卫处于警惕状态时的像素图。
*   `guard_sleeping.png`: 守卫睡着时的像素图。

前端将根据后端返回的游戏状态，动态加载并显示对应的图片。

**示例：物体状态变化**

如果水晶有“未激活”、“已激活”、“破损”三种状态，则需要：
*   `crystal_inactive.png`: 未激活水晶的像素图。
*   `crystal_active.png`: 激活状态水晶的像素图。
*   `crystal_broken.png`: 破碎水晶的像素图。

## 9. 2D/3D 组件选择

考虑到游戏的核心概念是“抽象空间”和“不断变化的迷宫”，以及动态规则和组件的叠加，一个 **2D 叠加系统** 是最灵活和高效的选择。

*   **优势**:
    *   **开发速度快**: 2D 渲染和定位相对简单。
    *   **素材制作成本低**: 2D 像素图片制作比 3D 模型更直接。
    *   **灵活性高**: 容易实现图片叠加、状态切换、位置调整。
    *   **适应性强**: 方便实现响应式布局，适应手机和电脑。

*   **实现方式建议**:
    *   使用 CSS Grid 或 Flexbox 布局来构建基础场景容器。
    *   通过绝对定位 (`position: absolute;`) 将物体和角色图片��加到背景图上。
    *   使用 Vue 的 `:style` 绑定来动态控制元素的 `left`, `top`, `width`, `height`, `z-index` 等属性，实现位置和大小的调整。
    *   使用 `:src` 绑定动态切换图片源，以反映元素状态。
    *   考虑使用一些轻量级的 2D 动画库（如 GreenSock (GSAP) 或 Vue 的 `<Transition>` 组件）来实现平滑的移动、淡入淡出等效果。

**结论**: 建议采用 2D 叠加的方式来控制元素位置和状态，这能更好地满足当前项目的需求和迭代速度。