from docutils import nodes, utils
import urllib

codex_vlaanderen_url = 'http://codex.vlaanderen.be'
codex_vlaanderen_doc_url = codex_vlaanderen_url + '/Zoeken/Document.aspx?DID='

def codexdoc_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
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
    node = make_link_node(rawtext, app, 'codex-doc', str(doc_num), label, options)
    return [node], []

def make_link_node(rawtext, app, type, slug, label, options):
    """Create a link to a Document in the Vlaamse Codex.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param type: Link type (issue, changeset, etc.)
    :param slug: ID of the thing to link to
    :param label: Custom display label if given <label>
    :param options: Options dictionary passed to role func.
    """
    try:
        base = app.config.codex_vlaanderen_doc_url
        if not base:
            raise AttributeError
    except AttributeError:
        raise ValueError('codex_vlaanderen_doc_url configuration value is not set')
    ref = codex_vlaanderen_doc_url + slug
    display = label if label is not None else ref
    node = nodes.reference(rawtext, utils.unescape(display), refuri=ref, **options)
    return node

def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """

    app.add_role('codex-doc', codexdoc_role)
    app.add_config_value('codex_vlaanderen_doc_url', codex_vlaanderen_doc_url, 'env')
    return