import json, sys

def print_constants(program):
    new_prog_list = []
    for func in program['functions']:
        for instr in func['instrs']:
            if 'op' in instr and instr['op'] == 'const':
                new_instr = {
                    "op": "print",
                    "args": [],
                    "funcs": [],
                    "labels": [],
                    "type": None,
                    "value": "const " + instr['dest'] + " = " + str(instr['value'])
                }
                print("added:" + instr['dest'], '=', instr['value'])
                new_prog_list.append(new_instr)
            new_prog_list.append(instr)
    return new_prog_list

def main():
    with open(sys.argv[1]) as f:
        program = json.load(f)

    program = print_constants(program)
    print(program)

        
if __name__ == '__main__':
    main()