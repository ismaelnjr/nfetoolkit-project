from nfetoolkit.organizer import NFeOrganizer
from nfetoolkit.repository import NFeRepository
from nfetoolkit.handler import NFeHandler
from tqdm import tqdm

xml_dir = "."

nfe_organizer = NFeOrganizer()
nfe_repository = NFeRepository()

xml_list = nfe_organizer.find_all(xml_dir)

for xml_file in tqdm(xml_list, desc="Exportando NF-es", unit="xml"): #xml_list:   
    xml = NFeHandler.nfe_from_path(xml_file) 
    nfe_repository.store_nfe(xml)
    
with open("nfe_data.txt", "w") as stream:
    nfe_repository.write_to(stream)