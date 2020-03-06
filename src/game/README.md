# UNO - 先锋规则

# 卡片
![uno](https://upload.wikimedia.org/wikipedia/commons/9/95/UNO_cards_deck.svg)

每副牌共有108张，每张牌都有一个index标号和face牌面。
标号index是一个整数，意义是这张牌是同face牌中的第几张牌。

face牌面在Card类中表现为三点：
- 颜色
- 功能
- 值

*index是一个一位整数*
对于face值都为红2的牌来说，index为1就代表这是第一张红2牌，为2就代表这是第二张红2牌，以此类推。每副牌中一共有两张红二牌、

# player

这里的player是游戏意义上的player，并不拥有昵称、id等乱七八糟的东西，
而是作为一局游戏的参与者而存在的一个抽象实体，拥有手牌并可以摸牌和出牌。

player有摸牌draw和出牌put两个方法，在player的一个游戏回合中，他可以做出
最多两个操作，一次摸牌一次出牌。

# action

游戏行为并不包括喊uno等乱七八糟的东西，而是玩家在自己的回合内进行的纯粹和游戏有关系的行为，
分为出牌put和摸牌draw。注意，根据先锋规则，摸牌后也可以出牌，因此玩家在一个回合内至多可以
进行两个游戏行为action