import json
import xml.etree.ElementTree as ET

class XMLTagCorrector:
    def __init__(self, xml_content, config_file):
        # Inicializa com o conteúdo XML e o caminho para o arquivo de configuração
        self.tree = ET.ElementTree(ET.fromstring(xml_content))
        self.root = self.tree.getroot()
        
        # Carrega o arquivo de configuração JSON
        with open(config_file, 'r') as f:
            self.config = json.load(f)
    
    def apply_corrections(self):
        # Percorre as regras no arquivo de configuração
        for rule in self.config.get("rules", []):
            namespace = rule.get("namespace", {})
            path = rule.get("path")
            tag = rule.get("tag")
            condition = rule.get("condition", {})
            new_value = rule.get("new_value")
            
            # Aplica a correção com base na condição
            self._apply_rule(path, namespace, tag, condition, new_value)
    
    def _apply_rule(self, path, namespace, tag, condition: dict, new_value):
        change_tag = False
        for r_elem in self.root.findall(path, namespace):

            for condition_key in condition:
                if (elem_condition := r_elem.find(condition_key, namespace)) is not None:
                    elem_condition_value = elem_condition.text
                    change_tag = elem_condition_value == condition.get(condition_key)
                else:
                    change_tag = False

            if (elem_target := r_elem.find(tag, namespace)) is not None:
                if change_tag:
                    elem_target.text = new_value
                    
               
    
    def get_modified_xml(self):
        # Retorna o XML modificado como string
        return ET.tostring(self.root, encoding='unicode')

    def save_modified_xml(self, output_file):
        # Salva o XML modificado no arquivo especificado
        self.tree.write(output_file, encoding="utf-8", xml_declaration=True)
        
# Exemplo de uso

# XML de exemplo (substitua pelo XML completo fornecido)
xml_content = '''<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
<infNFe versao="4.00">
<det nItem="1">
<prod>
    <cProd>7898564046137</cProd>
    <NCM>85044010</NCM>
</prod>
<imposto>
    <ICMS>
        <ICMS70>
            <orig>1</orig>
        </ICMS70>
    </ICMS>
</imposto>
</det>
</infNFe>
</NFe>
</nfeProc>
'''

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
        ".ns:prod/ns:NCM": "85044010",
        ".ns:imposto/ns:ICMS//ns:orig": "1"
      },
      "new_value": "2"
    }
  ]
}
'''

# Salvar JSON de configuração para um arquivo temporário
config_file = 'config.json'
with open(config_file, 'w') as f:
    f.write(config_json)

# Instancia o corretor e aplica as correções
corrector = XMLTagCorrector(xml_content, config_file)
corrector.apply_corrections()

# Obtém o XML modificado
modified_xml = corrector.get_modified_xml()
print(modified_xml)

output_file = "teste.xml"
corrector.save_modified_xml(output_file)