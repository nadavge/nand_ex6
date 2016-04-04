from collections import namedtuple

class CommandTypes(Enum):
	A_command = 0
	C_command = 1
	L_command = 2

ParsedLine = namedtuple('ParsedLine', ['type', 'command'])

compDict = {'0':        '0101010',
            '1':        '0111111',
            '-1':       '0111010',
            'D':        '0001100',
            'A':        '0110000',
            '!D':       '0001101',
            '!A':       '0110001',
            '-D':       '0001111',
            '-A':       '0110011',
            'D+1':      '0011111',
            'A+1':      '0110111',
            'D-1':      '0001110',
            'A-1':      '0110010',
            'D+A':      '0000010',
            'D-A':      '0010011',
            'A-D':      '0000111',
            'D&A':      '0000000',
            'D|A':      '0010101'}

for key in compDict:
        if 'A' in key:
                aVal = compDict[key]
                mVal = '1' + aVal[1:]
                compDict[key.replace('A', 'M')] = mVal

jumpDict = {None:       '000',
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

def encode(lines)
"""Receives a list of commands as output by the parser, and encodes
    string for the command"""

        encoded = []

        for line in lines:
                if line.type == CommandTypes.A_command:
                        encodedLine = str(bin(line.command))[2:].rjust(16, '0')
                else:
                        command = line.command
                        dest = command.dest
                        comp = command.comp
                        jump = command.jump

                        if dest is None:
                                dest = ""

                        # The order ADM was chosen based on their order bit-wise
                        destBinary = "".join('1' if register in dest else '0' for register in 'ADM')

                        encodedLine = "111" + compDict[comp] + destBinary + jumpDict[jump]

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
