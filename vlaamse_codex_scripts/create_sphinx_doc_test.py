import requests, json
from collections import OrderedDict 

codex_vlaanderen_url = 'http://codexws.vlaanderen.be'
decreeturl = codex_vlaanderen_url + "/Hoofdstuk/ListByParentId/"
artikelurl = codex_vlaanderen_url + "/Artikel/ListByHoofdstukId/"



class Chapter:
    def __init__(self, chapterid, title, children, chaptertype):
        self.id = chapterid
        self.children = children
        self.title = title
        self.sections = []
        self.articles = []
        self.mainchapter = chaptertype

    def add_section(self, recid, title, children):
        self.section.append(Afdeling(recid, title, children))

    def add_article(self, artnr, recid):
        self.articles.append(Article(artnr, recid))

class Article:

    def __init__(self, artnr, recid):
        self.artnr = artnr
        self.recid = recid


def decreet_get_chapters(documentID, chaptertype = False):
    url = decreeturl+str(documentID)
    r = requests.get(url)
    data = json.loads(r.content[1:len(r.content)-2])
    h = []
    for value in data:
        chapter = Chapter(value['RecID'], value['Titel'], value['ChildCount'], chaptertype)
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

def rec_print_things(hoofdstukken):
    for h in hoofdstukken:
        if (h.mainchapter):
            words=h.title.split()
            foldername = words[0]+'_'+words[1]+'_articles'
            print foldername
        if (h.children == 0):
            for article in h.articles:
                print ".. include:: ../" + str(article.artnr).replace(".", "_") + ".rst"
        else:
            rec_print_things(h.sections)

if  __name__ =='__main__':
    hoofdstukken = decreet_get_chapters("1062445", True)
    rec_get_things(hoofdstukken)
    rec_print_things(hoofdstukken)

