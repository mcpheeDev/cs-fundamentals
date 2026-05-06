import heapq
from collections import Counter


# ── RLE ───────────────────────────────────────────────────────────────────────

def rle_encode(text):
    """
    TODO: encode text using Run-Length Encoding.
    Consecutive repeated characters → count + character.
    e.g. 'AAABBC' → '3A2B1C'
    Single characters don't need a count prefix (or use 1 — your choice,
    as long as decode reverses it correctly).
    """
    pass

def rle_decode(encoded):
    """
    TODO: reverse rle_encode.
    '3A2B1C' → 'AAABBC'
    Hint: read digit(s) then the character, repeat until end of string.
    """
    pass


# ── Huffman ───────────────────────────────────────────────────────────────────

class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def __lt__(self, other):
        # needed for heapq comparisons
        return self.freq < other.freq


def build_huffman_tree(text):
    """
    TODO:
    1. Count frequency of each character (use Counter)
    2. Create a HuffmanNode for each character
    3. Push all nodes onto a min-heap
    4. While heap has more than 1 node:
         pop two lowest-frequency nodes
         create a merged parent node (char=None, freq=left.freq+right.freq)
         push merged node back onto heap
    5. Return the root node (last item in heap)
    """
    pass


def build_codes(node, prefix="", codes=None):
    """
    TODO: recursively traverse the Huffman tree.
    Assign prefix+'0' to left, prefix+'1' to right.
    When a leaf is reached, store codes[node.char] = prefix.
    Return the codes dict.
    Edge case: if the tree has only one unique character,
    assign '0' as its code.
    """
    pass


def huffman_encode(text):
    """
    TODO:
    1. Build the tree and codes
    2. Encode text as a binary string using the codes
    3. Return (binary_string, codes_dict)
    """
    pass


def huffman_decode(binary_string, codes):
    """
    TODO: decode a Huffman binary string using the code table.
    Hint: reverse the codes dict (code → char), then greedily
    match prefixes of the binary string.
    """
    pass


# ── Stats helpers ─────────────────────────────────────────────────────────────

def rle_stats(original, encoded):
    orig_bits = len(original) * 8
    enc_bits  = len(encoded)  * 8
    ratio     = enc_bits / orig_bits if orig_bits else 1
    print(f"  Original: {len(original)} chars ({orig_bits} bits)")
    print(f"  Encoded:  {len(encoded)} chars ({enc_bits} bits)")
    print(f"  Ratio:    {ratio:.3f}  ({'saving' if ratio < 1 else 'overhead'})")


def huffman_stats(original, encoded_bits):
    orig_bits = len(original) * 8
    ratio     = len(encoded_bits) / orig_bits if orig_bits else 1
    print(f"  Original: {len(original)} chars ({orig_bits} bits)")
    print(f"  Encoded:  {len(encoded_bits)} bits")
    print(f"  Ratio:    {ratio:.3f}  ({(1-ratio)*100:.1f}% saving)")


if __name__ == "__main__":
    rle_sample = "AAAAAAABBBBCCDDDDDDDDDEEEE"
    text = ("To be, or not to be, that is the question: "
            "Whether tis nobler in the mind to suffer.")

    print("=== RLE ===")
    enc = rle_encode(rle_sample)
    dec = rle_decode(enc)
    print(f"Original: {rle_sample}")
    print(f"Encoded:  {enc}")
    print(f"Decoded:  {dec}")
    print(f"Lossless: {dec == rle_sample}")
    rle_stats(rle_sample, enc)

    print("\n=== Huffman ===")
    binary, codes = huffman_encode(text)
    recovered = huffman_decode(binary, codes)
    print(f"Lossless: {recovered == text}")
    huffman_stats(text, binary)
