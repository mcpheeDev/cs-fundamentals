"""
simulator.py — A complete Little Man Computer (LMC) simulator.

Supports the full LMC instruction set. Includes a text assembler so you
can write programs in readable assembly and run them directly.

Run:  python3 simulator.py
"""


class LMCAssembler:
    """Converts human-readable LMC assembly text to machine code."""

    OPCODES = {
        "ADD": 100, "SUB": 200, "STA": 300, "LDA": 500,
        "BRA": 600, "BRZ": 700, "BRP": 800,
        "INP": 901, "OUT": 902, "HLT": 000,
    }

    def assemble(self, source: str) -> list[int]:
        """
        Two-pass assembly:
          Pass 1 — collect label definitions and their addresses
          Pass 2 — encode instructions, resolving labels
        """
        lines  = self._clean(source)
        labels = self._pass1(lines)
        return  self._pass2(lines, labels)

    def _clean(self, source):
        """Strip comments and blank lines; split into tokens."""
        cleaned = []
        for line in source.splitlines():
            line = line.split("//")[0].strip()   # remove comments
            if line:
                cleaned.append(line.split())
        return cleaned

    def _pass1(self, lines):
        """Build a label → address map."""
        labels  = {}
        address = 0
        for tokens in lines:
            if tokens[0].endswith(":"):
                labels[tokens[0][:-1]] = address
                tokens.pop(0)           # remove label from token list
            if tokens:                  # if there's still an instruction
                address += 1
        return labels

    def _pass2(self, lines, labels):
        """Encode each instruction as a 3-digit integer."""
        mem     = []
        for tokens in lines:
            # Remove label if still present
            if tokens[0].endswith(":"):
                tokens = tokens[1:]
            if not tokens:
                continue

            mnem = tokens[0].upper()
            if mnem == "DAT":
                mem.append(int(tokens[1]) if len(tokens) > 1 else 0)
            elif mnem in ("INP", "OUT", "HLT"):
                mem.append(self.OPCODES[mnem])
            elif mnem in self.OPCODES:
                operand_token = tokens[1] if len(tokens) > 1 else "0"
                operand = (labels[operand_token]
                           if operand_token in labels
                           else int(operand_token))
                mem.append(self.OPCODES[mnem] + operand)
            else:
                raise SyntaxError(f"Unknown mnemonic: {mnem!r}")

        return mem


