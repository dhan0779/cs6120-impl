import json, sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add cs6120-impl to sys.path
from l2.blocks import form_blocks



def dce(blocks):
    func_change = True
    while func_change:
        used = set()
        for block in blocks:
            for instr in block:
                used.update(instr.get('args', []))

        new_block = []
        for block in blocks:
            for instr in block:
                if 'dest' not in instr or instr['dest'] in used:
                    new_block.append(instr)
            
            if len(new_block) == len(block):
                func_change = False
            block = new_block
    
    return blocks

def main():
    with open(sys.argv[1]) as f:
        program = json.load(f)

    for func in program['functions']:
        print(func)
        blocks = form_blocks(func)
        func_with_dce = dce(blocks)
        print(func_with_dce)

if __name__ == '__main__':
    main()