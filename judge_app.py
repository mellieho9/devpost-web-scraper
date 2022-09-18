# -*- coding: utf-8 -*-
"""judge_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c0n26yqUWs_FmGS0Hlt1WzZJ3LlhoJ6k
"""

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

baseUrl = 'https://hacknc2021.devpost.com/'
subsUrl = baseUrl + '//submissions?page='


def main():
    count = 1
    fieldsList = []
    while True:
        subsObj = BeautifulSoup(urlopen(subsUrl + str(count)), 'html.parser')
        submissions = subsObj.findAll('a', {'class':'block-wrapper-link fade link-to-software'})
        if len(submissions) != 0:
            for submission in submissions:
                subUrl = submission.attrs['href']
                subObj = BeautifulSoup(urlopen(subUrl), 'html.parser')

                title = getTitle(subObj)
                subtitle = getSubtitle(subObj, title)
                members = getMembers(subObj)
                builtWith = getBuiltWith(subObj)
                fieldsList.append([title.get_text().strip(), subtitle.get_text().strip(), images, builtWith])
            count = count + 1
        else:
            break
    writeToCSV(fieldsList)


def getTitle(subObj):
    title = subObj.find('h1', {'id':'app-title'})
    return title


def getSubtitle(subObj, title):
    subtitle = title.parent.find('p')
    return subtitle

def getMembers(subObj):
  memberList = []
  members = subObj.find('section',{'id':'app-team'}).findAll('a',{'class':'user-profile-link'})
  for member in members:
    memberList.append(member.get_text().strip())
  return memberList


def getBuiltWith(subObj):
    builtWithList = []
    try:
        builtWith = subObj.find('div', {'id':'built-with'}).findAll('span', {'class':'cp-tag'})
        for tool in builtWith:
            builtWithList.append(tool.get_text().strip())
    except:
        print('No Tools Found')
    return builtWithList

def getTrack(subObj):
  track = subObj.find('div',{'class':'panel'}).find('label',{'class':'checkbox','checked':'checked'})

def writeToCSV(fieldsList):
    csvFile = open('data/data.csv', 'wt')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('Title', 'Subtitle', 'Members','Built With'))
        for row in fieldsList:
            writer.writerow((row[0], row[1], row[2], row[3]))
    finally:
        csvFile.close()


main()