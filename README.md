# gasm
The Gheith ISA assembler.

For students in Dr. Gheith's CS 429H course completing pipelining.

## Quick Start

```
python3 -m pip install gasm
```
And, you're good to go. 👍

## Usage

### Assembling:

```
gasm <path to assembly file> <OPTIONAL: path to desired output file>
```

There are relatively few restrictions on the assembly file. The file extension, for example, is entirely unimportant. Designations like `r` for registers and `#` for literals are also not required (and do not impact the assembly process).

However, you may not have labels (this should not matter). You may only have instructions, comments, and memory directives. Take the following as an example:

```
// place at memory location 0
@0
movl r0, #104 // print 'h'
movl r0, #101 // print 'e'
movl r0, #108 // print 'l'
movl r0, #108 // print 'l'
movl r0, #111 // print 'o'
movl r0, #10  // print '\n'
end
```

You may choose to end your assembly with an `end` directive. Doing so, the assembler will provide the hex instruction `ffff` in its place.

### Disassembling:

```
dasm <path to .hex file> <OPTIONAL: path to desired output file>
```

The file you want to disassemble should be valid `.hex`. It may, however, end with an `ffff`, though the instruction is not officially recognized.

## Comments:

You may find it important to comment your `.hex` output for test case quality. gasm supports this functionality, and should maintain your comments when assembling. For example, the above code assembles to:

```
// place at memory location 0
@0
8680	// print 'h'
8650	// print 'e'
86c0	// print 'l'
86c0	// print 'l'
86f0	// print 'o'
80a0	// print '\n'
ffff
```

dasm also supports having comments in the `.hex`, though I chose not to display them because of clutter.
