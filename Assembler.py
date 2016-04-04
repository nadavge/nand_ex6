from collections import namedtuple

INITIAL_SYMBOL_ADDRESS = 16

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

	resolvedLines = []
	symbolTable = {'SP':    0,
		'LCL':   1,
		'ARG':   2,
		'THIS':  3,
		'THAT':  4,
		'SCREEN':16384,
		'KBD':   24576}

	for i in range(16):
		symbolTable['R' + str(i)] = i

	# Used to hold the effective line number after extraction of the L commands
	currLine = 0

	# Iterate over the lines of the code, save all label locations
	for line in lines:
		# If label, save the current line, otherwise advance the line
		if line.type == CommandTypes.L_command:
			symbolTable[line.command] = currLine
		else:
			currLine += 1

	# RAM places counter
	currSymbolAddr = INITIAL_SYMBOL_ADDRESS

	# Iterate over the lines of code, replace references to symbols.
	# In case of unknown symbol, allocate a RAM address incrementally
	for line in lines:
		# Skip L commands
		if line.type == CommandTypes.L_command:
			continue

		# If A command and not numeric, resolve
		elif line.type == CommandTypes.A_command and not line.command.isnumeric():
			if line.command not in symbolTable:
				symbolTable[line.command] = currSymbolAddr
				currSymbolAddr += 1

			# All symbol values are passed as str.. sorry
			symbolVal = str(symbolTable[line.command])
			resolvedLines.append(ParsedLine(line.type, symbolVal))

		else:
			resolvedLines.append(line)

	return resolvedLines

def assemble(lines):
"""Manage the assembly process"""
	pass
