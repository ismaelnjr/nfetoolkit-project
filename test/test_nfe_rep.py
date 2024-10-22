import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit import NFeRepository

class TestNFeRep(unittest.TestCase):
           
    def test_rep(self):
        
        nfe_rep = NFeRepository()
        nfe_rep.store_all('.', verbose=True)
        nfe_rep.save('nfe_data.txt')
        self.assertIsNotNone(nfe_rep.content)
        
if __name__ == '__main__':
    unittest.main()