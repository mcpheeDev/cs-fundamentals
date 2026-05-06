# 05 – RPG Game

## What you're building
A turn-based RPG that demonstrates the full OOP hierarchy. You design
the classes, the combat system, and the game loop.

## The class hierarchy to build

```
Character (abstract base class)
    ├── Warrior    — high HP, physical attacks, passive damage reduction
    ├── Mage       — low HP, powerful spells, mana resource
    └── Rogue      — medium HP, chance to critically strike (3× damage)

Item (abstract base class)
    ├── Weapon     — increases attack stat
    ├── Armour     — increases defence stat
    └── Potion     — restores HP when used
```

## Requirements

### Character
- Private attributes: `__hp`, `__max_hp`, `__attack`, `__defence`
- Properties (getters) for each — no direct attribute access
- `is_alive` property — True if hp > 0
- `take_damage(amount)` — reduce hp, never below 0, return actual damage taken
- `heal(amount)` — restore hp, never above max, return amount healed
- `attack_target(target)` — call `calculate_damage()`, apply to target
- `calculate_damage()` — **abstract** — each subclass defines this differently
- `status_bar()` — print a visual HP bar: `Thor    HP [████████░░░░] 80/120`

### Warrior
- Passive: reduce all incoming damage by 15%
- Rage mechanic: each attack builds rage (max 30), which boosts damage

### Mage
- Has a mana pool (starts at 60)
- Choose from named spells, each with a mana cost
- Regenerate mana if no spells are available

### Rogue
- 30% chance to critically strike for 3× damage
- Print a different message when a crit lands

### Items
- `use(character)` applies the item's effect
- Weapons/Armour: equip to the character (boost their stats)
- Potions: consumed on use (remove from inventory)

### Combat class
- Takes two characters
- Runs turn-based rounds (each attacks once per round)
- Prints status bars after each round
- Declares a winner when one character reaches 0 HP

## Run tests
```bash
python3 tests.py
```
