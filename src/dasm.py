import sys
import os

def dasm():
    source = sys.argv[1]
 
    if (len(sys.argv) > 2):
        dest = sys.argv[2]
    else:
        # deduce dest
        path = source.split('/')
        source_name = os.path.splitext(path[len(path) - 1])[0]
        dest = f'{source_name}.dasm'

    in_data_block = False
    in_mis_block = False
    with open(dest, 'w') as o:
        o.write(f'~~~ GENERATED BY DASM ~~~\n~~~ DISASSEMBLY OF {source} ~~~\n')

        with open(source) as i:
            lines = i.readlines()

            for line_num, line in enumerate(lines):
                # remove newline
                line = line.replace('\n', '').strip()

                # print data
                if in_data_block:
                    o.write(f'{line}\n')
                    continue

                # empty
                if not line:
                    continue

                if line.startswith('//'):
                    if '@BEGIN' in line or '@END' in line:
                        if 'DATA' in line:
                            in_data_block = not in_data_block
                        elif 'MISALIGNED' in line:
                            in_mis_block = not in_mis_block

                        if '@BEGIN' in line:
                            o.write(f'\n{line}\n')
                        else:
                            o.write(f'{line}\n\n')
                    continue

                # reform misalignment
                if in_mis_block:
                    next_line = lines[line_num + 1].replace('\n', '')
                    if next_line.startswith('//'):
                        continue
                    else:
                        line = next_line[2:5] + line[0:2]

                # mem directive
                if line.startswith('@'):
                    o.write(f'{line}\n')
                    continue

                # extract comment
                comment = ''
                if '//' in line:
                    comment_index = line.index('//')
                    comment = line[comment_index:]
                    line = line[:comment_index].strip()

                half_bytes = [int(line[hb], 16) for hb in range(0, 4)]

                # decode
                opcode = half_bytes[0]
                if (opcode == 0):
                    ra = half_bytes[1]
                    rb = half_bytes[2]
                    rt = half_bytes[3]
                    o.write(f'<{line}>: sub r{rt}, r{ra}, r{rb}\n')
                elif (opcode == 8):
                    imm = (half_bytes[1] << 4) + half_bytes[2]
                    if (imm > 255):
                        print(f'IMMEDIATE VALUE TOO LARGE ({line}) AT LINE {line_num}')
                        exit(1)
                    rt = half_bytes[3]
                    o.write(f'<{line}>: movl r{rt}, #{imm}\n')
                elif (opcode == 9):
                    imm = (half_bytes[1] << 4) + half_bytes[2]
                    if (imm > 255):
                        print(f'IMMEDIATE VALUE TOO LARGE ({line}) AT LINE {line_num}')
                        exit(1)
                    rt = half_bytes[3]
                    o.write(f'<{line}>: movh r{rt}, #{imm}\n')
                elif (opcode == 14):
                    ra = half_bytes[1]
                    jmp_diff = half_bytes[2]
                    rt = half_bytes[3]
                    if (jmp_diff == 0):
                        o.write(f'<{line}>: jz r{rt}, r{ra}\n')
                    elif (jmp_diff == 1):
                        o.write(f'<{line}>: jnz r{rt}, r{ra}\n')
                    elif (jmp_diff == 2):
                        o.write(f'<{line}>: js r{rt}, r{ra}\n')
                    elif (jmp_diff == 3):
                        o.write(f'<{line}>: jns r{rt}, r{ra}\n')
                    else:
                        print(f'INCORRECT USAGE OF JMP ({line}) AT LINE {line_num}')
                        exit(1)
                elif (opcode == 15):
                    ra = half_bytes[1]
                    mem_diff = half_bytes[2]
                    rt = half_bytes[3]
                    if (mem_diff == 0):
                        o.write(f'<{line}>: ld r{rt}, r{ra}\n')
                    elif (mem_diff == 1):
                        o.write(f'<{line}>: st r{rt}, r{ra}\n')
                    elif (ra == 15 and mem_diff == 15 and rt == 15):
                        o.write('<ffff>: end\n')
                    else:
                        print(f'INCORRECT USAGE OF MEM STR/LD ({line}) AT LINE {line_num}')
                        exit(1)
                else:
                    print(f'UNKNOWN INSTRUCTION ({line}) AT LINE {line_num}')
                    exit(1)


if __name__ == '__main__':
    dasm()
