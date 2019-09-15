import os
import sys



#creating one file with the name out.pp that conatin all the files we want to proccess
def createOneFile():
	fileToParse = sys.argv[1:]
	with open("out.pp", 'w') as writer:
		for fileName in fileToParse:
			writer.write("\n")

			with open(fileName, 'r') as reader:
				# lines = reader.read()

				writer.write(reader.read())


if __name__ == "__main__":
	createOneFile()

