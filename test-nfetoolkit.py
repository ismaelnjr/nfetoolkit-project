import os
import sys

from spednfe.nfetoolkit import NFeToolkit

# Caminho para o arquivo ZIP contendo os XMLs
zip_path = 'etc/notas.zip'

dest_dir_fd = f'{os.getcwd()}\\output'

test = NFeToolkit()
test.extract_xmls(zip_path, dest_dir_fd)
