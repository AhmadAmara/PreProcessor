import os
import sys
import re

def handleMacros(content):
	lines = content.split("\n")
	macros_dic = dict()
	for line in lines:
		line = line.lstrip()
		if(line.startswith("#define")):
			macro = line.replace("#define ", "")
			print(macro)
			if(re.search(r'\w\s+\w', macro)):
				tokens = macro.split()
				macros_dic[tokens[0]] = tokens[1]
				print(tokens[0])
				print(tokens[1])
			content = content.replace(line, "")

	for key in macros_dic.keys():
		content = content.replace(key, macros_dic[key]);
	return content

#creating one file with the name out.pp that conatin all the files we want to proccess
def createOneFile():
	fileToParse = sys.argv[1:]
	with open("out.pp", 'w') as writer:
		for fileName in fileToParse:
			writer.write("\n")

			with open(fileName, 'r') as reader:
				content = handleMacros(reader.read())

				writer.write(content)



if __name__ == "__main__":
	createOneFile()

