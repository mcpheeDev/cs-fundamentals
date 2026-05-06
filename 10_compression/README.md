# 10 – Compression

## What you're building
Two lossless compression algorithms from scratch, with real
compression ratio statistics.

## Part 1 — Run-Length Encoding (`compression.py`)

RLE replaces runs of repeated characters with a count + character.
e.g. `AAABBC` → `3A2B1C`

Implement:
- `rle_encode(text)` — compress a string
- `rle_decode(encoded)` — decompress back to original
- Verify lossless round-trip
- Print: original size, encoded size, ratio, whether it helped

RLE works well on data with long repetitions (e.g. images).
It can actually make text *larger* — show this with an example.

## Part 2 — Huffman Coding (`compression.py`)

Huffman assigns shorter binary codes to more frequent characters.

Steps to implement:
1. Count character frequencies
2. Build a min-heap of leaf nodes
3. Repeatedly merge the two lowest-frequency nodes until one root remains
4. Traverse the tree to assign binary codes (left=0, right=1)
5. Encode the text using your code table
6. Decode by traversing the tree with the binary string

Implement:
- `huffman_encode(text)` → (binary_string, code_table)
- `huffman_decode(binary_string, code_table)` → original text
- Print a code table sorted by frequency
- Print compression stats

## Part 3 — Comparison
Apply both algorithms to the same text (e.g. a paragraph of Shakespeare).
Show which performs better and explain why.

## Run tests
```bash
python3 tests.py
```
