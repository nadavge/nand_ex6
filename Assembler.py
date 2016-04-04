from collections import namedtuple
from enum import Enum

class CommandTypes(Enum):
	A_command = 0
	C_command = 1
	L_command = 2

ParsedLine = namedtuple('ParsedLine', ['type', 'command'])

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

for key in list(compDict.keys()):
	if 'A' in key:
		mVal = compDict[key]
		mVal = list(mVal)
		mVal[a_BIT] = '1'
		mVal = ''.join(mVal)
		compDict[key.replace('A', 'M')] = mVal

jumpDict = {None:	'000',
	     'JGT':      '001',
	     'JEQ':      '010',
	     'JGE':      '011',
	     'JLT':      '100',
	     'JNE':      '101',
	     'JLE':      '110',
	     'JMP':      '111'}

def parse(lines):
	"""Parse the code lines, return a list of the commands
	    linesIter: iterator for the lines in the code file
	    return: a list of named tuples for the commands"""
	pass

def encode(lines):
	"""Receives a list of commands as output by the parser, and encodes
	    string for the command"""

	encoded = []

	for line in lines:
		if line.type == CommandTypes.A_command:
			encodedLine = str(bin(line.command))[2:].rjust(16, '0')

		elif line.type == CommandTypes.C_command:
			command = line.command
			dest = command.dest
			comp = command.comp
			jump = command.jump

			if dest is None:
				dest = ''

			# The order ADM was chosen based on their order bit-wise
			destBinary = ''.join('1' if register in dest else '0' for register in 'ADM')
			encodedLine = compDict[comp] + destBinary + jumpDict[jump]

		encoded.append(encodedLine)

	return encoded

def resloveSymbols(lines):
	"""Receives a list of parsed lines, resolves the symbols and references
	    lines: List of lines as output by parser
	    return: List of lines, with symbols resolved"""
	pass

def assemble(lines):
	"""Manage the assembly process"""
	pass
