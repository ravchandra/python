import ast
import csv
import itertools
import os
import pdb


def generate_test_plans(path):
    # print("--------------------- Path --------------------\n")
    # print(path)
    # print("\n")
    os.chdir(path)
    for st in os.listdir(path):
        try:
            if os.path.isdir(st):
                continue

            # # print("File name : " + path + "\\" + st)
            # print("File name : " + st)
            # print("-----------------------------------------\n")

            with open(st) as fd:
                file_contents = fd.read()
            with open(st) as fd:
                file_lines = fd.readlines()

            module = ast.parse(file_contents)
            nodes = (node.body for node in module.body
                     if isinstance(node, ast.ClassDef))
            function_definitions = [fun for fun in
                                    list(itertools.chain.from_iterable(nodes))
                                    if isinstance(fun, ast.FunctionDef)
                                    and "test_" in fun.name]

            for i, f in enumerate(function_definitions):

                n = i+1
                doc_string = ast.get_docstring(f)

                if n<len(function_definitions):
                    next_line = function_definitions[n].lineno
                else:
                    next_line = len(file_lines)

                # print("---- function ----")
                # print(f.name)
                # print("\n")

                # print("---- description ----")
                # print(doc_string)
                # print("\n")

                # Single line comments
                # print("---- comments ----")
                if doc_string is not None:
                    comment_start_line = f.lineno + doc_string.count("\n") + 1
                else:
                    comment_start_line = f.lineno + 1
                comment = ""
                for li in file_lines[comment_start_line:next_line]:
                    if li.strip().startswith("#"):
                        comment += li.strip() + "\n"
                        # print(li.strip())

                writer.writerow((f.name, doc_string, comment))
                # print("\n")
        except Exception as e:
            print(repr(e))
            print("Exception in file")
            print(st)


paths = [r"D:\work\cloudstack\repo\internal-cloudstack\test\integration\smoke",
         # r"D:\work\cloudstack\repo\internal-cloudstack\test\integration
         # \component\maint",
         # r"D:\work\cloudstack\repo\internal-cloudstack\test\integration
         # \smoke\misc",
         r"D:\work\cloudstack\repo\internal-cloudstack\test\integration\component"]

with open(r'D:\testplan.csv', 'wb') as cf:
    writer = csv.writer(cf)
    writer.writerow(('Test Name', 'Description', 'Comments'))
    for p in paths:
        generate_test_plans(p)