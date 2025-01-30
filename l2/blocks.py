import json, sys

TERMINATOR = 'br', 'jmp'

def form_blocks(func):
    blocks = []
    block = []
    for instr in func['instrs']:
        if 'op' in instr and (instr['op'] in TERMINATOR):
            block.append(instr)
            blocks.append(block)
            block = []
        elif 'label' in instr:
            if block:
                blocks.append(block)
            block = [instr]
        else:
            block.append(instr)

    if block:
        blocks.append(block)
    
    return blocks

with open(sys.argv[1]) as f:
    program = json.load(f)


for func in program['functions']:
    print(form_blocks(func))


