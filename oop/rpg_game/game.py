"""
game.py — A turn-based RPG demonstrating the full OOP hierarchy:
  Character (base)
    ├── Warrior   — high HP, physical attacks
    ├── Mage      — low HP, powerful spells
    └── Rogue     — medium HP, critical hit chance

  Item (base)
    ├── Weapon    — increases attack
    ├── Armour    — increases defence
    └── Potion    — restores HP

Demonstrates: classes, inheritance, encapsulation, polymorphism,
              operator overloading, class methods, static methods.

Run:  python3 game.py
"""

import random
from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════════════════
# ITEMS
# ══════════════════════════════════════════════════════════════════════════════

class Item(ABC):
    """Abstract base class for all items."""

    def __init__(self, name, description, value):
        self._name        = name
        self._description = description
        self._value       = value   # gold value

    @property
    def name(self):        return self._name
    @property
    def description(self): return self._description
    @property
    def value(self):       return self._value

    @abstractmethod
    def use(self, character):
        """Apply the item's effect to a character."""

    def __str__(self):
        return f"{self._name} ({self._description})"


class Weapon(Item):
    def __init__(self, name, attack_bonus, value):
        super().__init__(name, f"+{attack_bonus} ATK", value)
        self._attack_bonus = attack_bonus

    @property
    def attack_bonus(self): return self._attack_bonus

    def use(self, character):
        character.equip_weapon(self)
        print(f"  ⚔  {character.name} equips {self.name}")


class Armour(Item):
    def __init__(self, name, defence_bonus, value):
        super().__init__(name, f"+{defence_bonus} DEF", value)
        self._defence_bonus = defence_bonus

    @property
    def defence_bonus(self): return self._defence_bonus

    def use(self, character):
        character.equip_armour(self)
        print(f"  🛡  {character.name} equips {self.name}")


class Potion(Item):
    def __init__(self, name, heal_amount, value):
        super().__init__(name, f"Restores {heal_amount} HP", value)
        self._heal_amount = heal_amount

    def use(self, character):
        healed = character.heal(self._heal_amount)
        print(f"  💊  {character.name} drinks {self.name} and restores {healed} HP")


# ══════════════════════════════════════════════════════════════════════════════
# CHARACTERS
# ══════════════════════════════════════════════════════════════════════════════

class Character(ABC):
    """Abstract base class for all characters."""

    _total_characters = 0   # class variable — shared across all instances

    def __init__(self, name, max_hp, attack, defence):
        self._name       = name
        self._max_hp     = max_hp
        self._hp         = max_hp
        self._base_atk   = attack
        self._base_def   = defence
        self._weapon     = None
        self._armour     = None
        self._inventory  = []
        self._gold       = random.randint(10, 50)
        Character._total_characters += 1

    # ── Properties (encapsulation) ────────────────────────────────────────────
    @property
    def name(self):    return self._name
    @property
    def hp(self):      return self._hp
    @property
    def max_hp(self):  return self._max_hp
    @property
    def is_alive(self): return self._hp > 0

    @property
    def attack(self):
        base = self._base_atk
        return base + (self._weapon.attack_bonus if self._weapon else 0)

    @property
    def defence(self):
        base = self._base_def
        return base + (self._armour.defence_bonus if self._armour else 0)

    # ── Class / static methods ────────────────────────────────────────────────
    @classmethod
    def total_created(cls):
        return cls._total_characters

    @staticmethod
    def roll_dice(sides=6, count=1):
        return sum(random.randint(1, sides) for _ in range(count))

    # ── Equipment & inventory ─────────────────────────────────────────────────
    def equip_weapon(self, weapon):  self._weapon = weapon
    def equip_armour(self, armour):  self._armour = armour

    def pick_up(self, item):
        self._inventory.append(item)

    def use_item(self, item_name):
        for item in self._inventory:
            if item.name.lower() == item_name.lower():
                item.use(self)
                if isinstance(item, Potion):
                    self._inventory.remove(item)
                return
        print(f"  {self._name} doesn't have '{item_name}'")

    # ── Combat ────────────────────────────────────────────────────────────────
    @abstractmethod
    def calculate_damage(self):
        """Return (damage, description) — subclasses define their attack style."""

    def take_damage(self, raw_damage):
        """Apply damage after defence reduction. Return actual damage taken."""
        actual = max(1, raw_damage - self.defence)
        self._hp = max(0, self._hp - actual)
        return actual

    def heal(self, amount):
        """Heal HP, capped at max_hp. Return actual amount healed."""
        before = self._hp
        self._hp = min(self._max_hp, self._hp + amount)
        return self._hp - before

    def attack_target(self, target):
        """Perform an attack on target. Returns (damage_dealt, description)."""
        damage, desc = self.calculate_damage()
        actual = target.take_damage(damage)
        return actual, desc

    # ── Status ────────────────────────────────────────────────────────────────
    def status_bar(self):
        filled = int(self._hp / self._max_hp * 20)
        bar = "█" * filled + "░" * (20 - filled)
        return f"{self._name:<12} HP [{bar}] {self._hp:>3}/{self._max_hp}"

    def __str__(self):
        cls  = self.__class__.__name__
        wpn  = self._weapon.name if self._weapon else "none"
        arm  = self._armour.name if self._armour else "none"
        return (f"{cls}: {self._name}  HP={self._hp}/{self._max_hp}  "
                f"ATK={self.attack}  DEF={self.defence}  "
                f"Weapon={wpn}  Armour={arm}")