class LMC:
    """
    Little Man Computer simulator.

    Registers:
      ACC — accumulator
      PC  — program counter
      NEG — negative flag (set when ACC < 0, used by BRP)

    Memory: 100 mailboxes (addresses 0–99)
    """

    def __init__(self):
        self.memory = [0] * 100
        self.acc    = 0
        self.pc     = 0
        self._neg   = False
        self._halted = False
        self._inputs  = []
        self._outputs = []
        self._steps   = []
        self._max_steps = 10_000

    def load(self, program: list[int]):
        """Load a machine-code program into memory from address 0."""
        self.memory[:len(program)] = program
        self.acc = self.pc = 0
        self._halted = False
        self._inputs  = []
        self._outputs = []
        self._steps   = []

    def set_inputs(self, *values):
        """Pre-load input values (avoids interactive prompts for testing)."""
        self._inputs = list(values)

    def run(self, verbose=False):
        """Execute until HLT or max_steps reached."""
        for _ in range(self._max_steps):
            if self._halted:
                break
            self._step(verbose)
        else:
            raise RuntimeError("Max steps exceeded — possible infinite loop")
        return self._outputs

    def _step(self, verbose=False):
        instruction = self.memory[self.pc]
        self.pc += 1
        opcode  = (instruction // 100) * 100
        operand = instruction % 100

        before_acc = self.acc

        if   instruction == 901:   # INP
            val = self._inputs.pop(0) if self._inputs else int(input("INP > "))
            self.acc = val

        elif instruction == 902:   # OUT
            self._outputs.append(self.acc)
            print(f"OUT: {self.acc}")

        elif instruction == 0:     # HLT
            self._halted = True

        elif opcode == 100:        # ADD
            self.acc += self.memory[operand]

        elif opcode == 200:        # SUB
            self.acc -= self.memory[operand]
            self._neg = self.acc < 0

        elif opcode == 300:        # STA
            self.memory[operand] = self.acc

        elif opcode == 500:        # LDA
            self.acc = self.memory[operand]

        elif opcode == 600:        # BRA
            self.pc = operand

        elif opcode == 700:        # BRZ
            if self.acc == 0:
                self.pc = operand

        elif opcode == 800:        # BRP
            if self.acc >= 0:
                self.pc = operand

        if verbose:
            mnem = self._decode(instruction)
            print(f"  PC={self.pc-1:>3}  {mnem:<10}  "
                  f"ACC: {before_acc:>5} → {self.acc:>5}  "
                  f"MEM[{operand}]={self.memory[operand]}")

        self._steps.append((instruction, self.acc))

    def _decode(self, instruction):
        NAMES = {900:"INP",900+2:"OUT",0:"HLT",
                 100:"ADD",200:"SUB",300:"STA",
                 500:"LDA",600:"BRA",700:"BRZ",800:"BRP"}
        if instruction in (901, 902, 0):
            return NAMES.get(instruction, "???")
        opcode  = (instruction // 100) * 100
        operand = instruction % 100
        name    = NAMES.get(opcode, "???")
        return f"{name} {operand}"


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE PROGRAMS
# ══════════════════════════════════════════════════════════════════════════════

PROGRAMS = {}

PROGRAMS["absolute_difference"] = """
// Outputs the positive difference between two inputs
// e.g. inputs 13, 5  → output 8
//      inputs 3,  8  → output 5

        INP
        STA  first
        INP
        STA  second
        LDA  first
        SUB  second
        BRP  positive
        LDA  second    // result was negative, swap subtraction
        SUB  first
positive: OUT
        HLT

first:  DAT 0
second: DAT 0
"""

PROGRAMS["count_to_n"] = """
// Counts from 1 up to the input value
// e.g. input 5 → outputs 1 2 3 4 5

        INP
        STA  limit
        LDA  one
        STA  counter

loop:   LDA  counter
        OUT
        SUB  limit
        BRZ  done
        LDA  counter
        ADD  one
        STA  counter
        BRA  loop

done:   HLT

counter: DAT 0
limit:   DAT 0
one:     DAT 1
"""

PROGRAMS["sum_to_n"] = """
// Computes the sum 1 + 2 + ... + n
// e.g. input 5 → output 15

        INP
        STA  n
        LDA  zero
        STA  total

loop:   LDA  n
        BRZ  done
        ADD  total
        STA  total
        LDA  n
        SUB  one
        STA  n
        BRA  loop

done:   LDA  total
        OUT
        HLT

n:      DAT 0
total:  DAT 0
one:    DAT 1
zero:   DAT 0
"""

PROGRAMS["loop_until_three"] = """
// Repeatedly asks for input until 3 is entered, then stops

loop:   INP
        SUB  three
        BRZ  done
        BRA  loop

done:   HLT

three:  DAT 3
"""


# ── Main ──────────────────────────────────────────────────────────────────────

def demo(name, inputs, verbose=False):
    asm    = LMCAssembler()
    source = PROGRAMS[name]
    mc     = asm.assemble(source)
    lmc    = LMC()
    lmc.load(mc)
    lmc.set_inputs(*inputs)
    print(f"\n{'─'*50}")
    print(f"  Program: {name}")
    print(f"  Inputs:  {inputs}")
    outputs = lmc.run(verbose=verbose)
    print(f"  Output:  {outputs}")
    print(f"  Steps:   {len(lmc._steps)}")


if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Little Man Computer Simulator          ║")
    print("╚══════════════════════════════════════════╝")

    demo("absolute_difference", [13, 5])
    demo("absolute_difference", [3,  8])
    demo("count_to_n",          [5])
    demo("sum_to_n",            [5])
    demo("sum_to_n",            [10])
    demo("loop_until_three",    [7, 2, 9, 3])

    # Show step-by-step trace for one program
    print(f"\n{'═'*55}")
    print("  VERBOSE TRACE — absolute_difference with inputs [13, 5]")
    print("═"*55)
    asm = LMCAssembler()
    lmc = LMC()
    lmc.load(asm.assemble(PROGRAMS["absolute_difference"]))
    lmc.set_inputs(13, 5)
    lmc.run(verbose=True)
