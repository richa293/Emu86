"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from assembler.errors import check_num_args
from assembler.tokens import Instruction, Register, IntegerTok
from .argument_check import *



class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Unknown control flow exception."

def get_one_op(instr, ops):
    check_num_args(instr, ops, 1)
    return ops[0]

def get_two_ops(instr, ops):
    check_num_args(instr, ops, 2)
    return (ops[0], ops[1])

def get_three_ops(instr, ops):
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    return (ops[0], ops[1], ops[2])

def get_three_ops_imm(instr, ops):
    check_num_args(instr, ops, 3)
    check_immediate_three(instr, ops)
    return (ops[0], ops[1], ops[2])

class Jump(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


class Slt(Instruction):
    """
        <instr>
             slt
        </instr>
        <syntax>
            SLT reg, reg, reg
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to 
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm):      
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops)
        res = op2.get_val() - op3.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            vm.flags['SF'] = 1
        else:
            vm.flags['SF'] = 0
        op1.set_val(vm.flags['SF'])

class Slti(Instruction):
    """
        <instr>
             slti
        </instr>
        <syntax>
            SLTI reg, con, reg
            SLTI reg, reg, con
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to 
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops)
        res = op2.get_val() - op3.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            vm.flags['SF'] = 1
        else:
            vm.flags['SF'] = 0
        op1.set_val(vm.flags['SF'])
    

class Jmp(Instruction):
    """
        <instr>
            jmp
        </instr>
        <syntax>
            JMP lbl
        </syntax>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Je(Instruction):
    """
        <instr>
             je
        </instr>
        <syntax>
            JE lbl
        </syntax>
        <descr>
            Jumps if ZF is one. <br>
            Equivalent name: JZ
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['ZF']) == 1:
            raise Jump(target.name)

class Jne(Instruction):
    """
        <instr>
             jne
        </instr>
        <syntax>
            JNE lbl
        </syntax>
        <descr>
            Jumps if ZF is zero. <br>
            Equivalent name: JNZ
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['ZF']) == 0:
            raise Jump(target.name)

class Jg(Instruction):
    """
        <instr>
             jg
        </instr>
        <syntax>
            JG lbl
        </syntax>
        <descr>
            Jumps if SF == 0 and ZF == 0. <br>
            Equivalent name: JLNE
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if (int(vm.flags['SF']) == 0 
            and int(vm.flags['ZF']) == 0):
            raise Jump(target.name)

class Jge(Instruction):
    """
        <instr>
             jge
        </instr>
        <syntax>
            JGE lbl
        </syntax>
        <descr>
            Jumps if SF == 0.
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['SF']) == 0:
            raise Jump(target.name)
        return ''

class Jl(Instruction):
    """
        <instr>
             jl
        </instr>
        <syntax>
            JL lbl
        </syntax>
        <descr>
            Jumps if SF == 1. <br>
            Equivalent name: JGNE
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if int(vm.flags['SF']) == 1:
            raise Jump(target.name)
        return ''

class Jle(Instruction):
    """
        <instr>
             jle
        </instr>
        <syntax>
            JLE lbl
        </syntax>
        <descr>
            Jumps if SF == 1 or ZF == 1.
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        if (int(vm.flags['SF']) == 1
            or int(vm.flags['ZF']) == 1):
            raise Jump(target.name)
        return ''

class Call(Instruction):
    """
        <instr>
             call
        </instr>
        <syntax>
            CALL lbl
        </syntax>
        <descr>
            Pushes value of EIP to stack and jumps to the internal subroutine.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("CALL", ops, 1)
        vm.dec_sp()
        vm.stack[hex(vm.get_sp() + 1).split('x')[-1].upper()] = vm.get_ip()
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Ret(Instruction):
    """
        <instr>
             ret
        </instr>
        <syntax>
            RET
        </syntax>
        <descr>
            Pops value from stack to EIP and returns control to the 
            the line after the subroutine call.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("RET", ops, 0)
        vm.inc_sp()
        vm.set_ip(int(vm.stack[hex(vm.get_sp()).split('x')[-1].upper()]))
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = vm.empty_cell()
