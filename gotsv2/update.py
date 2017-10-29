import requests
from django.utils import timezone
import pandas
import re
from bs4 import BeautifulSoup
from .models import Character

class Update():
    def __init__(self):
        r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        self.all = soup.find_all("span", {"class": "mw-headline"})
        regex = (
        '(House|References|Secondary sources|Primary sources|Bibliography|External links|Other characters|Royal court and officials|Night\\\'s Watch and wildlings|The Sand Snakes)')
        self.p = re.compile(regex)
        self.namelist = []
        self.linklist = []
        self.checklist = []
        self.infolist = []

    # def generatelinks(self):
    #     # a = 0
    #     for item in self.all:
    #         name = item.text
    #         # while a <= 5:
    #         if self.p.match(name) is None:
    #             # gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
    #             if name == "Eddard Stark":
    #                 self.namelist.append("Ned Stark")
    #                 rightname = "Ned_Stark"
    #                 url = str("https://en.wikipedia.org/wiki/" + rightname)
    #                 self.linklist.append(url)
    #                 # a = a + 1
    #             else:
    #                 self.namelist.append(name)
    #                 urlend = name.replace(" ", "_")
    #                 underscore = "_"
    #                 if urlend.endswith(underscore):
    #                     # takes off the last underscore if present using indexing
    #                     urlend = urlend[0:-1]
    #                         # print(urlend)
    #                     url = str("https://en.wikipedia.org/wiki/" + urlend)
    #                     self.linklist.append(url)self.
    #                     # a = a + 1
    #         else:
    #             pass
    #             # a = a + 1
    def generatelinks(self):
        for item in self.all:
            name = item.text
            if self.p.match(name) is None:
                # gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
                if name == "Eddard Stark":
                    self.namelist.append("Ned Stark")
                    rightname = "Ned_Stark"
                    url = str("https://en.wikipedia.org/wiki/" + rightname)
                    self.linklist.append(url)
                else:
                    self.namelist.append(name)
                    urlend = name.replace(" ", "_")
                    underscore = "_"
                    if urlend.endswith(underscore):
                        # takes off the last underscore if present using indexing
                        urlend = urlend[0:-1]
                        # print(urlend)
                    url = str("https://en.wikipedia.org/wiki/" + urlend)
                    self.linklist.append(url)
            else:
                pass


                # character page exists checker - scrapes for redirect link text (this is the name of the character if redirected to
                # the 'list of characters' page

    def linkscrape(self):
        a = 0
        for item in self.linklist:
            request = requests.get(item)
            z = request.content
            global soup2
            soup2 = BeautifulSoup(z, "html.parser")
            if "may refer to" in soup2.text:
                self.trychar(request, item)
            else:
                try:
                    redirected = soup2.find("a", {"class:", "mw-redirect"}).text
                    if redirected == self.namelist[a]:
                        self.checklist.append("No")
                        self.infolist.append("")
                    else:
                        self.getinfobox(item)
                except:
                    self.checklist.append("No")
                    self.infolist.append("")
            print(str(a) + " of 124 entries checked")
            a = a + 1

    def trychar(self, request, item):
        try:
            request2 = requests.get(str(item) + "_(character)")
            y = request2.content
            soup3 = BeautifulSoup(y, "html.parser")
            infobox2 = soup3.find(("table", {"class:", "infobox"}))
            infobox = infobox2.encode('utf-8').strip()
            if "Male" or "Female" in infobox:
                self.checklist.append("Yes")
                self.infolist.append(infobox)
            else:
                self.checklist.append("No")
                self.infolist.append("")
        except:
            self.checklist.append("No")
            self.infolist.append("")

    def getinfobox(self, item):
        try:
            table = soup2.find_all(("table", {"class:", "infobox"}))
            infobox = table[0].encode('utf-8').strip()
            if str(infobox).startswith("b'<table class=\"infobox\""):
                self.checklist.append("Yes")
                self.infolist.append(infobox)
            else:
                self.refineinfobox(item, table)
        except:
            self.checklist.append("No")
            self.infolist.append("")

    def refineinfobox(self, item, table):
        t = False
        for i in range(4):
            if "infobox" in str(table[i]):
                print(i)
                index = i
                t = True
                break
        while t is True:
            print("saved")
            infobox = table[index].encode('utf-8').strip()
            self.checklist.append("Yes")
            self.infolist.append(infobox)
            break
        if t is False:
            print("nothing saved")
            self.checklist.append("No")
            self.infolist.append("")
        print("done")


    def CharacterModelUpdate(self):
        # print(self.namelist)
        # print(self.linklist)
        # print(self.checklist)
        # print(self.infolist)
        df = pandas.DataFrame(
            {'Names': self.namelist,
             'URLs': self.linklist,
             'Pages': self.checklist,
             'Infoboxes': self.infolist})
        print(df)
        # df_reordered = df[['Names', 'URLs', 'Pages', 'Infoboxes']]
        # print(df_reordered)

        # a = 2
        # for row in df_reordered.loc[a]:
        #     print(row)
        #     a = a + 1

        # characters = [
        #     {
        #         'name': 'Stark',
        #         'url': '#',
        #     },
        #     {
        #         'name': 'Bolton',
        #         'url': '#',
        #     },
        #     {
        #         'name': 'Lannister',
        #         'url': '#',
        #     }
        # ]

        # for character in characters:


        # for item in df['Name']:
        #     # 1. Make a new Character object
        #     # 2. Save the name from namelist to the new character
        #     # m = Character(name=n, url='#', page=1, infobox='.', created_at=timezone.now(), updated_at=timezone.now())
        #     print('ok')
        #     # 3. Persist the new Character to the database (save())
        #     # m.save()
