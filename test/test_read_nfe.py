import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit import nfetk 

class TestReadNFe(unittest.TestCase):
           
    def test_read_nfe(self):
        
        nfeToolkit = nfetk.XMLHandler()
        nfeProc = nfeToolkit.nfe_from_path("nfe.xml")
        print(f"NFe Id: {nfeProc.NFe.infNFe.Id}")

        nfecanc = nfeToolkit.evento_canc_from_path("canc.xml")
        print(f"Motivo cancelamento: {nfecanc.evento.infEvento.detEvento.xJust}")

        cce = nfeToolkit.evento_cce_from_path("cce.xml")
        print(f"Correção CCe: {cce.evento.infEvento.detEvento.xCorrecao}")

if __name__ == '__main__':
    unittest.main()


