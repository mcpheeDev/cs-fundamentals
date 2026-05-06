from collections import Counter

# ── Caesar Cipher ─────────────────────────────────────────────────────────────

def caesar_encrypt(text, shift):
    """
    TODO: shift every letter by `shift` positions.
    Uppercase stays uppercase, lowercase stays lowercase.
    Non-alphabetic characters are unchanged.
    Wraps around: Z+1 = A.
    """
    pass

def caesar_decrypt(text, shift):
    """TODO: decrypt by shifting in the opposite direction."""
    pass

def caesar_brute_force(ciphertext):
    """
    TODO: try all 25 possible shifts.
    Score each decryption by how English-like it is.

    Simple scoring: count how often the most common English letters
    (e, t, a, o, i, n, s, h, r) appear in the decrypted text.

    Return a list of (shift, decrypted_text) sorted best-first.
    """
    pass


# ── Vigenère Cipher ────────────────────────────────────────────────────────────

def vigenere_encrypt(text, key):
    """
    TODO: encrypt using a repeating keyword.
    Each letter of the key determines the Caesar shift for that position.
    key = 'A' means shift 0, 'B' means shift 1, etc.
    Non-alphabetic characters are unchanged and don't advance the key index.
    """
    pass

def vigenere_decrypt(text, key):
    """TODO: reverse vigenere_encrypt."""
    pass

def guess_key_length(ciphertext, max_len=12):
    """
    TODO: estimate the key length using the Index of Coincidence (IC).

    For each candidate length L:
      - Split ciphertext letters into L columns (every L-th character)
      - Calculate IC for each column: sum(f*(f-1)) / (n*(n-1))
        where f = frequency of each letter, n = column length
      - Average the IC across all columns

    English text has IC ≈ 0.065. Random text ≈ 0.038.
    The correct key length will produce columns with IC closest to 0.065.

    Return lengths sorted by how close their avg IC is to 0.065.
    """
    pass

def crack_vigenere(ciphertext, key_length):
    """
    TODO: given the key length, recover the key using frequency analysis.

    For each column i (every key_length-th character starting from i):
      - Find the most frequent letter in that column
      - Assume it corresponds to 'e' (most common in English)
      - Shift = (most_frequent - 'e') mod 26
      - That shift is the i-th key letter

    Return the guessed key as an uppercase string.
    """
    pass


if __name__ == "__main__":
    plaintext = ("The quick brown fox jumps over the lazy dog. "
                 "Cryptography is fascinating.")

    print("=== Caesar (shift=13) ===")
    enc = caesar_encrypt(plaintext, 13)
    dec = caesar_decrypt(enc, 13)
    print(f"Encrypted: {enc[:50]}...")
    print(f"Lossless:  {dec == plaintext}")

    print("\nBrute force top 3:")
    for shift, text in caesar_brute_force(enc)[:3]:
        print(f"  shift={shift:>2}  {text[:40]}...")

    print("\n=== Vigenère (key=PYTHON) ===")
    v_enc = vigenere_encrypt(plaintext, "PYTHON")
    v_dec = vigenere_decrypt(v_enc, "PYTHON")
    print(f"Encrypted: {v_enc[:50]}...")
    print(f"Lossless:  {v_dec == plaintext}")

    print("\nGuessing key length:")
    lengths = guess_key_length(v_enc)
    print(f"Top guesses: {lengths[:5]}")
    best = lengths[0]
    guessed_key = crack_vigenere(v_enc, best)
    print(f"Guessed key (length {best}): {guessed_key}")
