from collections import namedtuple
import re

HACK_COMMENT = '//'

class CommandTypes(Enum):
	A_command = 0
	C_command = 1
	L_command = 2

ParsedLine = namedtuple('ParsedLine', ['type', 'command'])

# Based on constans and symbols, page 72
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
RE_L_COMMAND = '^\(?P<L_label>{symbol}\)$'.format(symbol=RE_SYMBOL)
RE_COMMAND = '|'.join(command for command in [RE_A_COMMAND, RE_C_COMMAND, RE_L_COMMAND])
RE_COMMAND_PATTERN = re.compile(RE_COMMAND)

def parse(lines):
"""Parse the code lines, return a list of the commands
    linesIter: iterator for the lines in the code file
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
