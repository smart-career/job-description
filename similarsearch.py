# David Son 7/12/19
# This program takes an input of the field and
# text to search for and outputs all similar
# versions of that word.

def main():
    # Take in the 3 user inputs (file, field, word to search for)
    newFile = input("What is the file name? ")
    field = input("What is the field you are looking for? ")
    newText = input("What is the text you are looking for? ")
    fieldText = field + "\"" + ":" + "\"" + newText

    lineCount = 0
    newList = []

    # Open a file and parse through each document and add it to a list.
    with open(newFile, encoding="utf8") as thisFile:
        for line in thisFile:
            if fieldText in line:
                newList.append(line)
                lineCount += 1

    similarCount = {}

    # Use some natural language processing to extract unique values and insert
    # into a dictionary. if there are equivalent values, increase that specific counter.
    for i in newList:
        subStart = i.index(field)
        subEnd = i.index('\",\"', subStart)
        compName = i[subStart:subEnd]
        cStart = compName.index(':\"')
        cleanName = compName[cStart+2:]
        if cleanName in similarCount:
            similarCount[cleanName] = similarCount.get(cleanName) + 1
        else :
            similarCount[cleanName] = 0

    print()
    print("Finished parsing data.")
    print("Results:")
    print("Line Count:", lineCount)
    print()

    # Print out each dictionary item and how many times it was found/percentage of all
    # documents with that word or phrase.
    for key,val in sorted(similarCount.items(), key = lambda kv:(kv[1], kv[0])):
        print(key, "=>", val, "|", (val/lineCount)*100,"%")

main()