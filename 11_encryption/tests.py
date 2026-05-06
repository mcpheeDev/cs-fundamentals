from encryption import (caesar_encrypt, caesar_decrypt, caesar_brute_force,
                         vigenere_encrypt, vigenere_decrypt, guess_key_length,
                         crack_vigenere)

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


print("\n── Caesar ────────────────────────────────────────────")
test("shift 1",  caesar_encrypt("ABC", 1),  "BCD")
test("shift 13", caesar_encrypt("ABC", 13), "NOP")
test("wrap Z",   caesar_encrypt("XYZ", 3),  "ABC")
test("lowercase", caesar_encrypt("abc", 1), "bcd")
test("non-alpha unchanged", caesar_encrypt("Hello, World!", 1), "Ifmmp, Xpsme!")

for shift in [1, 7, 13, 25]:
    text = "The Quick Brown Fox"
    enc = caesar_encrypt(text, shift)
    dec = caesar_decrypt(enc, shift)
    test(f"round-trip shift={shift}", dec, text)

print("\n── Caesar brute force ────────────────────────────────")
plaintext = "the cat sat on the mat"
enc = caesar_encrypt(plaintext, 7)
candidates = caesar_brute_force(enc)
test_true("returns 25 candidates", len(candidates) == 25)
shifts = [s for s, _ in candidates]
test_true("correct shift in results", 7 in shifts)
test_true("correct shift is top result", candidates[0][0] == 7)

print("\n── Vigenère ──────────────────────────────────────────")
for text, key in [("HELLOWORLD", "KEY"), ("attackatdawn", "LEMON")]:
    enc = vigenere_encrypt(text, key)
    dec = vigenere_decrypt(enc, key)
    test(f"round-trip key={key}", dec.upper(), text.upper())

# Non-alpha unchanged
test("spaces unchanged", vigenere_encrypt("Hello World", "KEY")[5], " ")

print("\n── Vigenère crack ────────────────────────────────────")
# Use a long text so frequency analysis has enough data
long_text = ("the cat sat on the mat the fat cat ate the rat "
             "a cat a mat a rat the cat sat flat ") * 5
key = "CAT"
enc = vigenere_encrypt(long_text, key)
lengths = guess_key_length(enc)
test_true("correct key length in top 3", 3 in lengths[:3])
guessed = crack_vigenere(enc, 3)
test_true("cracked key is a string", isinstance(guessed, str))
test_true("cracked key has correct length", len(guessed) == 3)

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
