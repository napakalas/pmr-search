==========
pmr_search
==========

This script is used to search for models in PMR using ontology terms in UBERON and ILX, or free text. Search can be SPARQL based or embedding based.

SPARQL-based execution is quite slow because it has to do two queries to SciCrunch and PMR endpoints. However, it is useful to know whether a term has been used to annotate models in PMR or not.

Embedding-based execution is much faster and lends itself well to explorative search. Each search will display results with the score value. The result is a dictionary consisting of exposure lists, workspaces, and CellML files.

Installation
------------
To install `pmr-search`, you can use pip:

.. code-block:: 
    
    pip install git+https://github.com/napakalas/pmr-search.git

Usage
-----
.. code-block::

   pmr_search -o {ontology term} -t {threshold} -s {size}
   pmr_search -s {size} -o {query}
   pmr_search -s {size} -f {file} -d {destination} -t {threshold}

to add PMR's models to an annotation.json for FC:

.. code-block::
   
   # example
   pmr_search -f annotation.json -d new/annotation.json -t 0.84
    

Options
-------
- `-o {ontology term}` : search with ontology term(s).
- `-t {threshold}` : set threshold for similarity score (default: 0.8).
- `-s {size}` : set maximum number of models to retrieve (default: 5).
- `-f {file}` : search with a json file containing anatomical terms.
- `-d {destination}` : file destination to save the results.

To use `pmr-search` in your Python code, you can install it using pip and then import it in your Python script:

.. code-block:: python

   from pmr_search import ModelSearch

Then you can create a `ModelSearch` object and call `search` function with the appropriate arguments to search for models in PMR:

.. code-block:: python

   ms = ModelSearch() 
   results = ms.search('UBERON:0001629')
   print(result)

.. code-block:: python

   from pmr_search import EMBEDDING
   results = ms.search('UBERON:0002173', context=['Lungs'], topk=5, min_sim=0.85, c_weight=0.5, client_type=EMBEDDING)

   from pmr_search import SPARQL
   results = ms.search('UBERON:0002173', client_type=SPARQL)

