import os
import sys
import re


# def parseFuncMacro(funcMacro):
# constants_dict = dict()
# funcMacro_dict = dict()

# def handleMacros(content):
# 	global constants_dict, funcMacro_dict

# 	with open(out.pp, 'r') as reader:
# 		lines = content.split("\n")
		
# 		lines = reader.readlines()

# 		# macros_dic = dict()
# 		# simpleMacro_dic = dict()

# 		for line in lines:
# 			line = line.lstrip()
# 			if(line.startswith("#define")):
# 				# macro = line.replace("#define ", "")
# 				# print(macro)
# 				# if(re.search(r'\w\s+\w', macro)):)
# 					# tokens = macro.split()
# 					# macros_dic[tokens[0]] = tokens[1]
# 					# print(tokens[0])
# 					# print(tokens[1])
# 				# matched = re.search(r'\s*(\w+)\s*\(\s*((\w+)\s*(,\s*\w+\s*))*\)\s*(.)*$', line)
# 				# if matched:

# 					# print(matched.group(0))
# 					# print(matched.group(1))
# 					# print(matched.group(2))
# 					# print(matched.group(3))
# 					# print((line.split()[2:]))

# 					# print("".join((line.split()[3:])))
# 					macro_compoents = line.split()
# 					# print(macro_compoents)
# 					# print("$$$")
# 					# print("".join(macro_compoents[3:]))
# 					# print(macro_compoents[1].split("(")[0])
# 					if(len(macro_compoents) == 3):
# 						print(macro_compoents)
# 						constants_dict[macro_compoents[1].split("(")[0]] = "".join(macro_compoents[2:])
# 					else:	
# 						funcMacro_dict[macro_compoents[1].split("(")[0]] = "".join(macro_compoents[3:])

# 					content = content.replace(line, "")


# 	# for key in macros_dic.keys():
# 	# 	matched = re.search(r'\s*(\w+)\s*\(\s*((\w+)\s*(,\s*\w+\s*))*\)\s*', key):
# 	# 	if matched:
# 	# 		print()
# 	# 	content = content.replace(key, parseFuncMacro(macros_dic[key]));
# 	# return content

# #creating one file with the name out.pp that conatin all the files we want to proccess
# def HandleOneFile(fileName):
# 	headers = []
# 	with open(fileName, 'r') as reader:
# 		lines = reader. readlines()
# 		for line in lines:
# 			if line.startswith("#include"):
# 				if "\"" in line:
# 					headers.append((line.split()[1]).replace("\"", ""))
# 	# if fileName.endwith("cpp"):
# 	# 	with open(fileName.replace("cpp", "pp"), 'w') as writer:
# 	# 		print(fileName.replace("cpp", "pp"))
# 	# 		# for fileName in filesToParse:
# 	# 		# 	writer.write("\n")
# 	# 		with open(fileName, 'r') as reader:
# 	# 			ppContent = reader.read()#handleMacros(reader.read())
				
# 	# 			writer.write(ppContent)

# 	# else:
# 	# 	with open(fileName, 'r') as reader:
# 	# 			headerContent = reader.read()

# realtedFiles = []

# def getheaders(fileNamem, noHeaderFlag):
# 	global realtedFiles, definesFlag
# 	if noHeaderFlag:
# 		print(realtedFiles)
# 		return

# 	else:
# 		realtedFiles.append(fileName)
# 		print(realtedFiles)
# 		with open(fileName, 'r') as reader:
# 			lines = reader.readlines()
# 			for line in lines:
# 				if line.startswith("#include"):
# 					if "\"" in line:
# 						print(line)
# 						# headers.append((line.split()[1]).replace("\"", ""))
# 						# headers.append((line.split()[1])
# 						return getheaders(line.split()[1], False)

# 			return getheaders("", True)



ppLines = []
definesFlag = []

def parse_one_file(fileName):
	global ppLines, definesFlag
	with open(fileName, 'r') as reader:
		lines = reader.readlines()
		for line in lines:
			if "pragma once" in line:
				print(line)
				if fileName in definesFlag:
					break;
				else:
					definesFlag.append(fileName)
			elif "ifndef" in line:
				if fileName in definesFlag:
					# print(line)
					break;
				else:
					print(line)
					definesFlag.append(fileName)

			elif line.startswith("#include"):
				if "\"" in line:
					print(line.split()[1].replace("\"", ""))
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

		# realtedFile = getheaders(fileName, False)
		# print(realtedFile)
		# HandleOneFile(fileName)
		

