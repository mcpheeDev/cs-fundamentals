# 12 – LMC Simulator

## What you're building
A complete Little Man Computer simulator with a text assembler,
so you can write LMC programs as readable text and run them.

## Part 1 — The Simulator (`simulator.py`)

Build a class `LMC` with:
- 100 mailboxes (memory), initialised to 0
- An accumulator (ACC), program counter (PC)
- A negative flag (set when SUB produces a negative result — used by BRP)

Implement the full instruction set:

| Mnemonic | Machine code | Effect |
|----------|-------------|--------|
| ADD xx | 1xx | ACC = ACC + memory[xx] |
| SUB xx | 2xx | ACC = ACC − memory[xx] |
| STA xx | 3xx | memory[xx] = ACC |
| LDA xx | 5xx | ACC = memory[xx] |
| BRA xx | 6xx | PC = xx (always jump) |
| BRZ xx | 7xx | PC = xx if ACC == 0 |
| BRP xx | 8xx | PC = xx if ACC >= 0 |
| INP | 901 | ACC = next input |
| OUT | 902 | print ACC |
| HLT | 000 | stop |

## Part 2 — The Assembler (`simulator.py`)

Write an `LMCAssembler` class that converts human-readable text to machine code.

Support:
- Mnemonics with/without operands
- Labels (e.g. `loop: INP`) — two-pass assembly
- `DAT n` — store a data value in memory
- `// comments`

## Part 3 — Write these programs yourself

Once your simulator works, write LMC assembly for each:

1. **absolute_difference** — input two numbers, output their positive difference
2. **count_to_n** — input N, output 1 2 3 ... N
3. **sum_to_n** — input N, output 1+2+...+N
4. **loop_until_three** — keep asking for input until the user enters 3

Store each as a string constant in `simulator.py`.

## Run tests
```bash
python3 tests.py
```
