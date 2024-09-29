# NFE Toolkit

Biblioteca para manipulação de arquivos nfe (Nota Fiscal Eletrônica)

## Requisitos

- python
- nfelib
- spedpy

## Como instalar

    $ pip install nfetoolkit

## Objetivos do Projeto

A ideia é criar um toolkit para leitura/criação/organização de xmls relacionados ao projeto da Nota Fiscal Eletrônica

Casos de uso:

    1) Ler uma nfe a partir do xml e gerar o pdf correspondente:

    nfetoolkit = NFeTkt.XMLHandler()             
    nfeProc = nfetoolkit.nfe_from_path('nfe.xml')
    nfetoolkit.nfe_to_pdf(nfeProc, 'nfe.pdf')

    2) Extrair os xmls contidos em um arquivo Zip na pasta do diretório corrente e organizar em subpastas padrão: nfe, canc, inut e cce

    zip_path = 'notas.zip'
    dest_dir_fd = os.getcwd()

    test = NFeTkt.XMLOrganizer()
    test.extract_xmls(zip_path, dest_dir_fd)   

    3) Gravar conjunto de dados de notas fiscais em um único arquivo texto, separado por pipes (ArquivoDigital) 

    nfeToolkit = NFeTkt.NFeRepository()
    nfeToolkit.add_all_nfe('C:\\temp\\dest\\nfe')
    nfeToolkit.save('nfe_data.txt')
