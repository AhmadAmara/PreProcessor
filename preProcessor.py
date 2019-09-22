import os
import sys
import re
import glob




constants_dict = dict()
funcMacro_dict = dict()


def collectMacros(fileName):

	with open(fileName, 'r') as reader:
		lines = reader.readlines()
		for line in lines:
			line = line.lstrip()
			if(line.startswith("#define")):
				macro_compoents = line.split()
				# print(macro_compoents)

				if(len(macro_compoents) == 3):
						constants_dict[macro_compoents[1].split("(")[0]] = "".join(macro_compoents[2:])
				else:	
					matched = re.search(r'\s*(\w+)\s*\(\s*((\w+)\s*(,\s*\w+\s*))*\)\s*(.)*$', line)
					if matched:
						# print("matched.group(0)",matched.group(0))
						# print("matched.group(1)",matched.group(1))
						# print("matched.group(2)",matched.group(2))
						# print("matched.group(3)",matched.group(3))
						# print("".join(macro_compoents[3:]))
						funcMacro_dict[matched.group(1)] = {"params": matched.group(2), "func" : "".join(macro_compoents[3:]) }

				

ppLines = []
definesFlag = []

def parse_one_file(fileName):
	global ppLines, definesFlag
	with open(fileName, 'r') as reader:
		lines = reader.readlines()
		for line in lines:
			if "pragma once" in line:
				# print(line)
				if fileName in definesFlag:
					break;
				else:
					definesFlag.append(fileName)
			elif "ifndef" in line:
				if fileName in definesFlag:
					# print(line)
					break;
				else:
					# print(line)
					definesFlag.append(fileName)

			elif line.startswith("#include"):
				if "\"" in line:
					# print(line.split()[1].replace("\"", ""))
					parse_one_file(line.split()[1].replace("\"", ""))
			else:
				ppLines.append(line)


def create_pp_output(fileName):
	global ppLines
	with open(fileName.replace("cpp", "pp"), 'w') as writer:
		for line in ppLines:
			writer.write(line)


if __name__ == "__main__":
	filesToParse = sys.argv[1:]
	for fileName in filesToParse:
		ppLines = []
		definesFlag = []
		parse_one_file(fileName)
		create_pp_output(fileName)

	for ppFileName in glob.glob("*.pp"):
		collectMacros(ppFileName)
	
		# realtedFile = getheaders(fileName, False)
		# print(realtedFile)
		# HandleOneFile(fileName)
		

