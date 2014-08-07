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

.. code-block:: python

    .. codex-art-text:: 1168908

*becomes:*

.. codex-art-text:: 1168908

Possibility to show the article text collapsed:

.. code-block:: python

    .. codex-art-text:: 1168906
        :collapse:

*becomes:*

.. codex-art-text:: 1168906
    :collapse: