# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


from setuptools import setup
from setuptools import find_packages

from nfetoolkit import __version__
    
def parse_requirements(filename):
    with open(filename, encoding='utf-16') as f:
        return f.read().splitlines()

setup(name='nfetoolkit',
    version=__version__,
    license='MIT',
    author='Ismael Nascimento',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author_email='ismaelnjr@icloud.com.br',
    keywords='sped fiscal nfe receita federal',
    description=u'Toolkit para manipulação de notas fiscais eletrônicas',
    url='https://github.com/ismaelnjr/nfetoolkit-project.git',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


