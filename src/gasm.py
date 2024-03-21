import sys
import os

def gasm():
    source = sys.argv[1]

    if (len(sys.argv) > 2):
        dest = sys.argv[2]
    else:
        # deduce dest
        path = source.split('/')
        source_name = os.path.splitext(path[len(path) - 1])[0]
        dest = f'{source_name}.hex'

    with open(dest, 'w') as o:
        o.write('@0\n')

        with open(source) as i:
            for line_num, line in enumerate(i):
                # remove symbols
                line = line.replace(',', '').replace('r', '').replace('#', '').replace('\n', '').lower()
                comps = line.split(' ')

                instr = comps[0]

                # end
                if instr == 'end':
                    o.write('ffff\n')
                    exit(0)

                if len(comps) > 1:
                    rt = hex(int(comps[1])).split('x')[-1]
                    ra = hex(int(comps[2])).split('x')[-1]
                if len(comps) > 3:
                    rb = hex(int(comps[3])).split('x')[-1]

                imm = hex(int(comps[2])).split('x')[-1]
                imm = f'0{imm}' if len(imm) == 1 else imm

                # convert to hex
                if instr == 'sub':
                    o.write(f'0{ra}{rb}{rt}\n')
                elif instr == 'movl':
                    o.write(f'8{imm}{rt}\n')
                elif instr == 'movh':
                    o.write(f'9{imm}{rt}\n')
                elif instr == 'jz':
                    o.write(f'e{ra}0{rt}\n')
                elif instr == 'jnz':
                    o.write(f'e{ra}1{rt}\n')
                elif instr == 'js':
                    o.write(f'e{ra}2{rt}\n')
                elif instr == 'jns':
                    o.write(f'e{ra}3{rt}\n')
                elif instr == 'ld':
                    o.write(f'f{ra}0{rt}\n')
                elif instr == 'st':
                    o.write(f'f{ra}1{rt}\n')
                else:
                    print(f'INVALID ASM INSTRUCTION ({line}) AT LINE {line_num}')
                    exit(1)

if __name__ == '__main__':
    gasm()
