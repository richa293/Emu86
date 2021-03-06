#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".")


from unittest import TestCase, main

from assembler.virtual_machine import intel_machine, STACK_BOTTOM, STACK_TOP
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
from assembler.errors import MISSING_COMMA, MISSING_DATA, INVALID_TOKEN
from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
from assembler.errors import UNKNOWN_NM


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        (output, error) = assemble("shove_up_reg $1, %eax", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        (output, error) = assemble("mov $666, (hell)", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        (output, error) = assemble("add $10, $22, $34, %eax", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

# we have to clear up symbol handling to make this test work.
#    def test_unknown_name(self):
#        (output, error) = assemble("add fred, wilma", intel_machine)
#        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        (output, error) = assemble("mov $10, %EIP", 'att', intel_machine)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_stack_overflow(self):
        intel_machine.registers["ESP"] = STACK_BOTTOM-1
        (output, error) = assemble("push $1", 'att', intel_machine)
        self.assertTrue(error.startswith(STACK_OVERFLOW))

    def test_stack_underflow(self):
        intel_machine.registers["ESP"] = STACK_TOP
        (output, error) = assemble("pop %ebx", 'att', intel_machine)
        self.assertTrue(error.startswith(STACK_UNDERFLOW))

    def test_comma_error(self):
        (output, error) = assemble("mov $1 %eax", 'att', intel_machine)
        self.assertTrue(error.startswith(MISSING_COMMA))

    def test_comma_error(self):
        (output, error) = assemble("mov $1,,,, %eax", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_data_error(self):
        (output, error) = assemble(".data \n  x: .short", 'att', intel_machine)
        self.assertTrue(error.startswith(MISSING_DATA))

    def test_mem_error_over(self):
        (output, error) = assemble("mov $0, (256)", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_mem_error_less(self):
        (output, error) = assemble("mov $0, (-30)", 'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))


if __name__ == '__main__':
    main()
