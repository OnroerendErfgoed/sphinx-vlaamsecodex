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

    extensions = ['sphinxcontrib.sphinx-vlaamsecodex', ]




To make it possible to collapse articles extend the css of the theme with the following css:

.. code-block:: css

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

It is also possible to extend the css for a document by adding a page.html file in a _templates folder with the following code:

.. code-block:: none

    {% extends "!page.html" %}
    {% set css_files = css_files + ["_static/customstyle.css"] %}