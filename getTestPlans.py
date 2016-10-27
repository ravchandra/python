import ast
import itertools
import os

path = r"D:\work\cloudstack\repo\internal-cloudstack\test\integration\smoke"
os.chdir(path)
for st in os.listdir(path):
    if os.path.isdir(st):
        continue

    print('Filename : '+st)
    print('-----------------------------------------\n')

    with open(st) as fd:
        file_contents = fd.read()
    with open(st) as fd:
        file_lines = fd.readlines()

    module = ast.parse(file_contents)
    nodes = (node.body for node in module.body if isinstance(node, ast.ClassDef))
    function_definitions = [fun for fun in list(itertools.chain.from_iterable(nodes))
                            if isinstance(fun, ast.FunctionDef) and 'test_' in fun.name]

    for i, f in enumerate(function_definitions):

        n = i+1
        if n<len(function_definitions):
            nextline = function_definitions[n].lineno
        else:
            nextline = len(file_lines)

        print('---- function ----')
        print(f.name)
        print('\n')
        print('---- description ----')
        print(ast.get_docstring(f))

        # Single line comments
        for li in file_lines[f.lineno:nextline]:
            if li.strip().startswith('#'):
                print(li.strip())

    print "\n"