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
        
    from nfetoolkit import NFeHandler

    nfeProc = NFeHandler.nfe_from_path('nfe.xml')
    NFeHandler.nfe_to_pdf(nfeProc, 'nfe.pdf')

    2) Extrair os xmls contidos em um arquivo Zip na pasta do diretório corrente e organizar em subpastas padrão: nfe, canc, inut e cce

    from nfetoolkit import nfetk


    zip_path = 'notas.zip'
    dest_dir_fd = os.getcwd()

    test = nfetk.XMLOrganizer()
    test.extract_xmls(zip_path, dest_dir_fd)   

    3) Gravar conjunto de dados de notas fiscais em um único arquivo texto, separado por pipes (ArquivoDigital) 

    from nfetoolkit import nfetk


    nfeToolkit = nfetk.NFeRepository()
    nfeToolkit.store_all('C:\\temp\\dest\\nfe', verbose=True)
    nfeToolkit.save('nfe_data.txt')
