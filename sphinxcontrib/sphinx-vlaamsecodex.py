from docutils import nodes, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes
import requests, json
import uuid

codex_vlaanderen_url = 'http://codex.vlaanderen.be'
codexws_vlaanderen_url = 'http://codexws.vlaanderen.be/'
codex_vlaanderen_doc_url = codex_vlaanderen_url + '/Zoeken/Document.aspx?DID='
codex_vlaanderen_docid = codexws_vlaanderen_url + 'Document/GetByID/'
codex_vlaanderen_art_posturl = '&param=inhoud&AID='
codex_vlaanderen_artid = codexws_vlaanderen_url + 'Artikel/GetByID/'
codex_vlaanderen_arthisid = codexws_vlaanderen_url + 'ArtikelHistoriek/GetByID/'

def codex_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """Link to a Document in the Vlaamse Codex.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    try:
        inputtext = text.split('<')
        doc_num = int(text.split('<')[0])
        label = None
        if len(inputtext) >1:
            label = inputtext[1][0:len(inputtext[1])-1]
        if doc_num <= 0:
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(
            'Document number must be a number greater than or equal to 1; '
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    app = inliner.document.settings.env.app
    node = make_link_node(rawtext, app, role, str(doc_num), label, options)
    return [node], []

def make_link_node(rawtext, app, type, id, label, options):
    """Create a link to a Document in the Vlaamse Codex.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param type: Link type (issue, changeset, etc.)
    :param id: ID of the thing to link to
    :param label: Custom display label if given <label>
    :param options: Options dictionary passed to role func.
    """
    try:
        base = app.config.codex_vlaanderen_doc_url
        if not base:
            raise AttributeError
    except AttributeError:
        raise ValueError('codex_vlaanderen_doc_url configuration value is not set')
    ref = codex_vlaanderen_url
    display = ""
    if 'doc' in type:
        ref = codex_vlaanderen_doc_url + id
        display = label if label is not None else get_title_doc(id, default=ref)
    if 'art' in type:
        info_artikel = get_info_artikel(id)
        ref = info_artikel['ref']
        display = label if label is not None else get_title_art(info_artikel['ArtNr'], default=ref)
    node = nodes.reference(rawtext, utils.unescape(display), refuri=ref, **options)
    return node

def get_info_artikel(AID):
    """Returns a list of information about the artikel in the Vlaamse Codex:
    - ArtNr
    - Link

    :param AID: ID of the artikel to link to
    """
    url = codex_vlaanderen_artid + str(AID)
    r = requests.get(url)
    artikel_json = json.loads(r.content[1:len(r.content)-2].decode())
    return {
        'ArtNr': artikel_json['ArtNr'],
        'ref': codex_vlaanderen_doc_url + str(artikel_json['DocumentID']) + codex_vlaanderen_art_posturl + str(AID)
    }

def get_title_doc(DID, default=""):
    """Returns the titel of the document in the Vlaamse Codex.

    :param DID: ID of the document
    :param default: value if no title is returned
    """
    url = codex_vlaanderen_docid + str(DID)
    r = requests.get(url)
    doc_json = json.loads(r.content[1:len(r.content)-2].decode())
    try:
        return "%s %s" %(doc_json['DocumentType'], doc_json['Naam'])
    except:
        return default


def get_title_art(ArtNr,  default=""):
    """Returns the titel of the art in the Vlaamse Codex.

    :param ArtNr: number of the artikel
    :param default: value if no title is returned
    """
    try:
        return "Artikel: %s" %ArtNr
    except:
        return default

def get_text_art(AID):
    """Returns the tekst of the artikel in the Vlaamse Codex.

    :param AID: ID of the artikel
    """
    url_art = codex_vlaanderen_artid + str(AID)
    r = requests.get(url_art)
    artikel_json = json.loads(r.content[1:len(r.content)-2].decode())
    try:
        RecID = artikel_json['HistorischeVersies'][len(artikel_json['HistorischeVersies'])-1]['RecID']
        url_arthis = codex_vlaanderen_arthisid + str(RecID)
        r = requests.get(url_arthis)
        return json.loads(r.content[1:len(r.content)-2].decode())['Tekst'].replace('<BR>', '|BR|')
    except:
        return ""

class ArtikelTextDirective(Directive):
    """Directive to show the tekst of the artikel in the Vlaamse Codex.
       Option to collapse (article text is hidden)
    """
    required_arguments = 1
    optional_arguments = 0
    option_spec = dict(collapse=directives.flag)

    def run(self):
        AID = directives.uri(self.arguments[0])
        collapseclass= AID + uuid.uuid4().hex
        set_classes(self.options)
        content = get_text_art(AID)
        art_info = get_info_artikel(AID)
        artnr= art_info['ArtNr']
        html_class = "collapsable art" if 'collapse' in self.options else "art"
        html_input = '<dl class="%s"><input class="toggle-box" id="%s" type="checkbox"><label for="%s"> <dt class="article"><tt class="descname article"> Artikel %s</tt></dt></label><dd class="article-content"> %s <dd></dl>' \
                     % (html_class, collapseclass, collapseclass, artnr, content.replace('|BR|', '<BR><BR>'))
        latex_line = r'\rule{\textwidth}{0.6pt}'
        latex_input = r'\newline %s \textbf{Artikel:} %s %s'  \
                      %(latex_line, content.replace('|BR|', r'\newline \newline '), latex_line)
        node_html = nodes.raw('', html_input, format='html')
        node_latex = nodes.raw('', latex_input, format='latex')
        return [node_latex, node_html]

def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """

    app.add_role('codex-doc', codex_role)
    app.add_role('codex-art', codex_role)
    app.add_directive("codex-art-text", ArtikelTextDirective)
    app.add_config_value('codex_vlaanderen_url', codex_vlaanderen_url, 'env')
    app.add_config_value('codexws_vlaanderen_url', codexws_vlaanderen_url, 'env')
    app.add_config_value('codex_vlaanderen_doc_url', codex_vlaanderen_doc_url, 'env')
    app.add_config_value('codex_vlaanderen_docid', codex_vlaanderen_docid, 'env')
    app.add_config_value('codex_vlaanderen_art_posturl', codex_vlaanderen_art_posturl, 'env')
    app.add_config_value('codex_vlaanderen_artid', codex_vlaanderen_artid, 'env')
    app.add_config_value('codex_vlaanderen_arthisid', codex_vlaanderen_arthisid, 'env')
    return