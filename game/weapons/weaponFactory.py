from enum import Enum
from game.gameObject import GameObject
from game.weapons.weapon import Weapon


class WEAPON_TYPE(Enum):
    COMMON_WEAPON = 0
    GHOST_WEAPON = 1
    MISSILE_WEAPON = 2
    FRAGMENTBOMB_WEAPON = 3


class WeaponFactory:

    def __init__(self):
        raise NotImplementedError("WeaponFactory类不允许初始化")

    @staticmethod
    def createWeapon(owner: GameObject, weaponType: WEAPON_TYPE) -> Weapon:
        from game.weapons.commonWeapon import CommonWeapon
        from game.weapons.ghostWeapon import GhostWeapon
        from game.weapons.remoteControlMissileWeapon import RemoteControlMissileWeapon
        from game.weapons.fragmentBombWeapon import FragmentBombWeapon

        weaponList: list[type[Weapon]] = [CommonWeapon, GhostWeapon, RemoteControlMissileWeapon,FragmentBombWeapon]
        return weaponList[weaponType.value](owner)
