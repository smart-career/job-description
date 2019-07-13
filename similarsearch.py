# David Son 7/12/19
# This program takes an input of the field and
# text to search for and outputs all similar
# versions of that word.

def main():
    newFile = input("What is the file name? ")
    field = input("What is the field you are looking for? ")
    newText = input("What is the text you are looking for? ")
    fieldText = field + "\"" + ":" + "\"" + newText

    lineCount = 0
    newList = []

    with open(newFile, encoding="utf8") as thisFile:
        for line in thisFile:
            if fieldText in line:
                newList.append(line)
                lineCount += 1

    similarCount = {}
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
    for key,val in sorted(similarCount.items(), key = lambda kv:(kv[1], kv[0])):
        print(key, "=>", val, "|", (val/lineCount)*100,"%")

main()