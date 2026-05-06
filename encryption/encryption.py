"""
encryption.py — Caesar cipher, Vigenère cipher, and a brute-force
frequency-analysis cracker for each.

Run:  python3 encryption.py
"""

import string
from collections import Counter


# ══════════════════════════════════════════════════════════════════════════════
# CAESAR CIPHER  (symmetric — same key to encrypt and decrypt)
# ══════════════════════════════════════════════════════════════════════════════

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Shift every letter by `shift` positions (wraps A-Z, a-z)."""
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt by shifting in the opposite direction."""
    return caesar_encrypt(ciphertext, -shift)


def caesar_brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """
    Try all 25 possible shifts. Score each by English letter frequency.
    Return shifts ranked best to worst.
    """
    ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"

    def score(text):
        letters = text.lower()
        freq = Counter(c for c in letters if c.isalpha())
        total = sum(freq.values()) or 1
        return sum(
            freq[ch] / total * (26 - ENGLISH_FREQ.index(ch))
            for ch in freq if ch in ENGLISH_FREQ
        )

    candidates = []
    for shift in range(1, 26):
        attempt = caesar_decrypt(ciphertext, shift)
        candidates.append((shift, attempt, score(attempt)))

    return [(s, t) for s, t, _ in sorted(candidates, key=lambda x: -x[2])]


# ══════════════════════════════════════════════════════════════════════════════
# VIGENÈRE CIPHER  (polyalphabetic — harder to crack)
# ══════════════════════════════════════════════════════════════════════════════

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt using a repeating keyword.
    Each letter of the keyword determines the Caesar shift for that position.
    """
    key     = key.upper()
    result  = []
    key_idx = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord("A")
            base  = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt by using the negative of each key letter's shift."""
    key     = key.upper()
    result  = []
    key_idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord("A")
            base  = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            key_idx += 1
        else:
            result.append(ch)
    return "".join(result)


def guess_key_length(ciphertext: str, max_len=12) -> list[tuple[int, float]]:
    """
    Kasiski / Index of Coincidence method to estimate key length.
    Returns key lengths ranked by likelihood.
    """
    letters = [c.lower() for c in ciphertext if c.isalpha()]

    def index_of_coincidence(text):
        n = len(text)
        if n <= 1: return 0
        freq = Counter(text)
        return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))

    scores = []
    for length in range(1, max_len + 1):
        columns = ["".join(letters[i::length]) for i in range(length)]
        avg_ic  = sum(index_of_coincidence(col) for col in columns) / length
        scores.append((length, avg_ic))

    # English IC ≈ 0.065; random IC ≈ 0.038
    return sorted(scores, key=lambda x: abs(x[1] - 0.065))


def crack_vigenere(ciphertext: str, key_length: int) -> str:
    """
    Crack Vigenère given a known key length using frequency analysis per column.
    """
    letters  = [c.lower() for c in ciphertext if c.isalpha()]
    MOST_COMMON = "e"

    key = []
    for i in range(key_length):
        column = letters[i::key_length]
        freq   = Counter(column)
        most_common_char = freq.most_common(1)[0][0]
        # Assume most common ciphertext letter corresponds to 'e'
        shift = (ord(most_common_char) - ord(MOST_COMMON)) % 26
        key.append(chr(shift + ord("A")))

    return "".join(key)


# ══════════════════════════════════════════════════════════════════════════════
# DEMO
# ══════════════════════════════════════════════════════════════════════════════

PLAINTEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "Cryptography is the practice of securing communication."
)

if __name__ == "__main__":

    # ── Caesar ────────────────────────────────────────────────────────────────
    print("═" * 60)
    print("  CAESAR CIPHER")
    print("═" * 60)

    shift = 13   # ROT13
    enc = caesar_encrypt(PLAINTEXT, shift)
    dec = caesar_decrypt(enc, shift)

    print(f"  Plaintext:  {PLAINTEXT[:60]}...")
    print(f"  Shift:      {shift}")
    print(f"  Encrypted:  {enc[:60]}...")
    print(f"  Decrypted:  {dec[:60]}...")
    print(f"  Lossless:   {'✓' if dec == PLAINTEXT else '✗'}")

    print("\n  Brute-force crack (top 3 candidates):")
    candidates = caesar_brute_force(enc)
    for rank, (s, text) in enumerate(candidates[:3], 1):
        print(f"  #{rank}  shift={s:>2}  {text[:55]}...")

    # ── Vigenère ──────────────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  VIGENÈRE CIPHER")
    print("═" * 60)

    key   = "PYTHON"
    v_enc = vigenere_encrypt(PLAINTEXT, key)
    v_dec = vigenere_decrypt(v_enc, key)

    print(f"  Plaintext:  {PLAINTEXT[:60]}...")
    print(f"  Key:        {key}")
    print(f"  Encrypted:  {v_enc[:60]}...")
    print(f"  Decrypted:  {v_dec[:60]}...")
    print(f"  Lossless:   {'✓' if v_dec == PLAINTEXT else '✗'}")

    # ── Crack Vigenère ────────────────────────────────────────────────────────
    print("\n  Cracking Vigenère (key length analysis):")
    length_guesses = guess_key_length(v_enc)
    print(f"  Top guessed key lengths: "
          f"{[l for l, _ in length_guesses[:5]]}")
    best_len = length_guesses[0][0]
    guessed_key = crack_vigenere(v_enc, best_len)
    print(f"  Guessed key (length {best_len}): {guessed_key}")
    attempt = vigenere_decrypt(v_enc, guessed_key)
    print(f"  Attempt:    {attempt[:60]}...")

    # ── Comparison ────────────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("  SYMMETRIC CIPHER COMPARISON")
    print("═" * 60)
    print("  Caesar:    simple, single shift, broken by brute force in ≤25 tries")
    print("  Vigenère:  polyalphabetic, key determines security, harder to crack")
    print("  Both:      symmetric — same key encrypts and decrypts")
    print("  Real-world symmetric: AES (Advanced Encryption Standard)")
    print("  Real-world asymmetric: RSA (public/private key pair)")
