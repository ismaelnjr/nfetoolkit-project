import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit import NFeRepository, NFeHandler

class TestNFeRep(unittest.TestCase):
           
    def test_rep(self):
        
        xml1 = NFeHandler.nfe_from_path('nfe.xml')
        evt1 = NFeHandler.evento_canc_from_path('canc.xml')  
        evt2 = NFeHandler.evento_cce_from_path('cce.xml') 
        
        nfe_rep = NFeRepository()
        nfe_rep.store_nfe(xml1)
        nfe_rep.store_evt(evt1)
        nfe_rep.store_evt(evt2)
       
        nfe_rep.save('nfe_data.txt')
        self.assertIsNotNone(nfe_rep.content)
        
if __name__ == '__main__':
    unittest.main()