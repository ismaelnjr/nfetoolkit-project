import zipfile
import random
import string
import shutil
import os

from pathlib import Path
from .nfe_handler import NFeHandler

class NFeOrganizer:

    def organize_xmls(self, source_dir_fd: str, dest_dir_fd: str, folders_map=None):
        """oraniza os arquivos xml contidos em uma pasta e os move para subpastas de 
        um diretório fornecido pelo usuário (pastas padrão: nfe, canc, cce e inut)""" 
        if folders_map is None:
            folders_map = {
                'nfe_type': 'nfe',
                'canc_type': 'canc',
                'cce_type': 'cce',
                'inut_type': 'inut',
            }
        NFeOrganizer.create_dest_folders(path=dest_dir_fd, dest_fds_map=folders_map)

        for root, dirs, files in os.walk(source_dir_fd):
            for file in files:
                file_path = Path(root) / file
                if file.endswith('.zip'):
                    self.extract_xmls(file_path, dest_dir_fd)
                elif file.endswith('.xml'):
                    try:
                        xml_type = NFeHandler.xml_type(file_path)
                        if xml_type == 'unknown_type':
                            print(f"Arquivo {file} não é um arquivo xml conhecido")
                        else:
                            file_path.rename(Path(dest_dir_fd) / folders_map[xml_type] / file)
                    except Exception as e:
                        print(f"Erro ao processar {file}: {e}")
                        
    @staticmethod
    def find_all(from_path, xml_types: list = None):
        """Finds and returns a list of NFE XML files from a specified directory.

        This static method traverses the directory tree starting from `from_path`, 
        searching for files with an '.xml' extension. It identifies files of types 
        'nfe', 'canc', 'cce', and 'inut', collecting their paths in a list which 
        is returned at the end.

        Args:
            from_path (str): The root directory path to start the search from.
            xml_types (list, optional): A list of XML types to filter the results. 
                Defaults to ['nfe_type', 'canc_type', 'cce_type', 'inut_type'].

        Returns:
            list: A list of paths to the NFE XML files found in the directory.
        """

        nfe_list = []
        xml_types = ['nfe_type', 'canc_type', 'cce_type', 'inut_type']
        for file_path in Path(from_path).rglob('*.xml'):
            xml_type = NFeHandler.xml_type(file_path)
            if xml_type in xml_types:
                nfe_list.append(file_path) 
        return nfe_list

    def extract_xmls(self, zipFile: str, dest_dir_fd: str):
        """extrai os arquivos xml de um arquivo zip e os organiza em um diretório fornecido pelo usuário"""
        
        temp_folder = Path.cwd() / ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        with zipfile.ZipFile(zipFile, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)

        self.organize_xmls(source_dir_fd=temp_folder, dest_dir_fd=dest_dir_fd)
        shutil.rmtree(temp_folder)

    
    @staticmethod                
    def create_dest_folders(path: str, dest_fds_map: dict = None):
        """Cria as pastas necessárias para armazenar os arquivos XML."""    
        if not os.path.exists(path):
            os.makedirs(path)

        for key in dest_fds_map:
            if not os.path.exists(f"{path}\\{dest_fds_map[key]}"):
                os.makedirs(f"{path}\\{dest_fds_map[key]}")