# TankGame

## 📄介绍

![](https://img.shields.io/badge/Python%203.12.7-3776AB?style=for-the-badge&logo=python&logoColor=white)

使用`Python`库
- `pygame`
- `pymunk`
- `loguru`

## 操作说明

**主玩家**

- `WASD` 移动

- `G` 射击

**副玩家**

- `方向键` 移动
- `[0]` 射击

## 游戏道具类型

- ### 幽灵武器道具

    幽灵武器，子弹穿墙并在飞行过程中加速

- ### 遥控导弹道具

    发射遥控导弹，发射后坦克无法移动，转而移动导弹，再次发射即可取消

- ### 破片弹武器道具

    发射破片炮弹，在命中目标或超过一定时间后爆炸，发射范围型破片，在爆炸范围内的坦克会被立刻摧毁