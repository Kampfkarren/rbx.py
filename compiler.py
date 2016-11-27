import _ast
import ast
import sys

if sys.version_info[0] < 3:
    print("rbx.py won't (and never will) run on Python 2. Use Python 3.")
    sys.exit()

dev = True
predefined = {}
predefined["print"] = ["print", None]
predefined["range"] = ["RBXPY_range", "range"]

class Defined(dict):
    def __init__(self, compiler, inpt={}):
        super().__init__(inpt)
        self.compiler = compiler

    def __getitem__(self, name):
        if name in predefined:
            if predefined[name][1] != None:
                self.compiler.include(predefined[name][1])

            return predefined[name][0]
        else:
            return self.__dict__[name]

    def __setitem__(self, key, item):
        self.__dict__[key] = item

class Translater(ast.NodeVisitor):
    def __init__(self, compiler, basename, only_import=None):
        self.compiler = compiler
        self.basename = basename
        self.only_import = only_import

    def visit_FunctionDef(self, node):
        for dec in node.decorator_list:
            if dec.func.id == "translate":
                if self.only_import != None and not node.name in self.only_import:
                    continue

                if len(dec.args) > 1:
                    self.compiler.include(dec.args[1].s)

                if self.only_import == None:
                    self.compiler.defined["importedbuiltin_{}.{}".format(self.basename, node.name)] = dec.args[0].s
                else:
                    self.compiler.defined[node.name] = dec.args[0].s

