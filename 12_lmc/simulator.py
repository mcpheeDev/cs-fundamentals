class LMC:
    """
    Little Man Computer simulator.
    Memory: 100 mailboxes (addresses 0-99)
    Registers: ACC (accumulator), PC (program counter)
    """

    def __init__(self):
        self.memory  = [0] * 100
        self.acc     = 0
        self.pc      = 0
        self._neg    = False    # negative flag — set when SUB produces < 0
        self._halted = False
        self._inputs  = []      # pre-loaded inputs (used by set_inputs)
        self._outputs = []      # values printed by OUT

    def load(self, program):
        """Load a list of integer machine codes into memory from address 0."""
        # TODO: copy program into self.memory, reset acc, pc, halted flag
        pass

    def set_inputs(self, *values):
        """Pre-load input values so the simulator doesn't need user input."""
        self._inputs = list(values)

    def run(self, verbose=False):
        """
        TODO: execute instructions until HLT or 10,000 steps.
        If verbose=True, print each instruction as it executes.
        Return self._outputs.
        Raise RuntimeError if 10,000 steps exceeded (infinite loop guard).
        """
        pass

    def _step(self, verbose=False):
        """
        TODO: fetch the instruction at self.memory[self.pc], increment PC,
        then decode and execute it.

        Decoding:
          instruction = memory[pc]
          opcode  = (instruction // 100) * 100   e.g. 102 → 100 (ADD)
          operand = instruction % 100             e.g. 102 → 2

        Special cases (full 3-digit codes):
          901 = INP
          902 = OUT
          000 = HLT
        """
        pass


class LMCAssembler:
    """
    Converts human-readable LMC assembly to a list of integer machine codes.

    Example source:
        // add two numbers
        loop:  INP
               STA 99
               INP
               ADD 99
               OUT
               HLT
    """

    OPCODES = {
        "ADD": 100, "SUB": 200, "STA": 300, "LDA": 500,
        "BRA": 600, "BRZ": 700, "BRP": 800,
        "INP": 901, "OUT": 902, "HLT": 0,
    }

    def assemble(self, source):
        """
        TODO: two-pass assembler.

        Pass 1: strip comments, split into token lists, record label addresses.
          - A label is a token ending with ':' at the start of a line.
          - Each non-empty instruction line occupies one memory address.

        Pass 2: encode each instruction as an integer.
          - DAT n  →  store n directly
          - INP/OUT/HLT  →  use OPCODES value directly
          - ADD/SUB/etc  →  OPCODES[mnem] + operand
          - Operand may be a label name — look it up in your label table.

        Return a list of integers (machine code).
        """
        pass

    def _clean(self, source):
        """
        TODO: split source into lines, remove // comments,
        strip whitespace, remove blank lines.
        Return a list of token lists e.g. [["INP"], ["STA", "99"], ...]
        """
        pass


# ── Your LMC programs ─────────────────────────────────────────────────────────
# Write these yourself once your simulator works!

PROGRAMS = {
    "absolute_difference": """
    // TODO: input two numbers, output their positive difference
    // e.g. inputs 13, 5 → output 8
    //      inputs 3, 8  → output 5
    HLT
    """,

    "count_to_n": """
    // TODO: input N, then output 1, 2, 3, ... N
    // e.g. input 5 → outputs 1 2 3 4 5
    HLT
    """,

    "sum_to_n": """
    // TODO: input N, output the sum 1+2+...+N
    // e.g. input 5 → output 15
    HLT
    """,

    "loop_until_three": """
    // TODO: keep asking for input until the user enters 3, then stop
    HLT
    """,
}


# ── Helper: run a named program with pre-set inputs ───────────────────────────

def run_program(name, *inputs, verbose=False):
    asm     = LMCAssembler()
    machine = asm.assemble(PROGRAMS[name])
    lmc     = LMC()
    lmc.load(machine)
    lmc.set_inputs(*inputs)
    print(f"Program: {name}  inputs: {list(inputs)}")
    outputs = lmc.run(verbose=verbose)
    print(f"Outputs: {outputs}\n")
    return outputs


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_program("absolute_difference", 13, 5)
    run_program("absolute_difference", 3,  8)
    run_program("count_to_n",          5)
    run_program("sum_to_n",            5)
    run_program("sum_to_n",            10)
    run_program("loop_until_three",    7, 2, 9, 3)
