import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from spednfe.nfe_toolkit import NFeToolkit 

class TestReadNFe(unittest.TestCase):
           
    def test_danfe_nfe(self):
        


        nfetoolkit = NFeToolkit()
        
        nfe_filename = 'nfe.xml'
        pdf_filename = 'nfe.pdf'
        
        nfetoolkit.nfe_to_pdf(nfe_filename, pdf_filename)

if __name__ == '__main__':
    unittest.main()


