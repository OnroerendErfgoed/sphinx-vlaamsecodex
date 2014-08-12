=====
Usage
=====

Sphinx role codex-doc
=====================

Sphinx role to create a link to a document on its title given the its id:

.. code-block:: python

    :codex-doc:`1001628`

*becomes:*
:codex-doc:`1001628`

Possibility to create custom label:

.. code-block:: python

    :codex-doc:`1001628 <Dit is document 1001628>`

*becomes:*
:codex-doc:`1001628 <Dit is document 1001628>`


Sphinx role codex-art
=====================

Sphinx role to create a link to an article on its number given its id:

.. code-block:: python

    :codex-art:`1168906`

*becomes:*
:codex-art:`1168906`

Possibility to create custom label:

.. code-block:: python

    :codex-art:`1168906 <Dit is artike 1168906>`

*becomes:*
:codex-art:`1168906 <Dit is artike 1168906>`

Sphinx directive codex-art-text
===============================

Sphinx directive to show the text of an article given the article id

.. code-block:: python

    .. codex-art-text:: 1168906

*becomes:*

.. codex-art-text:: 1168906


Possibility to show the article text collapsed:

.. note::

    To make it possible to collapse articles extend the css of the theme with the following css:

        .toggle-box {
          display: none;
        }

        .collapsable .toggle-box + label {
          cursor: pointer;
          display: block;
          font-weight: bold;
          line-height: 21px;
          margin-bottom: 5px;
        }

        .collapsable .toggle-box + label + dd{
          display: none;
          margin-bottom: 10px;
        }

        .collapsable .toggle-box:checked + label + dd {
          display: block;
        }

        .collapsable .toggle-box + label:before {
          background-color: #4F5150;
          -webkit-border-radius: 10px;
          -moz-border-radius: 10px;
          border-radius: 10px;
          color: #FFFFFF;
          content: "+";
          display: block;
          float: left;
          font-weight: bold;
          height: 20px;
          line-height: 20px;
          margin-right: 5px;
          margin-top:5px;
          text-align: center;
          width: 20px;
        }

        .collapsable .toggle-box:checked + label:before {
          content: "\2212";
        }

    It is also possible to extend the css for a document by adding a layout.html file in a _templates folder with the following code:

        {% extends "!layout.html" %}
        {% set css_files = css_files + ["_static/customstyle.css"] %}

.. code-block:: python

    .. codex-art-text:: 1168906
        :collapse:

*becomes:*

.. codex-art-text:: 1168906
    :collapse:

An other example:

.. code-block:: python

    .. codex-art-text:: 1168908


*becomes:*

.. codex-art-text:: 1168908


