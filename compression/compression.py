"""
compression.py — Run-Length Encoding and Huffman coding implemented
from scratch, with real compression ratio statistics.

Run:  python3 compression.py
"""

import heapq
from collections import Counter
import os


# ══════════════════════════════════════════════════════════════════════════════
# RUN-LENGTH ENCODING (RLE)
# ══════════════════════════════════════════════════════════════════════════════

def rle_encode(data: str) -> str:
    """
    Compress a string using RLE.
    Consecutive repeated characters are replaced with count+char.
    e.g. "AAABBC" → "3A2B1C"
    """
    if not data:
        return ""
    result = []
    count  = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            result.append(f"{count}{data[i-1]}" if count > 1 else data[i-1])
            count = 1
    result.append(f"{count}{data[-1]}" if count > 1 else data[-1])
    return "".join(result)


def rle_decode(encoded: str) -> str:
    """Decompress an RLE string back to original."""
    result = []
    i = 0
    while i < len(encoded):
        if encoded[i].isdigit():
            count_str = ""
            while i < len(encoded) and encoded[i].isdigit():
                count_str += encoded[i]
                i += 1
            result.append(encoded[i] * int(count_str))
        else:
            result.append(encoded[i])
        i += 1
    return "".join(result)


def rle_stats(original: str, encoded: str):
    orig_bits = len(original) * 8
    enc_bits  = len(encoded) * 8
    ratio     = enc_bits / orig_bits if orig_bits else 1
    saving    = (1 - ratio) * 100
    print(f"  Original:  {len(original):>6} chars  ({orig_bits:>6} bits)")
    print(f"  Encoded:   {len(encoded):>6} chars  ({enc_bits:>6} bits)")
    print(f"  Ratio:     {ratio:.3f}   ({saving:+.1f}% {'saving' if saving > 0 else 'overhead'})")


# ══════════════════════════════════════════════════════════════════════════════
# HUFFMAN CODING
# ══════════════════════════════════════════════════════════════════════════════

class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def is_leaf(self):
        return self.left is None and self.right is None


def build_huffman_tree(text: str) -> HuffmanNode:
    """Build a Huffman tree from character frequencies."""
    freq = Counter(text)
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left  = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def build_codes(node: HuffmanNode, prefix="", codes=None) -> dict:
    """Recursively build the character → binary code mapping."""
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.is_leaf():
        codes[node.char] = prefix or "0"   # edge case: single unique char
        return codes
    build_codes(node.left,  prefix + "0", codes)
    build_codes(node.right, prefix + "1", codes)
    return codes


def huffman_encode(text: str) -> tuple[str, dict]:
    """Encode text to a binary string using Huffman coding."""
    if not text:
        return "", {}
    tree  = build_huffman_tree(text)
    codes = build_codes(tree)
    return "".join(codes[ch] for ch in text), codes


def huffman_decode(encoded: str, codes: dict) -> str:
    """Decode a Huffman-encoded binary string using the code table."""
    reverse = {v: k for k, v in codes.items()}
    result  = []
    buffer  = ""
    for bit in encoded:
        buffer += bit
        if buffer in reverse:
            result.append(reverse[buffer])
            buffer = ""
    return "".join(result)


def print_huffman_table(codes: dict, freq: Counter):
    """Display the Huffman code table sorted by frequency."""
    print(f"\n  {'Char':<8} {'Freq':>6}  {'Code':<16}  {'Bits saved'}")
    print("  " + "─" * 46)
    for char, code in sorted(codes.items(), key=lambda x: -freq[x[0]]):
        fixed   = 8                             # standard ASCII
        huffman = len(code)
        saving  = (fixed - huffman) * freq[char]
        label   = repr(char) if char in ("\n", "\t", " ") else char
        print(f"  {label!r:<8} {freq[char]:>6}  {code:<16}  {saving:>+5} bits")


def huffman_stats(original: str, encoded: str):
    orig_bits = len(original) * 8
    enc_bits  = len(encoded)   # already in bits
    ratio     = enc_bits / orig_bits if orig_bits else 1
    saving    = (1 - ratio) * 100
    print(f"  Original:  {len(original):>6} chars   ({orig_bits:>8} bits)")
    print(f"  Encoded:   {len(encoded):>6} bits    ({len(encoded)//8:>8} bytes equiv)")
    print(f"  Ratio:     {ratio:.3f}    ({saving:.1f}% saving)")


# ── Main ──────────────────────────────────────────────────────────────────────

SAMPLE_TEXT = (
    "To be, or not to be, that is the question: "
    "Whether 'tis nobler in the mind to suffer "
    "the slings and arrows of outrageous fortune, "
    "or to take arms against a sea of troubles."
)

RLE_SAMPLE = "AAAAAAABBBBCCDDDDDDDDDEEEE"

if __name__ == "__main__":

    # ── RLE ───────────────────────────────────────────────────────────────────
    print("═" * 55)
    print("  RUN-LENGTH ENCODING (RLE)")
    print("═" * 55)

    encoded = rle_encode(RLE_SAMPLE)
    decoded = rle_decode(encoded)

    print(f"  Original: {RLE_SAMPLE}")
    print(f"  Encoded:  {encoded}")
    print(f"  Decoded:  {decoded}")
    print(f"  Lossless: {'✓' if decoded == RLE_SAMPLE else '✗'}")
    print()
    rle_stats(RLE_SAMPLE, encoded)

    print()
    print("  RLE on text (less repetition = less effective):")
    enc2 = rle_encode(SAMPLE_TEXT)
    rle_stats(SAMPLE_TEXT, enc2)

    # ── Huffman ───────────────────────────────────────────────────────────────
    print("\n" + "═" * 55)
    print("  HUFFMAN CODING")
    print("═" * 55)

    encoded_huff, codes = huffman_encode(SAMPLE_TEXT)
    decoded_huff = huffman_decode(encoded_huff, codes)

    freq = Counter(SAMPLE_TEXT)
    print_huffman_table(codes, freq)

    print()
    huffman_stats(SAMPLE_TEXT, encoded_huff)

    print(f"\n  Lossless round-trip: {'✓' if decoded_huff == SAMPLE_TEXT else '✗'}")

    # ── Comparison ────────────────────────────────────────────────────────────
    print("\n" + "═" * 55)
    print("  RLE vs HUFFMAN — which is better for natural text?")
    print("═" * 55)
    rle_enc    = rle_encode(SAMPLE_TEXT)
    huff_enc, _ = huffman_encode(SAMPLE_TEXT)
    orig_bits  = len(SAMPLE_TEXT) * 8
    rle_bits   = len(rle_enc) * 8
    huff_bits  = len(huff_enc)
    print(f"  Original:  {orig_bits} bits")
    print(f"  RLE:       {rle_bits} bits  ({(1-rle_bits/orig_bits)*100:+.1f}%)")
    print(f"  Huffman:   {huff_bits} bits  ({(1-huff_bits/orig_bits)*100:+.1f}%)")
    print()
    print("  Verdict: RLE is better for data with long repeated runs (e.g. images).")
    print("           Huffman is better for natural language text.")
