from collections import namedtuple
from enum import Enum
import re

HACK_COMMENT = '//'

INITIAL_SYMBOL_ADDRESS = 16

class CommandTypes(Enum):
	A_command = 0
	C_command = 1
	L_command = 2

ParsedLine = namedtuple('ParsedLine', ['type', 'command'])

# Based on constants and symbols, page 72
RE_SYMBOL = '[\w\.\$_:][\d\w\.\$_:]*'
RE_A_COMMAND = '^@(?P<A_value>\d+|{symbol})$'.format(symbol=RE_SYMBOL)
RE_C_DEST = '(?P<C_dest>.+?)'
RE_C_COMP = '(?P<C_comp>.+?)'
RE_C_JUMP = '(?P<C_jump>.+)'
RE_C_COMMAND = '^(?P<C_command>({dest}=)?{comp}(;{jump})?)$'.format(
		dest=RE_C_DEST,
		comp=RE_C_COMP,
		jump=RE_C_JUMP
	)
RE_L_COMMAND = '^\((?P<L_label>{symbol})\)$'.format(symbol=RE_SYMBOL)
RE_COMMAND = '|'.join(command for command in [RE_A_COMMAND, RE_L_COMMAND, RE_C_COMMAND])
RE_COMMAND_PATTERN = re.compile(RE_COMMAND)

def parse(lines):
	"""Parse the code lines, return a list of the commands
		lines: iterator for the lines in the code file
		return: a list of named tuples for the commands"""
	parsed = []

	for line in lines:
		# Remove whitespaces
		line = ''.join(line.split())

		# Remove comments
		try:
			comment_index = line.index(HACK_COMMENT)
			line = line[:comment_index]
		except:
			pass

		# If the line is empty, skip it
		if not line:
			continue

		# Parse non-empty lines
		match = RE_COMMAND_PATTERN.match(line)
		if match.group('A_value'):
			parsed.append(ParsedLine(CommandTypes.A_command, match.group('A_value')))
		elif match.group('C_comp'):
			dest = match.group('C_dest')
			comp = match.group('C_comp')
			jump = match.group('C_jump')
			command = {'dest': dest, 'comp': comp, 'jump': jump}
			parsed.append(ParsedLine(CommandTypes.C_command, command))
		elif match.group('L_label'):
			parsed.append(ParsedLine(CommandTypes.L_command, match.group('L_label')))
		else:
			print("Unable to match line: ", line)

	return parsed

def encode(lines):
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
