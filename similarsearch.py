# David Son 7/12/19
# This program takes an input of the field and
# text to search for and outputs all similar
# versions of that word.

import decimal

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
    descCount = {}

    # Use some natural language processing to extract unique values and insert
    # into a dictionary. if there are equivalent values, increase that specific counter.
    for i in newList:
        subStart = i.index('\"' + field + '\"')
        subEnd = i.index('\",\"', subStart)
        compName = i[subStart:subEnd]
        cStart = compName.index(':\"')
        cleanName = compName[cStart+2:]

        if cleanName in similarCount:
            similarCount[cleanName] = similarCount.get(cleanName) + 1
        else :
            similarCount[cleanName] = 1
        
        descStart = i.index('\"Description\":')
        descEnd = i.index('\",\"', descStart)
        descName = i[descStart:descEnd]
        descFull = descName.index(':\"')
        cleanDesc = descName[descFull+2:]
        splitDesc = cleanDesc.split(' ')

        # Get a count of important words within each description.
        for j in splitDesc:
            if j in descCount:
                descCount[j] = descCount.get(j) + 1
            else :
                descCount[j] = 1

    print("\nFinished parsing data.\n")
    print("Results:")
    print("Total Found:", lineCount,"\n")
    print("All similar words:\n")

    # Print out each dictionary item and how many times it was found/percentage of all
    # documents with that word or phrase.
    for key,val in sorted(similarCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True):
        print("Word: {:30s} Count: {:4d} Ratio: {:4s}".format(key,val,str(round(((val/lineCount)*100),2))+"%"))

    print("\nThese are the top ten words for this topic:\n")

    #Print the top 10 words in the descriptions of a certain job or topic.
    count = 1
    for key,val in sorted(descCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)[0:10]:
        print("{:3s} Word: {:10s} Count: {:4d}".format(str(count)+".","\""+key+"\"",val))
        count += 1

main()