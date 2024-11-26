from typing import Any
from pymunk import Arbiter, Body, CollisionHandler, Shape, Space


class GameSpace:


    

    __spaceInstance: Space = None
    __handler: CollisionHandler = None

    @staticmethod
    def initSpace():
        """
        初始化物理世界
        """
        if GameSpace.__spaceInstance is None:
            GameSpace.__spaceInstance = Space()
            # 物体每秒保留多少速度
            GameSpace.__spaceInstance.damping = 0
            # GameSpace.__handler = GameSpace.__spaceInstance.add_collision_handler(
            #     GameSpace.TANK_COLLISION_TYPE, GameSpace.BULLET_COLLISION_TYPE
            # )
            # GameSpace.__handler.post_solve = GameSpace._collisionHandler

    def getSpace():
        if GameSpace.__spaceInstance is None:
            GameSpace.initSpace()
        return GameSpace.__spaceInstance

    @staticmethod
    def updateSpace(delta: float):
        GameSpace.__spaceInstance.step(delta)
        pass

    # @staticmethod
    # def _collisionHandler(arbiter: Arbiter, space: Space, data: dict[Any, Any]):
    #     if(arbiter.is_first_contact):
    #         for shape in arbiter.shapes:
    #             body : Body = shape.body
    #             GameSpace.__spaceInstance.remove(shape.body,*body.shapes)
    #     # return True
