# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


from setuptools import setup
from setuptools import find_packages

from nfetoolkit import __version__

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='nfetoolkit',
    version=__version__,
    license='MIT License',
    author='Ismael Nascimento',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ismaelnjr@icloud.com.br',
    keywords='sped fiscal nfe receita federal',
    description=u'Toolkit para manipulação de notas fiscais eletrônicas',
    url='https://github.com/ismaelnjr/nfetoolkit-project.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['xsdata', 'nfelib', 'spedpy', 'BrazilFiscalReport', 'erpbrasil', 'six', 'tdqm'],
    classifiers=
        ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
   
    )


