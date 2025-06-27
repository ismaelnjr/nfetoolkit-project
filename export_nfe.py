import argparse
from tqdm import tqdm
from nfetoolkit.organizer import NFeOrganizer
from nfetoolkit.repository import NFeRepository
from nfetoolkit.handler import NFeHandler

def main(xml_dir: str, output_file: str = "nfe_data.txt"):
    nfe_organizer = NFeOrganizer()
    nfe_repository = NFeRepository()

    xml_list = nfe_organizer.find_all(xml_dir)

    for xml_file in tqdm(xml_list, desc="Exportando NF-es", unit="xml"):
        xml = NFeHandler.nfe_from_path(xml_file)
        nfe_repository.store_nfe(xml)

    with open(output_file, "w") as stream:
        nfe_repository.write_to(stream)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exportador de NF-es a partir de uma pasta de XMLs.")
    parser.add_argument("xml_dir", help="Caminho da pasta com os arquivos XML das NF-e.")
    parser.add_argument("-o", "--output", help="Nome do arquivo de saída (default: nfe_data.txt)", default="nfe_data.txt")

    args = parser.parse_args()
    main(args.xml_dir, args.output)

    print(f"[OK] Dados exportados para: {args.output}")