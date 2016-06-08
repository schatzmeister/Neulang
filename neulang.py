from sys import stderr

# error handling
def name_not_defined_error(name): 
    stderr.write("Name Error: '{}' is not defined.\n".format(name))
def empty_stack_error(name):
    stderr.write("Empty Stack error: '{}' has no elements.\n".format(name))
def name_already_defined_error(name):
    stderr.write("Name Error: '{}' is already defined.\n".format(name))
def argument_error(name):
    stderr.write(
        "Argument Error: '{}' is not "
        "provided the right arguments.\n".format(name)
        )
    
# builtin functions
def push_stack(stack, *val):
    try:
        stacks[stack].extend(val)
    except KeyError:
        name_not_defined_error(stack)
        
def pop_stack(stack):
    try:
        return stacks[stack].pop()
    except KeyError:
        name_not_defined_error(stack)
    except IndexError:
        empty_stack_error(stack)
        
def peek_stack(stack, number=1):
    if not stack:
        empty_stack_error(stack)
        return
    else:
        i = 1
        while stack and (i <= number or number in [-1, "all"]):
            return stacks[stack][-i]
            i += 1

def new_stack(name):
    if name not in stacks:
        stacks[name] = []
    else:
        name_already_defined_error(name)
        
def del_stack(name):
    if name in ["data", "prog"]:
        stderr.write("Cannot delete standard stack '{}'".format(name))
        return
    try:
        del stacks[name]
    except KeyError:
        name_not_defined_error(name)

def print_stacks():
    for key in stacks:
        print(key, end=' ')
    print()

# TODO: Get these to work.    
def add_stack(ins, args=2):
    add_stack(ins, ins, args)

def sub_stack(ins, args=2):
    sub_stack(ins, ins, args)

def mul_stack(ins, args=2):
    mul_stack(ins, ins, args)

def div_stack(ins, args=2):
    div_stack(ins, ins, args)

    
def add_stack(ins, outs, args=2):
    ins = stacks[ins]
    outs = stacks[outs]
    sum = 0
    if args == -1 or args == "all":
        for i in ins:
            sum += ins.pop()
    elif args < 0:
        argument_error("add")
        return
    else:
        for i in range(args):
            sum += ins.pop()
    push_stack(outs, sum)
    
def sub_stack(ins, outs, args=2):
    ins = stacks[ins]
    outs = stacks[outs]
    if not ins:
        empty_stack_error(ins)
        return
    diff = pop_stack(ins)    
    if args == -1 or args == "all":
        for i in ins:
            diff -= ins.pop()
    elif args <= 0:
        argument_error("sub")
        return
    else:
        for i in range(args - 1):
            diff -= ins.pop()
    push_stack(outs, diff)
    
def mul_stack(ins, outs, args=2):
    ins = stacks[ins]
    outs = stacks[outs]
    prod = 1
    if args == -1 or args == "all":
        for i in ins:
            pul *= ins.pop()
    elif args < 0:
        argument_error("mul")
        return
    else:
        for i in range(args):
            mul *= ins.pop()
    push_stack(outs, sum)
    
def div_stack(ins, outs, args=2):
    ins = stacks[ins]
    outs = stacks[outs]
    if not ins:
        empty_stack_error(ins)
        return
    quot = pop_stack(ins)    
    if args == -1 or args == "all":
        for i in ins:
            quot /= ins.pop()
    elif args <= 0:
        argument_error("div")
        return
    else:
        for i in range(args - 1):
            quot /= ins.pop()
    push_stack(outs, quot)
    
def flatten_first(stack):
    first = pop_stack(stack)
    # what is with special stacks like numbers?
    for elem in reversed(first):
        push_stack(stack, elem)
        
def push_range(stack, start, stop, step=1):
    for i in range(start, stop, step):
        push_stack(stack, i)
    
# stack operations
stackenv = {
    "push": push_stack,
    "pop": pop_stack,
    "peek": peek_stack,
    "new": new_stack,
    "del": del_stack,
    "stacks": print_stacks,
    "flatten": flatten_first,
    "range": push_range,
    }
# arithmetic operations
arithmenv = {
    "add": add_stack,
    "sub": sub_stack,
    "mul": mul_stack,
    "div": div_stack,
}

# user defined operations
userenv = {}

# stacks
data_stack = []
program_stack = []

stacks = {
    "data": data_stack,
    "prog": program_stack
    }

# REPL
def strip_line(line):
    '''Remove #-style comments and strip whitespace'''
    return line.split('#', 1)[0].strip()
    
def tokenize(line):
    if line == "":
        return []
    
    line.lstrip()
    if line.startswith('"'):
        token, _, rest = line[1:].partition('"')
    else:
        token, _, rest = line.partition(' ')
    
    return [token] + tokenize(rest)
    
def eval_line(line, environments):
    line = strip_line(line)
    name, *args = tokenize(line)
    try:
        return environments[name](*args)
    except KeyError:
        name_not_defined_error(name)
        return
    except TypeError:
        argument_error(name)
        return
            
if __name__ == '__main__':
    print("Welcome to Neulang interpreter version 0.1.")
    # standard environments
    envs = [stackenv, arithmenv, userenv]
    names = {}
    for env in envs:
        names.update(env)
    while True:
        line = input("~>")
        if line == "exit":
            exit()
        else:
            val = eval_line(line, names)
            if val is not None:
                print(val)
