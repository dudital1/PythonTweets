import csv
import re
import pandas as pd

def listHashTag(string):
    '''Creating a list of HashTags from string'''
    if (type(string) != str):
        return []
    hashTags = re.finditer('(#[\w_-]+)', string)
    tags = list()
    for a in hashTags:
        if ((a.group(0).lower() != "#btc") and (a.group(0).lower() != "#bitcoin") and (
                a.group(0).lower() != "#bitcoins")):
            tags.append(a.group(0))
    return tags

def listUserName(string):
    '''Creating a list of user names from string'''
    if (type(string) != str):
        return []
    userNames = re.finditer('(@[\w_-]+)', string)
    name = list()
    for a in userNames:
        name.append(a.group())
    return name

def listUrl(string):
    '''Creating a list of websites from string'''
    if (type(string) != str):
        return []
    urls = re.finditer('http([^\s"]*)://(?P<base>[^/\s]+)', string)
    url = list()
    for a in urls:
        url.append(a.group("base"))
    return url

def arrangeData(inFile):
    '''Create a dict of all the data from the CSV - key as month and value of lists of "Hashtag","Mention" and "Website"'''
    tmpDict = {}
    try:
        with open(inFile, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i, entry in enumerate(reader):
                time = str(entry["timestamp"])[:7]
                if not time in tmpDict:
                    tmpDict[time] = {"tags": list(), "urls": list(), "names": list()}
                tmpDict[time]["tags"].extend(listHashTag(entry["text"]))
                tmpDict[time]["names"].extend(listUserName(entry["text"]))
                tmpDict[time]["urls"].extend(listUrl(entry["text"]))
        return tmpDict
    except:
        print("An exception occurred - Couldn't open file to read")

def generateCsv(tmpDict, outputFile):
    '''Save the dict as CSV and run mode() on all sections'''
    try:
        with open(outputFile, "w", newline='', encoding='utf-8') as file:
            firstLine = ["Month", "Hashtag", "Mention", "Website"]
            writer = csv.DictWriter(file, firstLine)
            writer.writeheader()
            for key in sorted(tmpDict):
                tmpMode = {}
                tmpMode["Month"] = key
                if tmpDict[key]["tags"]:
                    tmpMode["Hashtag"] = pd.Series.mode(tmpDict[key]["tags"]).iloc[0]
                else:
                    tmpMode["Hashtag"] = ("None")
                if tmpDict[key]["names"]:
                    tmpMode["Mention"] = pd.Series.mode(tmpDict[key]["names"]).iloc[0]
                else:
                    tmpMode["Mention"] = ("None")
                if tmpDict[key]["urls"]:
                    tmpMode["Website"] = pd.Series.mode(tmpDict[key]["urls"]).iloc[0]
                else:
                    tmpMode["Website"] = ("None")
                writer.writerow(tmpMode)
    except:
        print("An exception occurred - Couldn't open file to write")

if __name__ == '__main__':
    inputFile = 'tweets.csv'
    outputFile = 'tweet-data.csv'
    jsonFile = arrangeData(inputFile)
    if jsonFile:
        generateCsv(jsonFile, outputFile)