import os
import sys

from spednfe.nfetoolkit import NFeToolkit

# Caminho para o arquivo ZIP contendo os XMLs
src_dir_fd = 'C:\\temp\\src'
dest_dir_fd = 'C:\\temp\\dest'

test = NFeToolkit()
test.organize_xmls(src_dir_fd, dest_dir_fd)
