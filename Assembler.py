from collections import namedtuple
from enum import Enum
import os
import sys
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


compDict = {
		'0':	 '1110101010',
		'1':	 '1110111111',
		'-1':	 '1110111010',
		'D':	 '1110001100',
		'A':	 '1110110000',
		'!D':	 '1110001101',
		'!A':	 '1110110001',
		'-D':	 '1110001111',
		'-A':	 '1110110011',
		'D+1':   '1110011111',
		'A+1':   '1110110111',
		'D-1':   '1110001110',
		'A-1':   '1110110010',
		'D+A':   '1110000010',
		'D-A':   '1110010011',
		'A-D':   '1110000111',
		'D&A':   '1110000000',
		'D|A':   '1110010101',
		'D<<':   '1010110000',
		'A<<':   '1010100000',
		'D>>':   '1010010000',
		'A>>':   '1010000000'
	}

"""Operations for A and M only differ in the a-bit,
located at the the fourth location in the string (index == 3)
A = 0
M = 1
"""
a_BIT = 3

# Iterate over all keys where A is involved
for key in [k for k in compDict if 'A' in k]:
	mVal = compDict[key]
	# Replace the a-bit with 1 for M
	mVal = mVal[:a_BIT] + '1' + mVal[a_BIT+1:]
	compDict[key.replace('A', 'M')] = mVal

# A dictionary to resolve jump operations, setting the j1,j2,j3 bits
jumpDict = {
		None:	'000',
		'JGT':  '001',
		'JEQ':  '010',
		'JGE':  '011',
		'JLT':  '100',
		'JNE':  '101',
		'JLE':  '110',
		'JMP':  '111'
	}

def encode(lines):
	"""Receives a list of commands as output by the parser, and encodes
	string for the command"""

	encoded = []

	for line in lines:
		if line.type == CommandTypes.A_command:
			value = int(line.command)
			encodedLine = format(value, '016b')

		elif line.type == CommandTypes.C_command:
			command = line.command
			dest = command['dest']
			comp = command['comp']
			jump = command['jump']

			if dest is None:
				dest = ''

			# The order ADM was chosen based on their order bit-wise
			destBinary = ''.join('1' if register in dest else '0' for register in 'ADM')
			encodedLine = compDict[comp] + destBinary + jumpDict[jump]

		encoded.append(encodedLine)

	return encoded


def resolveSymbols(lines):
	"""Receives a list of parsed lines, resolves the symbols and references
		lines: List of lines as output by parser
		return: List of lines, with symbols resolved"""

	resolvedLines = []
	symbolTable = {
			'SP':    0,
			'LCL':   1,
			'ARG':   2,
			'THIS':  3,
			'THAT':  4,
			'SCREEN':16384,
			'KBD':   24576
		}

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
	parsed = parse(lines)
	resolved = resolveSymbols(parsed)
	code = encode(resolved)

	return code


def assemble_file(file_path):
	"""Assemble a file by filepath, save the result"""
	with open(file_path, 'r') as file:
		code = assemble(file.readlines())

		file_no_ext, _ = os.path.splitext(file_path)
		ofile_path = file_no_ext+'.hack'
		with open(ofile_path, 'w') as ofile:
			ofile.write('\n'.join(code))


def batch_assembly(dir_path):
	"""Batch assemble a directory, save all files to matching names as required"""
	for file in os.listdir(dir_path):
		file_path = os.path.join(dir_path, file)
		_, file_ext = os.path.splitext(file_path)
		# Choose only asm files
		if os.path.isfile(file_path) and file_ext.lower()=='.asm':
			code = assemble_file(file_path)


def main():
	"""The main program, loading the file and calling the assembler"""
	if len(sys.argv) < 2:
		print("Missing file parameter... Failure")
		sys.exit(1)

	input_path = sys.argv[1]

	if os.path.isdir(input_path):
		batch_assembly(input_path)
	elif os.path.isfile(input_path):
		assemble_file(input_path)
	else:
		print("Invalid argument supplied!")
		sys.exit(1)


if __name__=="__main__":
	main()