class Warrior(Character):
    """High HP, consistent physical damage, passive damage reduction."""

    def __init__(self, name):
        super().__init__(name, max_hp=120, attack=15, defence=8)
        self._rage = 0   # builds up, boosts next attack

    def calculate_damage(self):
        self._rage = min(self._rage + 5, 30)
        dmg = self.attack + self.roll_dice(8) + self._rage // 10
        return dmg, f"⚔  {self.name} strikes for"

    def take_damage(self, raw_damage):
        """Warriors reduce incoming damage by 15% (Fortitude passive)."""
        reduced = int(raw_damage * 0.85)
        return super().take_damage(reduced)


class Mage(Character):
    """Low HP, high burst magic damage, mana resource."""

    SPELLS = [
        ("Fireball",      20, 6),
        ("Ice Lance",     15, 4),
        ("Thunder Bolt",  25, 8),
        ("Arcane Blast",  18, 5),
    ]

    def __init__(self, name):
        super().__init__(name, max_hp=70, attack=8, defence=3)
        self._max_mana = 60
        self._mana     = 60

    def calculate_damage(self):
        available = [(n, d, c) for n, d, c in self.SPELLS if c <= self._mana]
        if not available:
            self._mana += 10   # regenerate
            return self.attack + self.roll_dice(4), f"🪄  {self.name} casts a weak bolt for"
        spell_name, base_dmg, cost = random.choice(available)
        self._mana -= cost
        dmg = base_dmg + self.attack + self.roll_dice(10)
        return dmg, f"✨  {self.name} casts {spell_name} for"


class Rogue(Character):
    """Medium HP, chance to critically strike (3× damage)."""

    CRIT_CHANCE = 0.30   # 30% crit rate

    def __init__(self, name):
        super().__init__(name, max_hp=90, attack=12, defence=5)

    def calculate_damage(self):
        base = self.attack + self.roll_dice(6)
        if random.random() < self.CRIT_CHANCE:
            return base * 3, f"🗡  CRITICAL! {self.name} backstabs for"
        return base, f"🗡  {self.name} slashes for"


# ══════════════════════════════════════════════════════════════════════════════
# COMBAT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class Combat:
    """Manages a turn-based battle between two characters."""

    def __init__(self, fighter_a, fighter_b):
        self.fighters = [fighter_a, fighter_b]

    def _print_status(self):
        print()
        for f in self.fighters:
            print(f"  {f.status_bar()}")
        print()

    def run(self, max_rounds=20):
        a, b = self.fighters
        print(f"\n{'═'*55}")
        print(f"  ⚔  {a.name}  vs  {b.name}  ⚔")
        print(f"{'═'*55}")
        self._print_status()

        for round_num in range(1, max_rounds + 1):
            print(f"  --- Round {round_num} ---")
            for attacker, defender in [(a, b), (b, a)]:
                if not attacker.is_alive or not defender.is_alive:
                    continue
                dmg, desc = attacker.attack_target(defender)
                print(f"  {desc} {dmg} damage  "
                      f"(defender HP: {defender.hp}/{defender.max_hp})")

            self._print_status()

            if not a.is_alive or not b.is_alive:
                winner = a if a.is_alive else b
                loser  = b if a.is_alive else a
                print(f"  🏆  {winner.name} wins! {loser.name} is defeated.\n")
                return winner

        print("  ⏱  Draw — max rounds reached.")
        return None


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create characters
    warrior = Warrior("Thor")
    mage    = Mage("Merlin")
    rogue   = Rogue("Shadow")

    # Give them gear
    sword   = Weapon("Excalibur",    attack_bonus=10, value=500)
    staff   = Weapon("Elder Staff",  attack_bonus=8,  value=400)
    potion  = Potion("Health Elixir", heal_amount=30, value=50)
    shield  = Armour("Dragon Shield", defence_bonus=6, value=300)

    sword.use(warrior)
    staff.use(mage)
    shield.use(warrior)
    warrior.pick_up(potion)

    print("\nCharacter stats:")
    for c in [warrior, mage, rogue]:
        print(f"  {c}")

    print(f"\nTotal characters created: {Character.total_created()}")

    # Fight 1: Warrior vs Mage
    combat1 = Combat(warrior, mage)
    combat1.run()

    # Fight 2: Warrior vs Rogue (warrior may be damaged from fight 1)
    warrior2 = Warrior("Achilles")
    sword.use(warrior2)
    combat2 = Combat(warrior2, rogue)
    combat2.run()
