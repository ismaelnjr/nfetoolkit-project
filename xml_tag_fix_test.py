from spednfe.xml_tag_fix import XMLTagFix

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

config_file = 'config.json'
#with open(config_file, 'w') as f:
#    f.write(config_json)

xml = 'etc\\35240523004906000180550010001354511002078970.xml'
with open(xml, 'r') as file:
    xml_content = file.read()

    # Instancia o corretor e aplica as correções
    corrector = XMLTagFix(xml_content, config_file)
    corrector.apply_corrections()

    # Obtém o XML modificado
    modified_xml = corrector.get_modified_xml()
    print(modified_xml)
    with open('modified.xml', 'w') as f:
        f.write(modified_xml)
    