# UNO - 先锋规则

# 卡片
![uno](https://upload.wikimedia.org/wikipedia/commons/9/95/UNO_cards_deck.svg)

每副牌共有108张，每张牌都有一个index标号和face牌面。

face牌面在Card类中表现为三点：
- 颜色
- 功能
- 值

*index是一个一位整数*，一共有108张牌，一副牌可以产生108个不同的index。
index在同一局游戏重新洗牌过后不会被重置，而是从上一局index的最后开始增加，
最终在同一局游戏中，不会有两个index完全一致的牌。


所有黑色牌在出牌之前都应该由出牌者指定颜色，但抽到手的牌可以是黑色。

# player

这里的player是游戏意义上的player，并不拥有昵称、id等乱七八糟的东西，
而是作为一局游戏的参与者而存在的一个抽象实体，拥有手牌并可以摸牌和出牌。

player有摸牌draw和出牌put两个方法，在player的一个游戏回合中，他可以做出
最多两个操作，一次摸牌一次出牌。

player还有切牌cut和过go方法，切牌使得玩家可以在拥有和出牌人所出的牌相同的牌的时候，
优先于出牌人的下家而打出自己与出牌人所出的牌相同的那张牌，让游戏从自己的座位seat开始的行为。

当player出的牌是自己的最后一张牌的时候，玩家的“出牌put”方法会返回True。
调用玩家出牌的调用者可以拿到这个值。
当游戏对象Game意识到玩家已经出了最后一张牌的时候，会在执行把玩家对象

player还有“胜利_win”方法。当玩家出完最后一张牌的时候，玩家立即执行自己的“胜利”方法，
此方法将玩家Player本身作为参数传递给游戏对象game的胜利win方法，游戏会从玩家列表里删除该玩家。



# action

玩家在他的一个回合里可以进行三种操作，“摸牌”、“出牌”和“过”。
根据先锋规则玩家可以这样操作：
- 出牌 - 自动结束
- 摸牌 - 出牌 - 自动结束
- 摸牌 - 过

由此可见，一个回合总是以“出牌”或者“过”而结束的。

一局游戏中，如果玩家选择去“摸牌”，那么他绝对不能指定自己应该摸几张牌——他摸牌的数量一定
等于系统需要他摸牌的数量。比如加牌（的叠加（yunqi的爱心传递~ 因此“摸牌”是一个单独的方法，
玩家对象从游戏实例中摸到的牌的数量总是和游戏当前的状态有关系的。

# game

游戏对象是抽象的一局游戏。
在这个抽象的游戏开始的时候，你不应该给它指定游戏的进行顺序和玩家的编号——而是应该把这些
作为顶层实例的底层部分与真实的玩家一一对应。你可以通过直接获取对象属性的方法来获知玩家的手牌。