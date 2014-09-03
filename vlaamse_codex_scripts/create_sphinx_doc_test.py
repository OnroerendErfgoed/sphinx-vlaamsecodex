import requests, json
import os
from collections import OrderedDict 

codex_vlaanderen_url = 'http://codexws.vlaanderen.be'
decreeturl = codex_vlaanderen_url + "/Hoofdstuk/ListByParentId/"
artikelurl = codex_vlaanderen_url + "/Artikel/ListByHoofdstukId/"



class Chapter:
    def __init__(self, chapterid, title, children, chaptertype):
        self.id = chapterid
        self.children = children
        self.title = title.encode('utf8')
        self.sections = []
        self.articles = []
        self.mainchapter = chaptertype

    def add_section(self, recid, title, children):
        self.section.append(Afdeling(recid, title, children))

    def add_article(self, artnr, recid):
        self.articles.append(Article(artnr, recid))

    def get_line(self, char):
        line=""
        for i in range(len(self.title)-2):
            line += char
        return line + "\n"

    def get_headtitle(self):
        title = self.get_line("-")+self.title+self.get_line("-")+"\n"
        return title

    def get_subtitle(self):
        subtitle = "\n\n"+self.title+self.get_line("^")+"\n"
        return subtitle

    def get_subsubtitle(self):
        title=self.title.replace("\r\n","")
        subsubtitle = "\n**"+title+"**"+"\n\n"
        return subsubtitle

class Article:

    def __init__(self, artnr, recid):
        self.artnr = str(artnr)
        self.recid = str(recid)


def decreet_get_chapters(documentID, chaptertype = False):
    url = decreeturl+str(documentID)
    r = requests.get(url)
    data = json.loads(r.content[1:len(r.content)-2])
    h = []
    for value in data:
        chapter = Chapter(value['RecID'], value['TitelParsed'], value['ChildCount'], chaptertype)
        h.append(chapter)
    return h


def decreet_get_articleids(parent):
    url = artikelurl + str(parent.id)
    r = requests.get(url)
    data = json.loads(r.content[1:len(r.content)-2])
    for value in data:
        parent.add_article(value["ArtNr"], value["RecID"])


def rec_get_things(hoofdstukken):
    for h in hoofdstukken:
        if (h.children == 0):
            decreet_get_articleids(h)
        else:
            h.sections= decreet_get_chapters(h.id)
            rec_get_things(h.sections)

def rec_print_things(hoofdstukken, chaptershort="", counter = 0):
    counter += 1
    codex_foldername = "vlaamse_codex"
    for h in hoofdstukken:
        if (h.mainchapter):
            counter = 0
            words=h.title.lower().split()
            chaptershort = words[0] + "_" + words[1]
            if not os.path.exists(codex_foldername):
                os.mkdir(codex_foldername)
            art_foldername = "./"+codex_foldername+"/"+chaptershort+'_articles'
            if not os.path.exists(art_foldername):
                os.mkdir(art_foldername)
            with open(codex_foldername + "/index.rst", 'a') as file:
                file.write(".. include:: " + chaptershort + ".rst\n")
        filename = codex_foldername + "/" + chaptershort + ".rst"
        with open(filename, 'a') as file:
            if (counter < 2):
                if (h.mainchapter):
                    file.write(h.get_headtitle())
                else:
                    file.write(h.get_subtitle())
            else:
                file.write(h.get_subsubtitle())

        if (h.children == 0):
                for article in h.articles:
                    articlenr = article.artnr.replace(".", "_")
                    articlenr = articlenr.replace("/","_")
                    words=articlenr.split("_")
                    articleloc = chaptershort + "_articles/" + articlenr + "article.rst"
                    with open(codex_foldername + "/" + articleloc, 'a') as file:
                        file.write(".. codex-art-text:: " + article.recid+"\n")
                    with open(filename, 'a') as file:
                        file.write(".. include:: " + articleloc+"\n")

        else:
            rec_print_things(h.sections, chaptershort, counter)

if  __name__ =='__main__':
    hoofdstukken = decreet_get_chapters("1062445", True)
    rec_get_things(hoofdstukken)
    rec_print_things(hoofdstukken)

