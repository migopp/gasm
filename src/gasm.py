import sys
import os

def resolve_labels(lines):
    labels = {}
    resolved_lines = []

    for line in lines:
        line = line.strip()
        if ':' in line:
            label, _ = line.split(':')
            if label.lower() in ['end', 'sub', 'movl', 'movh', 'jz', 'jnz', 'js', 'jns', 'ld', 'st']:
                print(f'INVALID LABEL ({label}) AT LINE {len(resolved_lines)}')
                exit(1)
            labels[label] = len(resolved_lines)*2-2
        else:
            resolved_lines.append(line)

    return resolved_lines, labels

def gasm():
    source = sys.argv[1]
    if (len(sys.argv) > 2):
        dest = sys.argv[2]
    else:
        # deduce dest path
        path = source.split('/')
        source_name = os.path.splitext(path[len(path) - 1])[0]
        dest = f'{source_name}.hex'

    with open(dest, 'w') as o:
        with open(source) as i:
            lines = i.readlines()
            lines, labels = resolve_labels(lines)

            for line_num, line in enumerate(lines):
                # remove newline
                line = line.replace('\n', '').strip()

                # empty line
                if not line:
                    o.write('\n')
                    continue

                # comment
                if line.startswith('//'):
                    o.write(f'{line}\n')
                    continue

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

                # insert char
                if "'" in line:
                    char_index = line.index("'")
                    char = line[char_index + 1]
                    line = line[:char_index] + str(ord(char)) + line[char_index + 2:]
                # remove symbols
                line = line.replace(',', '').replace('r', '').replace('#', '').lower()

                # filter out whitespace
                u_comps = line.split(' ')
                comps = list(filter(lambda c: c != '' and c != ' ' and c != '\t', u_comps))
                instr = comps[0]
                if len(comps) > 1:
                    rt = hex(int(comps[1])).split('x')[-1]
                    if instr in ['movl', 'movh'] and len(comps) > 2 and comps[2] in labels:
                        imm = hex(labels[comps[2]]).split('x')[-1]
                        print(labels[comps[2]])
                        imm = f'0{imm}' if len(imm) == 1 else imm
                    else:
                        ra = hex(int(comps[2])).split('x')[-1]
                        imm = hex(int(comps[2])).split('x')[-1]
                        imm = f'0{imm}' if len(imm) == 1 else imm
                if len(comps) > 3:
                    rb = hex(int(comps[3])).split('x')[-1]
                
                # convert to hex
                if instr == 'end':
                    o.write('ffff\n')
                elif instr == 'sub':
                    o.write(f'0{ra}{rb}{rt}\t{comment}\n')
                elif instr == 'movl':
                    o.write(f'8{imm}{rt}\t{comment}\n')
                elif instr == 'movh':
                    o.write(f'9{imm}{rt}\t{comment}\n')
                elif instr == 'jz':
                    o.write(f'e{ra}0{rt}\t{comment}\n')
                elif instr == 'jnz':
                    o.write(f'e{ra}1{rt}\t{comment}\n')
                elif instr == 'js':
                    o.write(f'e{ra}2{rt}\t{comment}\n')
                elif instr == 'jns':
                    o.write(f'e{ra}3{rt}\t{comment}\n')
                elif instr == 'ld':
                    o.write(f'f{ra}0{rt}\t{comment}\n')
                elif instr == 'st':
                    o.write(f'f{ra}1{rt}\t{comment}\n')
                else:
                    o.write(f'ffff\n')
                    print(f'INVALID ASM INSTRUCTION ({line}) AT LINE {line_num}, will be replaced with 0xffff')
                    # exit(1)

if __name__ == '__main__':
    gasm()