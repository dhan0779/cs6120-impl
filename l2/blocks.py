import json, sys, random

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

def create_block_name_map(blocks):
    block_map = {}
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
        else:
            name = 'block' + str(random.random())

        block_map[name] = block
    return block_map

def form_cfg(blocks):
    cfg = {} # label to list of labels
    block_map = create_block_name_map(blocks)
    for name, block in block_map.items():
        last = block[-1]
        if last['op'] in TERMINATOR:
            if last['op'] == 'jmp' or last['op'] == 'br':
                cfg[name] = [last['labels']]
            else:
                cfg[name] = []
        else:
            cfg[name] = []
    
    return cfg


with open(sys.argv[1]) as f:
    program = json.load(f)


for func in program['functions']:
    bb = form_blocks(func)
    cfg = form_cfg(bb)
    print(cfg)
    # break


