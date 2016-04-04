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

def resolveSymbols(lines):
"""Receives a list of parsed lines, resolves the symbols and references
    lines: List of lines as output by parser
    return: List of lines, with symbols resolved"""

        symbolTable = {"SP":    0,
                       "LCL":   1,
                       "ARG":   2,
                       "THIS":  3,
                       "THAT":  4,
                       "SCREEN":16384,
                       "KBD":   24576}

        for i in range(16):
                symbolTable["R" + str(i)] = i
        
        currSymbolLine = 1024

        resolvedLines = []

        for line in lines:
                if line.type == CommandTypes.L_command or line.type == CommandTypes.A_command and type(line.command)==str:
                        if line.command not in symbolTable:
                                symbolTable[line.command] = currSymbolLine
                                currSymbolLine += 1

                        if line.type == CommandTypes.A_command:
                                line.command = symbolTable[line.command]

                if line.type != CommandTypes.L_command:
                        resolvedLines.append(line)

        return resolvedLines

def assemble(lines):
"""Manage the assembly process"""
	pass
