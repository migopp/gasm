# gasm
The Gheith ISA assembler.

For students in Dr. Gheith's CS 429H course completing pipelining.

## Quick Start
`pip install gasm` 👍

## Usage

### Assembling:

```
gasm <path to assembly file> <OPTIONAL: path to desired output file>
```

There are relatively few restrictions on the assembly file. The file extension, for example, is entirely unimportant. Designations like `r` for registers and `#` for literals are also not required (and do not impact the assembly process).

However, you may not have labels (this should not matter). You may only have instructions. Take the following as an example:

```
movl r0, #104
movl r0, #101
movl r0, #108
movl r0, #108
movl r0, #111
movl r0, #10
```

You may choose to end your assembly with an `end` directive. Doing so, the assembler will provide the hex instruction `ffff` in its place.

### Disassembling:

```
dasm <path to .hex file> <OPTIONAL: path to desired output file>
```

The file you want to disassemble should be valid `.hex`. It may, however, end with an `ffff`, though the instruction is not officially recognized.
