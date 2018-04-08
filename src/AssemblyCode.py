####### Classess for memory #########

class Register():
    def __init__(self, regName):
        self.regName = regName

    def __str__(self):
        return '%{reg}'.format(reg=self.regName)

# define available registers for assembly x86:
ax = Register('eax')
al = Register('al')
bx = Register('ebx')
cx = Register('ecx')
dx = Register('edx')
si = Register('esi')
di = Register('edi')
sp = Register('esp')
bp = Register('ebp')
stackElementSize = 4
alignSP = 16
spAddress = [0]

class Memory():
    def __init__(self, reg, offset):
        self.reg = reg
        self.offset = offset

    def __str__(self):
        return '{offset}({reg})'.format(offset=self.offset, reg=self.reg)

###### general class for data ############
class Data():
    pass

class ConstantInt(Data):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return '${val}'.format(val=self.val)

class ConstantStrLabel(Data):
    def __init__(self, strlabel):
        self.strlabel = strlabel

    def __str__(self):
        return '${label}'.format(label=self.strlabel)

####### general class for istructions ######
class Instruction():
    pass

# stack manipulation instructions
class Push(Instruction):
    def __init__(self, source):
        self.source = source
        global spAddress
        spAddress[0] -= stackElementSize

    def __str__(self):
        return 'pushl {src}'.format(src=self.source)

class Pop(Instruction):
    def __init__(self, dest=None):
        self.dest = dest
        global spAddress
        spAddress[0] += stackElementSize

    def __str__(self):
        if self.dest == None:
            return 'popl'
        return 'popl {dest}'.format(dest=self.dest)

# special instructions for manipulating stack pointer register
class AddSp(Instruction):
    def __init__(self, offset):
        self.offset = offset
        global spAddress
        spAddress[0] += offset

    def __str__(self):
        return 'addl ${val}, {sp}'.format(val=self.offset, sp=sp)

class SubSp(Instruction):
    def __init__(self, offset):
        global spAddress
        spAddress[0] -= offset
        self.offset = offset

    def __str__(self):
        return 'subl ${val}, {sp}'.format(val=self.offset, sp=sp)

# memory addressing instructions
class Move(Instruction):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __str__(self):
        return 'movl {src}, {dst}'.format(src=self.src, dst=self.dest)

# binary operations
class BinOp(Instruction):
    def __init__(self, left, right, dest=None):
        self.left = left
        self.right = right
        self.dest = dest

# arithmetic operations
class ArithmOp(BinOp):
    def __init__(self, left, right, dest=None):
        super().__init__(left, right, dest)


class Add(ArithmOp):
    def __init__(self, left, right, dest=None):
        super().__init__(left, right, dest)

    def __str__(self):
        return 'addl {src}, {dst}\n'.format(src=self.right, dst=self.left)

class Sub(ArithmOp):
    def __init__(self, left, right, dest=None):
        super().__init__(left, right, dest)

    def __str__(self):
        return 'subl {src}, {dst}'.format(src=self.right, dst=self.left)

class Mul(ArithmOp):
    def __init__(self, left, right, dest=None):
        # TODO assert left == eax, right == ecx
        super().__init__(left, right, dest)

    def __str__(self):
        return 'imull {src}, {dst}'.format(src=self.right, dst=self.left)


class Div(ArithmOp):
    def __init__(self, left, right, dest=None):
        # TODO assert left == eax, right = ecx
        # result in ax
        super().__init__(left, right, dest)

    def __str__(self):
        return 'cltd' + '\n' + 'idivl {right}'.format(right=self.right)

class Mod(ArithmOp):
    def __init__(self, left, right, dest=None):
        # TODO assert left == eax, right = ecx
        # result in dx
        super().__init__(left, right, dest)

    def __str__(self):
        return 'cltd' + '\n' + 'idivl {right}'.format(right=self.right)

# unary operations
class UnOp(Instruction):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

class NegateInt(UnOp):
    def __init__(self, src, dest):
        super().__init__(src, dest)

    def __str__(self):
        return 'negl {src}'.format(src=self.src)

class NegateBool(UnOp):
    def __init__(self, src, dest):
        super().__init__(src, dest)

    def __str__(self):
        return 'xorl $1, {src}'.format(src=self.src)

############# return instruction ################
class Return(Instruction):
    def __init__(self):
        pass
    def __str__(self):
        return 'ret'

########### instructions for jumps ##############
class Jump(Instruction):
    def __init__(self, codelabel, cond=None):
        self.codelabel = codelabel
        self.cond = cond

    def __str__(self):
        jump = ''
        if self.cond == None:
            jump = 'jmp'
        elif self.cond == '==':
            jump = 'je'
        elif self.cond == '!=':
            jump = 'jne'
        return '{jumpCode} {label}'.format(jumpCode=jump, label=self.codelabel.getAsText())


######### Function call #################
class Call(Instruction):
    def __init__(self, funLabel):
        self.funLabel = funLabel

    def __str__(self):
        return 'call {funLabel}'.format(funLabel=self.funLabel)


########## Compare #####################
class Compare(BinOp):
    def __init__(self, left, operation, right, dest):
        super().__init__(left, right, dest)
        self.operation = operation

    def __str__(self):
        code = 'cmpl {right}, {left}\n'.format(right=self.right, left=self.left)
        code += str(Set(self.operation, self.dest))
        return code

class Cmpl(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        code = 'cmpl {right}, {left}'.format(right=self.right, left=self.left)
        return code

############# Set #######################
class Set(Instruction):
    def __init__(self, operator, reg):
        opCode = 'set'
        if operator == '<':
            opCode += 'l'
        elif operator == '<=':
            opCode += 'le'
        elif operator == '>':
            opCode += 'g'
        elif operator == '>=':
            opCode += 'ge'
        elif operator == '==':
            opCode += 'e'
        elif operator == '!=':
            opCode += 'ne'
        self.opCode = opCode
        self.reg = reg

    def __str__(self):
        code = '{opCode} {reg}'.format(opCode=self.opCode, reg=self.reg)
        return code

############### special ###################
class Globl():
    def __init__(self, funName):
        self.funName = funName

    def __str__(self):
        return '  .globl {funName}'.format(funName=self.funName)

class Cbw(Instruction):
    def __init__(self):
        pass

    def __str__(self):
        return 'cbw'

class Cwde(Instruction):
    def __init__(self):
        pass

    def __str__(self):
        return 'cwde'

class Xor(Instruction):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return 'xorl {reg1}, {reg2}'.format(reg1=self.reg1, reg2=self.reg2)


####### General class for labels ########
class CodeLabel():
    # counter of fresh string labels
    nextFresh = 0

    def __init__(self, number=None):
        if number == None:
            # generate a fresh label if no value is passed
            self.labelNr = CodeLabel.nextFresh
            CodeLabel.nextFresh += 1
        else:
            self.labelNr = number

    def getAsText(self):
        return '.L{labelNr}'.format(labelNr=self.labelNr)

    def __str__(self):
        return self.getAsText() + ':'

class FunctionLabel():
    def __init__(self, funName):
        self.funName = funName

    def __str__(self):
        return '{name}:'.format(name=self.funName)

class StringLabel():
    def __init__(self, string, labelNr):
        self.string = string
        self.labelNr = labelNr

    def __str__(self):
        code = '.LC{labelNr}:\n'.format(labelNr=self.labelNr)
        code += "  .string "
        code += "\"\"" if self.string == "" else self.string
        return code

    def getAsText(self):
        return '.LC{labelNr}'.format(labelNr=self.labelNr)