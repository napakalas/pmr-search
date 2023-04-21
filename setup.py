from setuptools import setup

setup(

    name='pmr-search',
    version='0.0.1',
    description='Searching models in the PMR using UBERON and ILX terms',
    url='http://github.com/napakalas/pmr-sparc-sparql',
    author='Yuda Munarko',
    author_email='yuda.munarko@gmail.com',
    license='Apache 2.0',
    packages=['pmr_search'],
    zip_safe=False,
    install_requires=[
        'torch>=1.13.0',
        'sentence-transformers>=2.2.2',
        'requests>=2.28.0',
        'SPARQLWrapper>=2.0.0',
    ],
    
      
)
#===============================================================================