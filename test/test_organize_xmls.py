import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from spednfe.nfe_toolkit import NFeToolkit

class TestNFeToolkit(unittest.TestCase):

    def test_organize_xmls(self):

        # Caminho para o arquivo ZIP contendo os XMLs
        zip_path = 'notas.zip'

        dest_dir_fd = f'{os.getcwd()}\\output'

        test = NFeToolkit()
        test.extract_xmls(zip_path, dest_dir_fd)      

if __name__ == '__main__':
    unittest.main()