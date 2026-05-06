# 11 – Encryption

## What you're building
Two classic symmetric ciphers and a frequency-analysis cracker for each.

## Part 1 — Caesar Cipher (`encryption.py`)
Shifts every letter by a fixed amount (wrapping A-Z).

- `caesar_encrypt(text, shift)` → encrypted string
- `caesar_decrypt(text, shift)` → original string
- `caesar_brute_force(ciphertext)` → list of (shift, decrypted) pairs,
  ranked by how English-like the result is (use letter frequency scoring)

## Part 2 — Vigenère Cipher (`encryption.py`)
A polyalphabetic cipher — each letter of the key determines the shift
for that position.

- `vigenere_encrypt(text, key)` → encrypted string
- `vigenere_decrypt(text, key)` → original string
- `guess_key_length(ciphertext)` → estimate key length using Index of Coincidence
- `crack_vigenere(ciphertext, key_length)` → guessed key using frequency analysis

## Part 3 — Comparison
Show why Vigenère is harder to crack than Caesar:
- Caesar: brute-forced in at most 25 attempts
- Vigenère: need to first guess key length, then crack each column

Include a brief written explanation in your README or as comments.

## Run tests
```bash
python3 tests.py
```
