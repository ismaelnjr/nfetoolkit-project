import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from core.fix import NFeFix

class TestFixNFe(unittest.TestCase):
           
    def test_fix_nfe(self):
        
        # Arquivo JSON de configuração
      config_json = '''
  {
    "rules": [
      {
        "namespace": { 
          "ns": "http://www.portalfiscal.inf.br/nfe" 
        },
        "path": "./ns:NFe/ns:infNFe/ns:det",
        "tag": ".ns:imposto/ns:ICMS//ns:orig",
        "condition": {
          ".ns:prod/ns:NCM": "85142011",
          ".ns:imposto/ns:ICMS//ns:orig": "0"
        },
        "new_value": "2"
      }
    ]
  }
  '''
      config_file = 'config.json'
      with open(config_file, 'w') as file:
        file.write(config_json)
      xml = 'nfe.xml'
      with open(xml, 'r') as file:
        xml_content = file.read()

      # Instancia o corretor e aplica as correções
      fix = NFeFix(config_file)
      modified_xml = fix.apply(xml_content)

      # Obtém o XML modificado

      print(modified_xml)
      with open('modified.xml', 'w') as f:
          f.write(modified_xml)
    
if __name__ == '__main__':
    unittest.main()

