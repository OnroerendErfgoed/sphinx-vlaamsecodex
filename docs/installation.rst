============
Installation
============

The sphinx vlaamse codex extention is availlable on github: https://github.com/OnroerendErfgoed/sphinx-vlaamsecodex .

Clone the repository and install the package in the virtual environment.

.. code-block:: bash

    $ cd <git repo>
    $ venv/bin/python setup.py install

Create a sphinx project in the same environment and include the extention in the **conf.py** file.

.. code-block:: bash

    $ cd <docs>
    $ venv/bin/pip install sphinx
    $ venv/bin/sphinx-quickstart

.. code-block:: python

    extensions = ['sphinx-oe.sphinx-vlaamsecodex', ]