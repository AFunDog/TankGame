import cProfile
from email.mime import base
from mimetypes import suffix_map
from select import select
from time import sleep
from typing import Any, Callable
from loguru import logger
from pygame import (
    K_DOWN,
    K_ESCAPE,
    K_KP_ENTER,
    K_RETURN,
    K_SPACE,
    K_UP,
    KEYDOWN,
    KSCAN_KP_ENTER,
    Rect,
    Surface,
    gfxdraw,
)
import pygame
from pygame.freetype import Font
from pygame.event import Event
from pymunk import Space
from pygame import image, transform
from game.controls.floatMenu import FloatMenu
from game.controls.selectionControl import Selection, SelectionControl
from game.controls.textbox import TextBox
from game.defines import BACKGROUND, FONT_COLOR, LARGE_TITLE_FONT, SELECTION_HEIGHT
from game.eventManager import EventManager

from game.gameSettings import GlobalSettingsManager
from game.sceneManager import SCENE_TYPE, SceneManager
from game.scenes.scene import Scene
from game.spaces.gameObjectSpace import GAMEOBJECT_SPACE_TYPE, GameObjectSpace
from online.onlineManager import OnlineManager


class StartScene(Scene):

    __ui: Surface
    __background: Surface
    __title: Surface
    # __settingMenu: Surface

    __selectIndex: int = 0
    # __selections: list[tuple[str, Callable[[], None]]]
    # __selectionScale: list[float]

    # __selections: list[SelectionControl]
    __selectionContorl: SelectionControl

    __createServerMenu: FloatMenu
    __connectServerMenu: FloatMenu
    __settingMenu: FloatMenu

    __SELECT_HEIGHT = 72
    __SELECT_SIGN_HEIGHT = 24

    @property
    def ui(self) -> Surface:
        return self.__ui

    def __init__(self):

        selections = [
            Selection(lambda: "本地游戏", SELECTION_HEIGHT, self.__onLocalGameEnter),
            Selection(lambda: "创建服务器", SELECTION_HEIGHT, self.__onCreateServerEnter),
            Selection(lambda: "连接服务器", SELECTION_HEIGHT, self.__onConnectServerEnter),
            Selection(lambda: "设置", SELECTION_HEIGHT, self.__onSettingEnter),
            Selection(lambda: "退出游戏", SELECTION_HEIGHT, self.__onExitGameEnter),
        ]

        self.__ui = Surface((1440, 1280))

        img = image.load("assets/background.png").convert_alpha()
        self.__background = transform.smoothscale_by(
            img, (self.__ui.get_width() + 108) / img.get_width()
        )
        self.__title = LARGE_TITLE_FONT.render("坦 克 动 荡", FONT_COLOR)[0]
        self.__selectionContorl = SelectionControl(
            self.__ui.get_width(),
            StartScene.__SELECT_HEIGHT * len(selections) + 108,
            selections,
        )

        def __downTankSpeed():
            GlobalSettingsManager.getGameSettings().tankSpeed = max(
                100, GlobalSettingsManager.getGameSettings().tankSpeed - 50
            )

        def __upTankSpeed():
            GlobalSettingsManager.getGameSettings().tankSpeed = min(
                2000, GlobalSettingsManager.getGameSettings().tankSpeed + 50
            )

        def __downBulletSpeed():
            GlobalSettingsManager.getGameSettings().commonBulletSpeed = max(
                50, GlobalSettingsManager.getGameSettings().commonBulletSpeed - 50
            )

        def __upBulletSpeed():
            GlobalSettingsManager.getGameSettings().commonBulletSpeed = min(
                1000, GlobalSettingsManager.getGameSettings().commonBulletSpeed + 50
            )

        def __downGhostBulletSpeed():
            GlobalSettingsManager.getGameSettings().ghostBulletSpeed = max(
                50, GlobalSettingsManager.getGameSettings().ghostBulletSpeed - 50
            )

        def __upGhostBulletSpeed():
            GlobalSettingsManager.getGameSettings().ghostBulletSpeed = min(
                1000, GlobalSettingsManager.getGameSettings().ghostBulletSpeed + 50
            )

        def __downGhostSpeedIncreaseRate():
            GlobalSettingsManager.getGameSettings().ghostSpeedIncreaseRate = max(
                0, GlobalSettingsManager.getGameSettings().ghostSpeedIncreaseRate - 0.002
            )

        def __upGhostSpeedIncreaseRate():
            GlobalSettingsManager.getGameSettings().ghostSpeedIncreaseRate = min(
                1, GlobalSettingsManager.getGameSettings().ghostSpeedIncreaseRate + 0.002
            )

        def __downMissileSpeed():
            GlobalSettingsManager.getGameSettings().missileSpeed = max(
                50, GlobalSettingsManager.getGameSettings().missileSpeed - 50
            )

        def __upMissileSpeed():
            GlobalSettingsManager.getGameSettings().missileSpeed = min(
                1000, GlobalSettingsManager.getGameSettings().missileSpeed + 50
            )

        self.__settingMenu = FloatMenu(
            self.__ui,
            1280,
            960,
            SelectionControl(
                1280,
                960,
                [
                    Selection(lambda: "坦克速度与子弹速度并不等价", SELECTION_HEIGHT, lambda: None),
                    Selection(
                        lambda: "坦克移动速度 {}".format(
                            GlobalSettingsManager.getGameSettings().tankSpeed
                        ),
                        SELECTION_HEIGHT,
                        lambda: None,
                        __downTankSpeed,
                        __upTankSpeed,
                    ),
                    Selection(
                        lambda: "子弹速度 {}".format(
                            GlobalSettingsManager.getGameSettings().commonBulletSpeed
                        ),
                        SELECTION_HEIGHT,
                        lambda: None,
                        __downBulletSpeed,
                        __upBulletSpeed,
                    ),
                    Selection(
                        lambda: "幽灵子弹速度 {}".format(
                            GlobalSettingsManager.getGameSettings().ghostBulletSpeed
                        ),
                        SELECTION_HEIGHT,
                        lambda: None,
                        __downGhostBulletSpeed,
                        __upGhostBulletSpeed,
                    ),
                    Selection(
                        lambda: "幽灵子弹速度增长率 {0:.2f}".format(
                            GlobalSettingsManager.getGameSettings().ghostSpeedIncreaseRate * 100
                        ),
                        SELECTION_HEIGHT,
                        lambda: None,
                        __downGhostSpeedIncreaseRate,
                        __upGhostSpeedIncreaseRate,
                    ),
                    Selection(
                        lambda: "导弹速度 {}".format(
                            GlobalSettingsManager.getGameSettings().missileSpeed
                        ),
                        SELECTION_HEIGHT,
                        lambda: None,
                        __downMissileSpeed,
                        __upMissileSpeed,
                    ),
                ],
            ),
        )

        hostTextBox = TextBox("host", "localhost")
        portTextBox = TextBox("port", "8900")

        def __createServer():
            try:
                host = hostTextBox.text
                port = int(portTextBox.text)
                OnlineManager.createServer(host, port)
            except Exception as e:
                logger.exception(e)
                return
            

        self.__createServerMenu = FloatMenu(
            self.__ui,
            1280,
            960,
            SelectionControl(
                1280,
                960,
                [
                    Selection(hostTextBox, SELECTION_HEIGHT),
                    Selection(portTextBox, SELECTION_HEIGHT),
                    Selection(lambda: "创建服务器", SELECTION_HEIGHT, __createServer),
                ],
            ),
        )
        hostTextBox2 = TextBox("host")
        portTextBox2 = TextBox("port", "8900")
        def __connectServer():
            try:
                host = hostTextBox2.text
                port = int(portTextBox2.text)
                OnlineManager.connectServer(host, port)
            except Exception as e:
                logger.exception(e)
                return

        self.__connectServerMenu = FloatMenu(
            self.ui,
            1280,
            960,
            SelectionControl(
                1280,
                960,
                [
                    Selection(hostTextBox2, SELECTION_HEIGHT),
                    Selection(portTextBox2, SELECTION_HEIGHT),
                    Selection(lambda: "连接服务器", SELECTION_HEIGHT, __connectServer),
                ],
            ),
        )

        logger.debug("主菜单场景初始化完成")

    def process(self, event: Event):
        if self.__settingMenu.isMenuShow:
            self.__settingMenu.process(event)
            return
        if self.__createServerMenu.isMenuShow:
            self.__createServerMenu.process(event)
            return
        if self.__connectServerMenu.isMenuShow:
            self.__connectServerMenu.process(event)
            return
        self.__selectionContorl.process(event)

    def update(self, delta: float):
        self.__ui.fill(BACKGROUND)
        self.__ui.blit(
            self.__background, self.__background.get_rect(center=self.__ui.get_rect().center)
        )

        self.__ui.blit(self.__title, ((self.ui.get_width() - self.__title.get_width()) / 2, 48))
        self.__updateSelection(delta)
        self.__updateMenus(delta)

    def __updateSelection(self, delta: float):
        self.__selectionContorl.update(delta)

        self.__ui.blit(
            self.__selectionContorl.ui,
            (
                (self.__ui.get_width() - self.__selectionContorl.ui.get_width()) / 2,
                self.__title.get_height() + 108,
            ),
        )

    def __updateMenus(self, delta: float):
        self.__settingMenu.update(delta)
        self.__createServerMenu.update(delta)
        self.__connectServerMenu.update(delta)

    def __onLocalGameEnter(self):
        SceneManager.changeScene(SCENE_TYPE.GAME_SCENE)

    def __onCreateServerEnter(self):
        # from online.onlineManager import OnlineManager

        # OnlineManager.createServer("127.0.0.1", 8900)
        # logger.debug("创建服务器")
        self.__createServerMenu.show()

    def __onConnectServerEnter(self):
        self.__connectServerMenu.show()

    def __onSettingEnter(self):
        self.__settingMenu.show()

    def __onExitGameEnter(self):
        EventManager.raiseEventType(pygame.QUIT)
