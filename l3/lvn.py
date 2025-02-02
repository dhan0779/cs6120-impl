#!/usr/bin/env python

import json, sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add cs6120-impl to sys.path
from l2.blocks import form_blocks

# cloud that points to table with var name
# this table needs a number, val -> tuple or const, var -> canonical name
# the tuple is the (op, number, number)
# if tuple is redundancy, add to cloud with var name which points to number in table 
# after adding to table, reconstruct the instruction with the new table according to value tuple

class Var2Num(dict):
    def __init__(self):
        super(Var2Num, self).__init__()
        self.counter = 0

    def generate_new_val(self):
        self.counter += 1
        return self.counter
    
def form_args_tuple(instr, var2num):
        return tuple([var2num[arg] for arg in instr.get('args', [])])


def check_overwritten(block):
    fresh = set()
    dest_fresh = []
    for instr in reversed(block):
        if 'dest' in instr:
            if instr['dest'] not in fresh:
                dest_fresh.append((True, instr))
            else: 
                dest_fresh.append((False, instr))
            fresh.add(instr['dest'])
    return dest_fresh[::-1]


def lvn(blocks):
    for block in blocks:
        lvn_table = {} # value tuple to canonical
        var2num = Var2Num() # var name to number table
        num2canonical = {} # number to canonical name table
        const_map = {}
        # lvn starts here for each basic block
        for fresh, instr in check_overwritten(block):
            arg_vars = form_args_tuple(instr, var2num) # this is the value tuple arguments
            if 'op' in instr and instr['op'] == 'const':
                arg_vars = instr['value']

            value = (instr['op'], ) + (arg_vars, )
            # print(value)
            if value in lvn_table:
                num, dest = lvn_table[value]
                var2num[instr['dest']] = num
                
                if num in const_map:  # Value is a constant.
                    instr.update({'op': 'const', 'value': const_map[num]})
                    del instr['args']
                else:
                    instr.update({'op': 'id', 'args': [dest]})

            elif 'dest' in instr and instr['op'] != 'call':
                num = var2num.generate_new_val()
                dest = instr['dest']

                if not fresh:
                    dest = dest + str(num)

                if instr['op'] == 'const':
                    const_map[num] = instr['value']
                    
                var2num[dest] = num
                num2canonical[num] = dest

                lvn_table[value] = (num, dest)

                new_args = []
                for a in instr.get('args', []):
                    new_args.append(num2canonical[var2num[a]])
                instr['args'] = new_args
    
    return blocks

def main():
    program = json.loads(sys.stdin.read())

    for func in program['functions']:
        blocks = form_blocks(func)
        func_with_lvn = lvn(blocks) 
        func = func_with_lvn
    
    json.dump(program, sys.stdout, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()