import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit import XMLHandler

class TestReadNFe(unittest.TestCase):
           
    def test_danfe_nfe(self):        
        
        nfeProc = XMLHandler.nfe_from_path('nfe.xml')
        XMLHandler.nfe_to_pdf(nfeProc, 'nfe.pdf')

if __name__ == '__main__':
    unittest.main()


