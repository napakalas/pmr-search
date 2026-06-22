==========
pmr_search
==========

This script is used to search for models in PMR using ontology terms in UBERON and ILX, or free text. Search can be SPARQL based or embedding based.

SPARQL-based execution is quite slow because it has to do two queries to SciCrunch and PMR endpoints. However, it is useful to know whether a term has been used to annotate models in PMR or not.

Embedding-based execution is much faster and lends itself well to explorative search. Each search will display results with the score value. The result is a dictionary consisting of exposure lists, workspaces, and CellML files.

Installation
------------
To install `pmr-search`, you can use `uv` (recommended) or `pip`:

.. code-block:: bash

    uv add git+https://github.com/napakalas/pmr-search.git

Or with pip:

.. code-block:: bash

    pip install git+https://github.com/napakalas/pmr-search.git

Usage
-----
CLI
~~~

Ontology term query:

.. code-block:: bash

   pmr_search -o UBERON:0001629 -t 0.84 -s 5

Free text query:

.. code-block:: bash

   pmr_search -o "basolateral plasma membrane" -t 0.84 -s 5

Free text query with your example terms:

.. code-block:: bash

   pmr_search -o "Apical and basolateral epithelial" -t 0.84 -s 5
   pmr_search -o "Aquaporin-1 (AQP1, Mouse)" -t 0.84 -s 5

Batch query from JSON (for FC annotations):

.. code-block:: bash

   pmr_search -f annotation.json -d new/annotation.json -t 0.84 -s 5

Example `annotation.json` input:

.. code-block:: json

    {
       "GroupA": [
          {
             "Model": "UBERON:0001629",
             "Organ": "Carotid body"
          },
          {
             "Models": "Aquaporin-1 (AQP1, Mouse)",
             "Organ/System": "Kidney"
          }
       ]
    }


Options
-------
- `-o {ontology term}` : search with ontology term(s).
- `-t {threshold}` : set threshold for similarity score (default: 0.8).
- `-s {size}` : set maximum number of models to retrieve (default: 5).
- `-f {file}` : search with a json file containing anatomical terms.
- `-d {destination}` : file destination to save the results.

Python API
~~~~~~~~~~

Import:

.. code-block:: python

   from pmr_search import ModelSearch, EMBEDDING, SPARQL

1. Embedding search with ontology term:

.. code-block:: python

   ms = ModelSearch()
   results = ms.search("UBERON:0001629", client_type=EMBEDDING)
   print(results)
   ms.close()

2. Embedding search with free text:

.. code-block:: python

   ms = ModelSearch()
   results = ms.search("basolateral plasma membrane", topk=5, min_sim=0.84)
   print(results)
   ms.close()

3. Embedding search with your text examples and context:

.. code-block:: python

   ms = ModelSearch()
   results_1 = ms.search(
       "Apical and basolateral epithelial",
       context=["Kidney", "Human"],
       topk=5,
       min_sim=0.84,
       c_weight=0.6,
       client_type=EMBEDDING,
   )
   results_2 = ms.search(
       "Aquaporin-1 (AQP1, Mouse)",
       context=["Kidney", "Mouse"],
       topk=5,
       min_sim=0.84,
       c_weight=0.6,
       client_type=EMBEDDING,
   )
   print(results_1)
   print(results_2)
   ms.close()

4. SPARQL search (annotation lookup):

.. code-block:: python

   ms = ModelSearch()
   results = ms.search("UBERON:0002173", client_type=SPARQL)
   print(results)
   ms.close()

Notes:

- SPARQL search is network-bound and slower.
- Embedding search is local and generally much faster.

