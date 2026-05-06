from abc import ABC, abstractmethod
import random


# ══════════════════════════════════════════════════════════════════════════════
# ITEMS
# ══════════════════════════════════════════════════════════════════════════════

class Item(ABC):
    def __init__(self, name, description, value):
        # TODO: store name, description, value
        pass

    @abstractmethod
    def use(self, character):
        """Apply this item's effect to character."""
        pass

    def __str__(self):
        # TODO: return "Name (description)"
        pass


class Weapon(Item):
    def __init__(self, name, attack_bonus, value):
        # TODO: call super().__init__ and store attack_bonus
        pass

    def use(self, character):
        # TODO: call character.equip_weapon(self)
        pass


class Armour(Item):
    def __init__(self, name, defence_bonus, value):
        # TODO
        pass

    def use(self, character):
        # TODO: call character.equip_armour(self)
        pass


class Potion(Item):
    def __init__(self, name, heal_amount, value):
        # TODO
        pass

    def use(self, character):
        # TODO: heal the character, print how much was healed
        pass


# ══════════════════════════════════════════════════════════════════════════════
# CHARACTERS
# ══════════════════════════════════════════════════════════════════════════════

class Character(ABC):
    def __init__(self, name, max_hp, attack, defence):
        # TODO: store all attributes as PRIVATE (__name, __hp, etc.)
        # hp starts equal to max_hp
        # _weapon and _armour start as None
        # _inventory starts as empty list
        pass

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def name(self):
        # TODO
        pass

    @property
    def hp(self):
        # TODO
        pass

    @property
    def max_hp(self):
        # TODO
        pass

    @property
    def is_alive(self):
        # TODO: return True if hp > 0
        pass

    @property
    def attack(self):
        # TODO: base attack + weapon bonus (if equipped)
        pass

    @property
    def defence(self):
        # TODO: base defence + armour bonus (if equipped)
        pass

    # ── Equipment ─────────────────────────────────────────────────────────────
    def equip_weapon(self, weapon):
        # TODO
        pass

    def equip_armour(self, armour):
        # TODO
        pass

    def pick_up(self, item):
        # TODO: add item to _inventory
        pass

    def use_item(self, item_name):
        # TODO: find item in inventory by name, call item.use(self)
        # remove potions after use
        # print a message if item not found
        pass

    # ── Combat ────────────────────────────────────────────────────────────────
    @abstractmethod
    def calculate_damage(self):
        """Return (damage_amount, description_string)."""
        pass

    def take_damage(self, raw_damage):
        # TODO: subtract (raw_damage - defence) from hp, minimum 1 damage
        # hp never goes below 0
        # return actual damage dealt
        pass

    def heal(self, amount):
        # TODO: add amount to hp, cap at max_hp
        # return how much was actually healed
        pass

    def attack_target(self, target):
        # TODO: call self.calculate_damage()
        # call target.take_damage() with the result
        # return (damage_dealt, description)
        pass

    def status_bar(self):
        # TODO: return a string like:
        # "Thor        HP [████████████░░░░░░░░] 80/120"
        # bar should be 20 chars wide, filled proportionally
        pass

    def __str__(self):
        return (f"{self.__class__.__name__}: {self.name}  "
                f"HP={self.hp}/{self.max_hp}  "
                f"ATK={self.attack}  DEF={self.defence}")


class Warrior(Character):
    def __init__(self, name):
        # TODO: call super with appropriate stats
        # max_hp=120, attack=15, defence=8
        # add a self._rage = 0 attribute
        pass

    def calculate_damage(self):
        # TODO: base damage = self.attack + random 1-8
        # increase rage by 5 each attack (max 30)
        # add rage // 10 to damage
        # return (damage, "⚔  Name strikes for")
        pass

    def take_damage(self, raw_damage):
        # TODO: Warriors reduce incoming damage by 15% before calling super
        pass


class Mage(Character):
    SPELLS = [
        ("Fireball",     20, 6),
        ("Ice Lance",    15, 4),
        ("Thunder Bolt", 25, 8),
        ("Arcane Blast", 18, 5),
    ]

    def __init__(self, name):
        # TODO: call super with max_hp=70, attack=8, defence=3
        # add self._mana = 60
        pass

    def calculate_damage(self):
        # TODO: filter SPELLS to those with cost <= self._mana
        # if none available, regenerate 10 mana and do a weak attack
        # otherwise pick a random available spell
        # subtract spell cost from mana
        # return (damage, "✨  Name casts SpellName for")
        pass


class Rogue(Character):
    CRIT_CHANCE = 0.30

    def __init__(self, name):
        # TODO: call super with max_hp=90, attack=12, defence=5
        pass

    def calculate_damage(self):
        # TODO: base damage = self.attack + random 1-6
        # 30% chance to crit: multiply damage by 3
        # return different descriptions for crit vs normal
        pass


# ══════════════════════════════════════════════════════════════════════════════
# COMBAT
# ══════════════════════════════════════════════════════════════════════════════

class Combat:
    def __init__(self, fighter_a, fighter_b):
        # TODO: store the two fighters
        pass

    def run(self, max_rounds=30):
        # TODO:
        # print a header showing both fighters
        # loop up to max_rounds:
        #   each fighter attacks the other (if both alive)
        #   print status bars after each round
        #   if either fighter is dead, declare winner and return them
        # if max_rounds reached with no winner, declare a draw
        pass


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    warrior = Warrior("Thor")
    mage    = Mage("Merlin")
    rogue   = Rogue("Shadow")

    sword  = Weapon("Excalibur",    attack_bonus=10, value=500)
    staff  = Weapon("Elder Staff",  attack_bonus=8,  value=400)
    potion = Potion("Health Elixir", heal_amount=30, value=50)

    sword.use(warrior)
    staff.use(mage)
    warrior.pick_up(potion)

    print("=== Fight 1: Warrior vs Mage ===")
    combat = Combat(warrior, mage)
    combat.run()

    print("\n=== Fight 2: Warrior vs Rogue ===")
    warrior2 = Warrior("Achilles")
    sword.use(warrior2)
    combat2 = Combat(warrior2, rogue)
    combat2.run()
