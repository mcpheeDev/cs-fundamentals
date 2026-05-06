from game import Warrior, Mage, Rogue, Weapon, Armour, Potion, Combat

passed = 0
failed = 0

def test(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        failed += 1

def test_true(name, condition):
    test(name, condition, True)

def test_raises(name, fn, error_type):
    global passed, failed
    try:
        fn()
        print(f"  ✗  {name}  (no exception raised)")
        failed += 1
    except error_type:
        print(f"  ✓  {name}")
        passed += 1


print("\n── Character stats ──────────────────────────────────")
w = Warrior("Thor")
m = Mage("Merlin")
r = Rogue("Shadow")

test("warrior max hp", w.max_hp, 120)
test("warrior hp starts full", w.hp, 120)
test("mage max hp", m.max_hp, 70)
test("rogue max hp", r.max_hp, 90)
test("warrior is alive", w.is_alive, True)

print("\n── Encapsulation ────────────────────────────────────")
test_raises("hp not directly accessible",
            lambda: w.__hp, AttributeError)

print("\n── Damage and healing ───────────────────────────────")
w2 = Warrior("Test")
actual = w2.take_damage(10)
test_true("take_damage returns positive int", actual > 0)
test_true("hp reduced after damage", w2.hp < w2.max_hp)
test_true("hp never below 0", w2.hp >= 0)

w3 = Warrior("Healer")
w3.take_damage(50)
hp_before = w3.hp
healed = w3.heal(20)
test("heal increases hp", w3.hp, hp_before + healed)

w4 = Warrior("Full")
healed = w4.heal(999)
test("heal caps at max_hp", w4.hp, w4.max_hp)
test("heal returns actual amount healed", healed, 0)

print("\n── Weapons and armour ───────────────────────────────")
w5 = Warrior("Armed")
base_atk = w5.attack
sword = Weapon("Sword", attack_bonus=10, value=100)
sword.use(w5)
test("weapon increases attack", w5.attack, base_atk + 10)

shield = Armour("Shield", defence_bonus=5, value=80)
base_def = w5.defence
shield.use(w5)
test("armour increases defence", w5.defence, base_def + 5)

print("\n── Potion ───────────────────────────────────────────")
w6 = Warrior("Injured")
w6.take_damage(40)
hp_before = w6.hp
potion = Potion("Elixir", heal_amount=30, value=50)
w6.pick_up(potion)
w6.use_item("Elixir")
test_true("potion heals character", w6.hp > hp_before)

print("\n── Warrior passive ──────────────────────────────────")
w7 = Warrior("Tough")
# Give 100 raw damage — warrior should take less due to 15% reduction
# and defence. Just check it takes less than 100.
actual = w7.take_damage(100)
test_true("warrior takes less than raw damage", actual < 100)

print("\n── Calculate damage returns correct format ──────────")
for char in [Warrior("A"), Mage("B"), Rogue("C")]:
    result = char.calculate_damage()
    test_true(f"{char.__class__.__name__} calculate_damage returns tuple",
              isinstance(result, tuple) and len(result) == 2)
    test_true(f"{char.__class__.__name__} damage is positive int",
              isinstance(result[0], int) and result[0] > 0)
    test_true(f"{char.__class__.__name__} description is string",
              isinstance(result[1], str))

print("\n── Status bar ───────────────────────────────────────")
bar = Warrior("BarTest").status_bar()
test_true("status bar is a string", isinstance(bar, str))
test_true("status bar contains name", "BarTest" in bar)
test_true("status bar contains hp", "120" in bar)

print("\n── Combat ───────────────────────────────────────────")
fighter1 = Warrior("W1")
fighter2 = Rogue("R1")
combat = Combat(fighter1, fighter2)
winner = combat.run()
test_true("combat returns a winner", winner is not None)
test_true("winner is alive", winner.is_alive)

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
