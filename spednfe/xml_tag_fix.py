import json
import xml.etree.ElementTree as ET

class XMLTagFix:
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
        change_tag = True
        for r_elem in self.root.findall(path, namespace):

            for condition_key in condition:
                if (elem_condition := r_elem.find(condition_key, namespace)) is not None:
                    elem_condition_value = elem_condition.text
                    change_tag = (elem_condition_value == condition.get(condition_key)) and change_tag
                else:
                    change_tag = False

            if (elem_target := r_elem.find(tag, namespace)) is not None:
                if change_tag:
                    elem_target.text = new_value
    
    def get_modified_xml(self):
        # Retorna o XML modificado como string
        return ET.tostring(self.root, encoding='unicode')



  
