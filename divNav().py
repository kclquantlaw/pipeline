import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from typing import Optional, Any, List, Union, TypeVar, Type, cast, Callable


class Part:
    def __init__(self, Number, Title, Chapters):
        self.Number = Number
        self.Title = Title
        self.Chapters = Chapters


class Chapter:
    def __init__(self, Number, Title, Sections):
        self.Number = Number
        self.Title = Title
        self.Sections = Sections


class SubSection:
    Title: str
    Number: int

    def __init__(self, Number, Title):
        self.Number = Number
        self.Title = Title


class Section:
    Title: str
    SubSections: Optional[List[SubSection]]

    def __init__(self, Title, SubSections):
        self.Title = Title
        self.SubSections = SubSections


def divNav(url):
    parts = []
    urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    for part in soup.select('Body > Part'):
        # print(" "+part.find('Number').text+" "+part.find('Title').text)
        partText = '<li class="subnav__list"><span class="togglePlus" style="cursor:pointer;margin-right:16px">+</span><a href="" style="color:#3ec2b4"><b>' + part.find(
            'Number').text.replace('\n', '') + " " + part.find('Title').text.replace('\n', '') + '</b></a>';
        print(partText)
        chapters = []
        if (len(part.find_all('Chapter')) > 0):
            for chapter in part.find_all('Chapter'):
                # keep chapter
                #                 print(chapter.find('Number').text+" "+chapter.find('Title').text)
                chapterText = '<li class="subnav__list"><span class="togglePlus" style="cursor:pointer;margin-right:16px">+</span><a href="">' + chapter.find(
                    'Number').text + " " + chapter.find('Title').text + '</a> \n <ul class="subnav-third-level">';
                print(chapterText)
                chapters.append(Chapter(chapter.find('Number').text, chapter.find('Title').text, ""))
                if (len(chapter.find_all('Pblock')) > 0):
                    sections = []
                    for result in chapter.find_all('Pblock'):
                        subsections = []
                        # print(" --"+result.find('Title').text)
                        line = '<li class="subnav__list"><span class="togglePlus" style="cursor:pointer;margin-right:16px">+</span><a href="">' + result.find(
                            'Title').text + '</a> <ul class="subnav-third-level">'
                        print(line)
                        for first in result.select('Pblock > P1group'):
                            #                             print("  "+first.select('Pnumber')[0].text+". "+first.find('Title').text)
                            liElement = '<li class="subnav__list"><a href="#' + first.select('Pnumber')[
                                0].text + '" onclick="showText(\'#' + first.select('Pnumber')[
                                            0].text + '\')" role="button" aria-expanded="true">' + \
                                        first.select('Pnumber')[0].text + ". " + first.find('Title').text + '</a> </li>'
                            print(liElement)
                            subsections.append(SubSection(first.select('Pnumber')[0].text, first.find('Title').text))
                            p1 = first.findAll("P1")
                            if p1[0].has_attr('DocumentURI'):
                                # print(p1[0]['DocumentURI'])
                                urls.append(p1[0]['DocumentURI'] + "/data.xml")
                        print('</ul> \n </li>')
                        # print(len(subsections))
                        sections.append(Section(result.find('Title').text, subsections))
                    print('</ul>')
                else:
                    for first in chapter.select('P1group'):
                        # print("  *"+first.select('Pnumber')[0].text+". "+first.find('Title').text)
                        liElement = '<li class="subnav__list"><a href="#' + first.select('Pnumber')[
                            0].text + '" onclick="showText(\'#' + first.select('Pnumber')[
                                        0].text + '\')" role="button" aria-expanded="true">' + first.select('Pnumber')[
                                        0].text + ". " + first.find('Title').text + '</a> </li>'
                        print(liElement)
                        subsections.append(SubSection(first.select('Pnumber')[0].text, first.find('Title').text))
                        p1 = first.findAll("P1")
                        if p1[0].has_attr('DocumentURI'):
                            # print(p1[0]['DocumentURI'])
                            urls.append(p1[0]['DocumentURI'] + "/data.xml")
                    print('</ul> \n </li>')
        else:
            if (len(part.find_all('P1group')) > 0):
                for first in part.select('P1group'):
                    if (len(first.findAll('P1')) > 0):
                        # print("  "+first.select('Pnumber')[0].text+". "+first.find('Title').text)
                        liElement = '<li class="subnav__list"><a href="#' + first.select('Pnumber')[
                            0].text + '" onclick="showText(\'#' + first.select('Pnumber')[
                                        0].text + '\')" role="button" aria-expanded="true">' + first.select('Pnumber')[
                                        0].text + ". " + first.find('Title').text + '</a> </li>'
                        subsections.append(SubSection(first.select('Pnumber')[0].text, first.find('Title').text))
                        p1 = first.findAll("P1")
                        if p1[0].has_attr('DocumentURI'):
                            # print(p1[0]['DocumentURI'])
                            urls.append(p1[0]['DocumentURI'] + "/data.xml")
            for result in part.find_all('Pblock'):
                #                     print(" "+result.find('Title').text)
                # code replication - improve
                line = '<li class="subnav__list"><span class="togglePlus" style="cursor:pointer;margin-right:16px">+</span><a href="">' + result.find(
                    'Title').text + '</a><ul class="subnav-third-level">'
                print(line)
                for first in result.select('Pblock > P1group'):
                    if (len(first.findAll('P1')) > 0):
                        #                                 print("  *"+first.select('Pnumber')[0].text+". "+first.find('Title').text)
                        liElement = '<li class="subnav__list"><a href="#' + first.select('Pnumber')[
                            0].text + '" onclick="showText(\'#' + first.select('Pnumber')[
                                        0].text + '\')" role="button" aria-expanded="true">' + first.select('Pnumber')[
                                        0].text + ". " + first.find('Title').text + '</a> </li>'
                        print(liElement)
                        subsections.append(SubSection(first.select('Pnumber')[0].text, first.find('Title').text))
                        p1 = first.findAll("P1")
                        if p1[0].has_attr('DocumentURI'):
                            # print(p1[0]['DocumentURI'])
                            urls.append(p1[0]['DocumentURI'] + "/data.xml")
                print('</ul> \n </li>')
        parts.append(Part(part.find('Number').text, part.find('Title').text, chapters))

    print(len(parts))

    return urls


url = 'https://www.legislation.gov.uk/ukpga/2004/34/data.xml'
links = divNav(url)
