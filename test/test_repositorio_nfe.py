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
           
    def test_repositorio(self):
        
        nfeToolkit = NFeToolkit()
        nfeToolkit.store_all_nfe_from_dir('C:\\temp\\dest\\nfe')
        nfeToolkit.save_repository_to('nfe_data.txt')

if __name__ == '__main__':
    unittest.main()