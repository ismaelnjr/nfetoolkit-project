import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit.nfetkt import NFeTkt

class TestNFeRep(unittest.TestCase):
           
    def test_rep(self):
        
        nfeToolkit = NFeTkt.NFeRepository()
        nfeToolkit.add_all_nfe('C:\\temp\\dest\\nfe')
        nfeToolkit.save('nfe_data.txt')

if __name__ == '__main__':
    unittest.main()