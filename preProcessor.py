import os
import sys
import re
import glob


def placefuncMacro(line, name, component_dict):
	matched = re.search(r'\s*((\w+)\s*\(\s*((\w+)\s*(,\s*\w+\s*))*\))\s*(.)*$', line)

	argments = matched.group(3).split(",")
	params = component_dict["params"].split(",")
	macro_result = component_dict["func"]

	i = 0;
	for arg in argments:
		arg = arg.lstrip().rstrip()
		toReplace = params[i].lstrip().rstrip()
		macro_result = macro_result.replace(toReplace, arg);
		i += 1

	line = line.replace(matched.group(1), macro_result)

	return line


def plantMacros(fileName):
	global constants_dict, funcMacro_dict, ppLines
	with open(fileName, 'r') as reader:
		lines = reader.readlines()

		for line in lines:
			if("#define" in line):
				continue
			else:	
				for key in constants_dict.keys():
					if key in line:
						line = line.replace(key, constants_dict[key])

				for key in funcMacro_dict.keys():
					if key in line:
						line = placefuncMacro(line, key, funcMacro_dict[key])	
				ppLines.append(line)
				
	create_pp_output(fileName)


constants_dict = dict()
funcMacro_dict = dict()


def collectMacros(fileName):
	global constants_dict, funcMacro_dict
	with open(fileName, 'r') as reader:
		lines = reader.readlines()
		for line in lines:
			line = line.lstrip()
			if(line.startswith("#define")):
				macro_compoents = line.split()

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
				if fileName in definesFlag:
					break;
				else:
					definesFlag.append(fileName)
			elif "ifndef" in line:
				if fileName in definesFlag:
					break;
				else:
					definesFlag.append(fileName)

			elif line.startswith("#include"):
				if "\"" in line:
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
		constants_dict = {}
		funcMacro_dict = {}
		collectMacros(ppFileName)
		ppLines = []
		plantMacros(ppFileName)

		

