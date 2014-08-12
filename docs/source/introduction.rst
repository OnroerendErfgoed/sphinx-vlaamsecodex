============
Introduction
============

Sphinx extension to integrate http://codex.vlaanderen.be in a document.

The extension include:

* A role to create a link to a document on its title given the id
* A role to create a link to an article on its number given the id
* A directive to show the text of an article given the id

It is possible to give a label to sphinx roles. In that case the link will be created on the given label in stead of the title or number.

The option 'collapsed' is availlable on the the sphinx directive.

Tested with sphinx_rtd_theme (https://github.com/snide/sphinx_rtd_theme/ ):

.. code-block:: bash

    $ make html
    $ make latexpdf