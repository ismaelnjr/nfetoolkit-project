import xml.etree.ElementTree as ET
import json


class NFeFix:
    '''
    The NFeFix class is used to correct NFe XML files based on a configuration file.
    The configuration file is a JSON file that contains a list of rules to be applied to the XML.
    '''

    def __init__(self, config_file: str):
        # Inicializa com o conteúdo XML e o caminho para o arquivo de configuração
        # Carrega o arquivo de configuração JSON
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def apply(self, xml_content):
        
        ET.register_namespace('', 'http://www.portalfiscal.inf.br/nfe')
        self.root = ET.ElementTree(ET.fromstring(xml_content)).getroot()
        # Percorre as regras no arquivo de configuração
        for rule in self.config.get("rules", []):
            namespace = rule.get("namespace", {})
            path = rule.get("path")
            tag = rule.get("tag")
            condition = rule.get("condition", {})
            new_value = rule.get("new_value")

            # Aplica a correção com base na condição
            self.__apply_rule(path, namespace, tag, condition, new_value)                
        
        return ET.tostring(self.root, encoding='unicode', xml_declaration=False)

    def __apply_rule(self, path, namespace, tag, condition: dict, new_value):
        for r_elem in self.root.findall(path, namespace):
            change_tag = all(
                (elem_condition := r_elem.find(condition_key, namespace)) is not None and
                elem_condition.text == condition.get(condition_key)
                for condition_key in condition
            )

            if change_tag and (elem_target := r_elem.find(tag, namespace)) is not None:
                elem_target.text = new_value
                    