class Compiler(ast.NodeVisitor):
    def __init__(self):
        self.code = ""
        self.libraries_used = []
        self.defined = Defined(self)
        self.inanif = 0

    def generic_visit(self, node):
        if dev:
            print(type(node).__name__)

        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node):
        for expr in node.body:
            self.visit(expr)

    def visit_Expr(self, node):
        self.visit(node.value)
        self.emit("\n")

    def visit_Name(self, node):
        self.emit(self.defined[node.id])

    def visit_Call(self, node):
        try:
            self.emit("{}(".format(self.defined[node.func.id]))
        except:
            self.emit("{}(".format(self.defined["importedbuiltin_{}.{}".format(node.func.value.id, node.func.attr)]))

        for arg in node.args:
            self.visit(arg)

            if node.args[-1] != arg:
                self.emit(", ")

        self.emit(")")

    def visit_Assign(self, node):
        for target in node.targets:
            if not target.id in self.defined:
                self.emit("local ")

            self.defined[target.id] = "var_{}".format(target.id)
            self.visit(target)
            self.emit(" = ")
            self.visit(node.value)
            self.emit("\n")

    def visit_Str(self, node):
        self.emit("\"{}\"".format(node.s))

    def visit_Num(self, node):
        self.emit(str(node.n))

    def visit_If(self, node):
        if self.inanif == 0:
            self.emit("\nif ")
        else:
            self.emit("elseif ")

        self.inanif += 1

        self.visit(node.test)
        self.emit(" then\n")

        for expr in node.body:
            self.visit(expr)

        for case in node.orelse:
            if type(case) is _ast.If:
                self.visit(case)
            else:
                self.emit("else\n")
                self.visit(case)

        self.inanif -= 1

        if self.inanif == 0:
            self.emit("end\n")

    def visit_Compare(self, node):
        self.visit(node.left)

        for i in range(len(node.ops)):
            self.visit(node.ops[i])
            self.visit(node.comparators[i])

    def visit_AugAssign(self, node):
        self.visit(node.target)
        self.emit(" = ")
        self.visit(node.target)
        self.visit(node.op)
        self.visit(node.value)
        self.emit("\n")

    def visit_Eq(self, node):
        self.emit(" == ")

    def visit_Add(self, node):
        self.emit(" + ")

    def visit_Sub(self, node):
        self.emit(" - ")

    def visit_Mult(self, node):
        self.emit(" * ")

    def visit_Div(self, node):
        self.emit(" / ")

    def visit_List(self, node):
        self.emit("{")

        for el in node.elts:
            self.visit(el)

            if node.elts[-1] != el:
                self.emit(", ")

        self.emit("}")

    def visit_For(self, node):
        self.defined[node.target.id] = "forloop_{}".format(node.target.id)

        self.emit("for _,forloop_{} in pairs(".format(node.target.id))
        self.visit(node.iter)
        self.emit(") do\n")

        for expr in node.body:
            self.visit(expr)

        self.emit("end\n")

    def visit_Dict(self, node):
        self.emit("{")

        for i in range(len(node.keys)):
            self.emit("[")
            self.visit(node.keys[i])
            self.emit("] = ")
            self.visit(node.values[i])

            if i != len(node.keys) - 1:
                self.emit(", ")

        self.emit("}")

    def visit_Subscript(self, node):
        self.visit(node.value)
        self.emit("[")
        self.visit(node.slice)
        self.emit("]")

    def visit_Index(self, node):
        self.visit(node.value)

    #someone make this not awful
    def visit_BinOp(self, node):
        if type(node.op) is _ast.Add:
            self.visit(node.left)
            self.emit(" + ")
            self.visit(node.right)
        elif type(node.op) is _ast.Sub:
            self.visit(node.left)
            self.emit(" - ")
            self.visit(node.right)
        elif type(node.op) is _ast.Mult:
            self.visit(node.left)
            self.emit(" * ")
            self.visit(node.right)
        elif type(node.op) is _ast.Div:
            self.visit(node.left)
            self.emit(" / ")
            self.visit(node.right)
        elif type(node.op) is _ast.Mod:
            self.visit(node.left)
            self.emit(" % ")
            self.visit(node.right)
        elif type(node.op) is _ast.BitXor:
            self.include("bitwise")
            self.emit("RBXPY_Bit.Xor(")
            self.visit(node.left)
            self.emit(", ")
            self.visit(node.right)
            self.emit(")")
        elif type(node.op) is _ast.BitAnd:
            self.include("bitwise")
            self.emit("RBXPY_Bit.And(")
            self.visit(node.left)
            self.emit(", ")
            self.visit(node.right)
            self.emit(")")
        elif type(node.op) is _ast.BitOr:
            self.include("bitwise")
            self.emit("RBXPY_Bit.Or(")
            self.visit(node.left)
            self.emit(", ")
            self.visit(node.right)
            self.emit(")")
        elif type(node.op) is _ast.LShift:
            self.include("bitwise")
            self.emit("RBXPY_Bit.LShift(")
            self.visit(node.left)
            self.emit(", ")
            self.visit(node.right)
            self.emit(")")
        elif type(node.op) is _ast.RShift:
            self.include("bitwise")
            self.emit("RBXPY_Bit.RShift(")
            self.visit(node.left)
            self.emit(", ")
            self.visit(node.right)
            self.emit(")")
        elif dev:
            print("Operator has not been accounted for: {}".format(type(node.op)))

    def visit_BoolOp(self, node):
        for val in node.values:
            self.visit(val)

            if node.values[-1] != val: #is there a better way to do this
                if type(node.op) is _ast.And:
                    self.emit(" and ")
                elif type(node.op) is _ast.Or:
                    self.emit(" or ")
                elif dev:
                    print("Bool operator not accounted for {}".format(node.op))

    def visit_Import(self, node):
        for name in node.names:
            try:
                builtin = open("./builtins/{}/__init__.py".format(name.name)).read()
            except:
                #TODO: custom imports
                pass
            else:
                translater = Translater(self, name.name)
                translater.visit(ast.parse(builtin))

    def visit_ImportFrom(self, node):
        try:
            builtin = open("./builtins/{}/__init__.py".format(node.module)).read()
        except:
            #TODO: custom imports
            pass
        else:
            translater = Translater(self, node.module, [name.name for name in node.names])
            translater.visit(ast.parse(builtin))

    def visit_NameConstant(self, node):
        if node.value == True:
            self.emit("true")
        elif node.value == False:
            self.emit("false")
        elif node.value == None:
            self.emit("nil")
        elif dev:
            print("Name constant does not have a value: {}".format(node.value))

    def visit_FunctionDef(self, node):
        self.defined[node.name] = "function_{}".format(node.name)

        self.emit("function function_{}(".format(node.name))

        total_args = []

        for arg in node.args.args:
            self.defined[arg.arg] = "funarg_{}".format(arg.arg)
            total_args.append("funarg_{}".format(arg.arg))

        self.emit("{})\n".format(', '.join(total_args)))

        for expr in node.body:
            self.visit(expr)

        self.emit("end\n\n")

        #unset vars
        for arg in node.args.args:
            del self.defined[arg.arg]

    def visit_Return(self, node):
        self.emit("return ")
        self.visit(node.value)
        self.emit("\n")

    #TODO: indentation
    def emit(self, val):
        self.code += val

    def include(self, library):
        if not library in self.libraries_used:
            self.libraries_used.append(library)
            self.code = open("./include/{}.lua".format(library)).read() + "\n" + self.code

compiler = Compiler()
compiler.visit(ast.parse(open(sys.argv[1]).read()))

compiler.code = "--This was Python code that was transpiled into Lua by rbx.py. Go to http://github.com/boynedmaster/rbx.py for more information.\n" + compiler.code

if dev:
    print(compiler.code)

with open(sys.argv[1] + ".lua", "w") as f:
    f.write(compiler.code + "\n")
