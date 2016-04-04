from collections import namedtuple

class CommandTypes(Enum):
	A_command = 0
	C_command = 1
	L_command = 2

ParsedLine = namedtuple('ParsedLine', ['type', 'command'])

def parse(lines):
"""Parse the code lines, return a list of the commands
    linesIter: iterator for the lines in the code file
    return: a list of named tuples for the commands"""
	pass

def encode(lines)
"""Receives a list of commands as output by the parser, and encodes
string for the command"""
	pass

def resloveSymbols(lines):
"""Receives a list of parsed lines, resolves the symbols and references
    lines: List of lines as output by parser
    return: List of lines, with symbols resolved"""
	pass

def assemble(lines):
"""Manage the assembly process"""
	pass
