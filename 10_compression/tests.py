from compression import (rle_encode, rle_decode, huffman_encode,
                          huffman_decode, build_huffman_tree, build_codes)

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


print("\n── RLE ───────────────────────────────────────────────")
# Round-trip tests
for s in ["AAABBC", "AAAAAAABBBBCCDDDDDDDDDEEEE", "A", "ABCDEF", ""]:
    decoded = rle_decode(rle_encode(s))
    test(f"round-trip: {s!r}", decoded, s)

# RLE compresses repetitive data
rep = "A" * 50
enc = rle_encode(rep)
test_true("RLE compresses 50 As",  len(enc) < len(rep))

# RLE may expand non-repetitive data
non_rep = "ABCDEFGHIJ"
enc2 = rle_encode(non_rep)
decoded2 = rle_decode(enc2)
test("RLE round-trips non-repetitive", decoded2, non_rep)


print("\n── Huffman ───────────────────────────────────────────")
texts = [
    "hello world",
    "aaabbbccc",
    "The quick brown fox jumps over the lazy dog",
    "aaaaaaaaaaaaaaaaaa",
]
for text in texts:
    binary, codes = huffman_encode(text)
    recovered = huffman_decode(binary, codes)
    test(f"round-trip: {text[:20]!r}", recovered, text)
    test_true(f"binary string is 0s and 1s",
              all(c in "01" for c in binary))

# Huffman should compress natural text
long_text = "abracadabra " * 20
binary, codes = huffman_encode(long_text)
orig_bits = len(long_text) * 8
test_true("Huffman compresses repetitive text",
          len(binary) < orig_bits)

# Frequent characters get shorter codes
from collections import Counter
text = "aaaaabbbcc"
_, codes = huffman_encode(text)
test_true("most frequent char has shortest code",
          len(codes["a"]) <= len(codes["b"]) <= len(codes["c"]))

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
