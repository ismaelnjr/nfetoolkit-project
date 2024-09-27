import contextlib
import zipfile
import os
import random
import string
import shutil
import xml.etree.ElementTree as ET
import warnings
import os
import xsdata
import inspect
import tqdm
import json

from datetime import date
from pathlib import Path

from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from nfelib.nfe_evento_cancel.bindings.v1_0 import ProcEventoNfe as CancNFe
from nfelib.nfe_evento_cce.bindings.v1_0.proc_cce_nfe_v1_00 import ProcEventoNfe as CCe
from xsdata.formats.dataclass.parsers import XmlParser
from lxml import etree
from typing import Optional, List, Any

from nfetoolkit.spednfe.arquivos import ArquivoDigital
from nfetoolkit.spednfe.registros import RegistroN100, RegistroN140, RegistroN141, RegistroN170, RegistroZ100


class NFeTkt(object):
    
    
    class NFeRepository:
        
        _rep: ArquivoDigital    
        
        def __init__(self, rep_filename: str = None) -> None:
            self._rep = ArquivoDigital()
            if rep_filename:
                self._rep.readfile(rep_filename)
            else:
                self._rep = ArquivoDigital()

        @property
        def content(self):
            return self._rep      

        def add_all_nfe(self, source_dir: str):
            
            xml_list = self.__list_xml(source_dir)
            for xml_file in tqdm.tqdm(xml_list, total=len(xml_list), desc="processando xmls"):            
                xml_type = NFeTkt.XMLOrganizer.xml_type(xml_file)
                
                if xml_type == 'nfe_type':
                    obj = NFeTkt.XMLHandler.nfe_from_path(xml_file)
                    self.store_nfe(obj)
                elif xml_type == 'canc_type':
                    obj = NFeTkt.XMLHandler.evento_canc_from_path(xml_file)
                    self.store_evt(obj)
                elif xml_type == 'cce_type':      
                    obj = NFeTkt.XMLHandler.evento_cce_from_path(xml_file)
                    self.store_evt(obj)         
                    
        def store_evt(self, evt: Any):
            
            blocoZ = self._rep.blocoZ
            z100 = RegistroZ100()
            z100.CNPJ = self.__format_CNPJ(evt.retEvento.infEvento.CNPJDest)
            z100.CPF = self.__format_CPF(evt.retEvento.infEvento.CPFDest)
            z100.CHAVE_NFE = evt.retEvento.infEvento.chNFe
            z100.DATA_EVENTO = evt.retEvento.infEvento.dhRegEvento
            z100.TIPO_EVENTO = evt.retEvento.infEvento.tpEvento
            z100.MOTIVO = evt.retEvento.infEvento.xMotivo
            z100.PROTOCOLO = evt.retEvento.infEvento.nProt
            z100.DESC_EVENTO = evt.retEvento.infEvento.xEvento
            blocoZ.add(z100)            
        
        def store_nfe(self, nfeProc: NfeProc):  # sourcery skip: extract-method

            blocoN = self._rep.blocoN
            # processa cabeçalho da nota fiscal
            n100 = RegistroN100()
            n100.CNPJ_EMIT = nfeProc.NFe.infNFe.emit.CNPJ
            n100.NOME_EMIT = nfeProc.NFe.infNFe.emit.xNome
            n100.NUM_NFE = nfeProc.NFe.infNFe.ide.nNF
            n100.SERIE = nfeProc.NFe.infNFe.ide.serie
            n100.DT_EMISSAO = self.__checkDate(nfeProc.NFe.infNFe.ide.dhEmi)
            n100.TIPO_NFE = {0: "ENTRADA", 1: "SAIDA"}.get(nfeProc.NFe.infNFe.ide.tpNF, "UNKNOWN")
            n100.MES_ANO = date.strftime(n100.DT_EMISSAO, '%m_%Y')
            n100.CHAVE_NFE = nfeProc.protNFe.infProt.chNFe
            n100.CNPJ_DEST = self.__format_CNPJ(nfeProc.NFe.infNFe.emit.CNPJ)
            n100.CPF_DEST = self.__format_CPF(nfeProc.NFe.infNFe.emit.CPF)
            n100.NOME_DEST = nfeProc.NFe.infNFe.dest.xNome
            n100.UF = nfeProc.NFe.infNFe.dest.enderDest.UF.value
            n100.VALOR_NFE = nfeProc.NFe.infNFe.total.ICMSTot.vNF
            n100.DATA_IMPORTACAO = date.today()
            n100.STATUS_NFE = "AUTORIZADA"
            blocoN.add(n100)

            # processa fatura/duplicatas
            if nfeProc.NFe.infNFe.cobr:
                if fat := nfeProc.NFe.infNFe.cobr.fat:
                    n140 = RegistroN140()
                    n140.NUM_FAT = fat.nFat
                    n140.VLR_ORIG = self.__checkFloat(fat.vOrig)
                    n140.VLR_DESC = self.__checkFloat(fat.vDesc)
                    n140.VLR_LIQ = self.__checkFloat(fat.vLiq)
                    blocoN.add(n140)

                for dup in nfeProc.NFe.infNFe.cobr.dup:
                    n141 = RegistroN141()
                    n141.NUM_DUP = dup.nDup
                    n141.DT_VENC = self.__checkDate(dup.dVenc)
                    n141.VLR_DUP = self.__checkFloat(dup.vDup)
                    blocoN.add(n141)

            # processa itens da nfe   
            for i, item in enumerate(nfeProc.NFe.infNFe.det, start=1):

                n170 = RegistroN170()
                n170.CNPJ_EMIT =  n100.CNPJ_EMIT
                n170.NUM_NFE = n100.NUM_NFE
                n170.SERIE = n100.SERIE 
                n170.NUM_ITEM = i
                n170.COD_PROD = item.prod.cProd
                n170.DESC_PROD = item.prod.xProd
                n170.NCM = item.prod.NCM
                n170.CFOP = item.prod.CFOP
                n170.VLR_UNIT = self.__checkFloat(item.prod.vUnCom)
                n170.QTDE = self.__checkFloat(item.prod.qCom)
                n170.UNID = item.prod.uCom
                n170.VLR_PROD = self.__checkFloat(item.prod.vProd)
                n170.VLR_FRETE = self.__checkFloat(item.prod.vFrete)
                n170.VLR_SEGURO = self.__checkFloat(item.prod.vSeg)
                n170.VLR_DESC = self.__checkFloat(item.prod.vDesc)
                n170.VLR_OUTROS = self.__checkFloat(item.prod.vOutro)  
                n170.VLR_ITEM = n170.VLR_PROD + n170.VLR_FRETE + n170.VLR_SEGURO - n170.VLR_DESC + n170.VLR_OUTROS

                icms_data = self.__extract_icms_data(item.imposto.ICMS)
                ipi_data = self.__extract_ipi_data(item.imposto.IPI)

                n170.ORIGEM = icms_data[0] 
                n170.CST_ICMS = icms_data[1] 
                n170.BC_ICMS = icms_data[2] 
                n170.ALQ_ICMS = icms_data[3] 
                n170.VLR_ICMS = icms_data[4] 
                n170.MVA = icms_data[5] 
                n170.BC_ICMSST = icms_data[6] 
                n170.ALQ_ICMSST = icms_data[7] 
                n170.ICMSST = icms_data[8] 

                n170.CST_IPI = ipi_data[0] 
                n170.VLR_IPI = ipi_data[1]

                blocoN.add(n170)

        def __extract_icms_data(self, ICMS):
            
            def fill_list(list, size, fill_value):    
                fill_size = size - len(list)
                if fill_size > 0:
                    list.extend([fill_value] * fill_size)
                return list
                    
            icms_map = {
                'ICMS00': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
                'ICMS20': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
                'ICMS10': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMS30': ('orig.value', 'CST.value', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMS40': ('orig.value', 'CST.value'),
                'ICMS51': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS'),
                'ICMS60': ('orig.value', 'CST.value'),
                'ICMS70': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMS90': ('orig.value', 'CST.value', 'vBC', 'pICMS', 'vICMS', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMSSN101': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN'),
                'ICMSSN102': ('orig.value', 'CSOSN.value'),
                'ICMSSN201': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMSSN202': ('orig.value', 'CSOSN.value', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST'),
                'ICMSSN500': ('orig.value', 'CSOSN.value'),
                'ICMSSN900': ('orig.value', 'CSOSN.value', 'pCredSN', 'vCredICMSSN', 'pICMSST', 'pMVAST', 'vBCST', 'vICMSST')
            }

            for icms_type, attrs in icms_map.items():
                if icms_obj := getattr(ICMS, icms_type):
                    return fill_list([getattr(icms_obj, attr, 0.0) for attr in attrs], 9, 0.0)

            return [None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        def __extract_ipi_data(self, IPI):
            if IPI:
                if IPI.IPITrib:
                    ipi_obj = IPI.IPITrib
                    return [ipi_obj.CST.value, ipi_obj.vIPI]
                elif IPI.IPINT:
                    return [IPI.IPINT.CST.value, 0.0]
            return [None, 0.0]
        
        def save(self, filename: str):
            with open(filename, 'w', encoding='utf-8') as file:
                self._rep.write_to(file)
    
        @staticmethod
        def __format_CNPJ(cnpj):
            if cnpj == "":
                return ""
            try:
                cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
                return cnpj
            except Exception:
                return ""

        @staticmethod
        def __format_CPF(cpf):
            if cpf == "":
                return ""
            try:
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                return cpf
            except Exception:
                return ""
            
        @staticmethod
        def __checkFloat(var):
            if var is None:
                return 0.0
            try:
                return float(var)
            except Exception:
                return 0.0     
        
        @staticmethod
        def __checkDate(date_str):
            return f'{date_str[8:10]}{date_str[5:7]}{date_str[:4]}'      
        
        def __list_xml(self, src_dir_fd: str):
            return [
                os.path.join(src_dir_fd, f)
                for f in os.listdir(src_dir_fd)
                if f.lower().endswith('.xml')
            ]
    
    
    class XMLHandler:
        
        _parser = XmlParser()
        
        @staticmethod
        def nfe_from_path( path) -> NfeProc:
            return NFeTkt.XMLHandler._parser.parse(path, NfeProc)
        @staticmethod
        def evento_canc_from_path(path) -> CancNFe:
            return NFeTkt.XMLHandler._parser.parse(path, CancNFe)
        @staticmethod
        def evento_cce_from_path(path) -> CCe:
            return NFeTkt.XMLHandler._parser.parse(path, CCe)
        @staticmethod
        def nfe_to_xml(nfeproc: NfeProc) -> str:
            return NFeTkt.XMLHandler.to_xml(nfeproc)
        @staticmethod
        def evento_canc_to_xml(nfecanc: CancNFe) -> str:
            return  NFeTkt.XMLHandler.to_xml(nfecanc)
        @staticmethod   
        def evento_cce_to_xml(cce: CCe) -> str:
            return NFeTkt.XMLHandler.to_xml(cce)
        @staticmethod
        def from_path(path) -> Any:
            with contextlib.suppress(Exception):
                for method in [
                    NFeTkt.XMLHandler.nfe_from_path, 
                    NFeTkt.XMLHandler.evento_canc_from_path, 
                    NFeTkt.XMLHandler.evento_cce_from_path
                ]:
                    if xml_instance := method(path):
                        return xml_instance
            return None            
        @staticmethod
        def to_xml(
            clazz,
            indent: str = "  ",
            ns_map: Optional[dict] = None,
            pkcs12_data: Optional[bytes] = None,
            pkcs12_password: Optional[str] = None,
            doc_id: Optional[str] = None,
            pretty_print: Optional[str] = None,  # deprecated
        ) -> str:
            """Serialize binding as xml. You can fill the signature params to sign it."""
            if xsdata.__version__.split(".")[0] in ("20", "21", "22", "23"):
                serializer = XmlSerializer(
                    config=SerializerConfig(pretty_print=pretty_print)
                )
            else:
                # deal with pretty_print deprecation in xsdata >= 24:
                if indent is True:  # (means pretty_print was passed)
                    indent = "  "
                if pretty_print:
                    warnings.warn(
                        "Setting `pretty_print` is deprecated, use `indent` instead",
                        DeprecationWarning,
                    )
                    indent = "  "
                elif pretty_print is False:
                    indent = ""

                if pkcs12_data:
                    indent = ""

                serializer = XmlSerializer(config=SerializerConfig(indent=indent))

            if ns_map is None:

                if hasattr(clazz.Meta, "namespace"):
                    ns_map = {None: clazz.Meta.namespace}
                else:
                    package = clazz._get_package()
                    ns_map = {None: f"http://www.portalfiscal.inf.br/{package}"}
            xml = serializer.render(obj=clazz, ns_map=ns_map)
            if pkcs12_data:
                return NFeTkt.XMLHandler.sign_xml(xml, pkcs12_data, pkcs12_password, doc_id=doc_id)
            return xml

        @classmethod
        def sign_xml(
            cls,
            xml: str,
            pkcs12_data: Optional[bytes] = None,
            pkcs12_password: Optional[str] = None,
            doc_id: Optional[str] = None,
        ) -> str:
            """Sign xml file with pkcs12_data/pkcs12_password certificate.

            Sometimes you need to test with a real certificate.
            You can use the CERT_FILE and CERT_PASSWORD environment
            variables to do tests with a real certificate data.
            """
            try:
                from erpbrasil.assinatura import certificado as cert
                from erpbrasil.assinatura.assinatura import Assinatura
            except ImportError as e:
                raise (RuntimeError("erpbrasil.assinatura package is not installed!")) from e

            certificate = cert.Certificado(
                arquivo=os.get("CERT_FILE", pkcs12_data),
                senha=os.get("CERT_PASSWORD", pkcs12_password),
            )
            xml_etree = etree.fromstring(xml.encode("utf-8"))
            return Assinatura(certificate).assina_xml2(xml_etree, doc_id)
        @staticmethod
        def schema_validation(obj_xml: Any, xml: str, schema_path: Optional[str] = None) -> List:
            """Validate xml against xsd schema at given path."""
            validation_messages = []
            doc_etree = etree.fromstring(xml.encode("utf-8"))
            if schema_path is None:
                schema_path = NFeTkt.XMLHandler.get_schema_path(obj_xml)
            xmlschema_doc = etree.parse(schema_path)
            parser = etree.XMLSchema(xmlschema_doc)

            if not parser.validate(doc_etree):
                validation_messages.extend(e.message for e in parser.error_log)
            return validation_messages

        @classmethod
        def get_schema_path(cls, obj_xml: Any) -> str:

            package = inspect.getmodule(obj_xml).__name__
            if package[:10] == "nfelib.nfe":
                return os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "nfe",
                    "schemas",
                    "v4_0",
                    "procNFe_v4.00.xsd",
                )
            if package[:10] == "nfelib.cce":
                return os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "cce",
                    "schemas",
                    "v1_0",
                    "procCCeNFe_v1.00.xsd",
                )
            if package[:14] == "nfelib.nfecanc":
                return os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "nfecanc",
                    "schemas",
                    "v1_0",
                    "procEventoCancNFe_v1.00.00.xsd",
                )
            return "undef"

        @staticmethod
        def validate_xml(obj_xml: Any, schema_path: Optional[str] = None) -> List:
            """Serialize binding as xml, validate it and return possible errors."""
            xml = NFeTkt.XMLHandler.to_xml(obj_xml)
            return NFeTkt.XMLHandler.schema_validation(obj_xml, xml, schema_path) 
        
        @staticmethod
        def nfe_to_pdf(nfeProc: NfeProc, pdf_filename: str):
            pdf_bytes = nfeProc.to_pdf()
            with open(pdf_filename, 'wb') as arquivo:
                arquivo.write(pdf_bytes)       
            
    class XMLOrganizer:

        def organize_xmls(self, source_dir_fd: str, dest_dir_fd: str, folders_map=None):
            """oraniza os arquivos xml contidos em uma pasta e os move para subpastas de 
            um diretório fornecido pelo usuário (pastas padrão: nfe, canc, cce e inut)""" 
            NFeTkt.XMLOrganizer.create_dest_folders(dest_dir_fd, folders_map)

            for root, dirs, files in os.walk(source_dir_fd):
                for file in files:
                    file_path = Path(root) / file
                    if file.endswith('.zip'):
                        self.extract_xmls(file_path, dest_dir_fd)
                    elif file.endswith('.xml'):
                        try:
                            xml_type = self.xml_type(file_path)
                            if xml_type == 'unknown_type':
                                print(f"Arquivo {file} não é um arquivo xml conhecido")
                            else:
                                file_path.rename(Path(dest_dir_fd) / folders_map[xml_type] / file)
                        except Exception as e:
                            print(f"Erro ao processar {file}: {e}")

        def extract_xmls(self, zipFile: str, dest_dir_fd: str):
            """extrai os arquivos xml de um arquivo zip e os organiza em um diretório fornecido pelo usuário"""
            
            temp_folder = Path.cwd() / ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            with zipfile.ZipFile(zipFile, 'r') as zip_ref:
                zip_ref.extractall(temp_folder)

            NFeTkt.XMLOrganizer.organize_xmls(temp_folder, dest_dir_fd)
            shutil.rmtree(temp_folder)

        @staticmethod
        def xml_type(xml_file):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

            if root.tag == '{http://www.portalfiscal.inf.br/nfe}nfeProc':
                return 'nfe_type'
            elif root.tag == '{http://www.portalfiscal.inf.br/nfe}procEventoNFe':
                tipo_evento = root.find('.//nfe:tpEvento', ns).text
                return {'110111': 'canc_type', '110110': 'cce_type'}.get(tipo_evento, 'undefined')
            elif root.tag == '{http://www.portalfiscal.inf.br/nfe}retInutNFe':
                return 'inut_type'

            return 'unknown_type'   
                
        def create_dest_folders(self, path: str, dest_fds_map: dict = None):
            if dest_fds_map is None:
                dest_fds_map = {
                    'nfe_type': 'nfe',
                    'canc_type': 'canc',
                    'cce_type': 'cce',
                    'inut_type': 'inut',
                }
            """Cria as pastas necessárias para armazenar os arquivos XML."""    
            if not os.path.exists(path):
                os.makedirs(path)

            for key in dest_fds_map:
                if not os.path.exists(f"{path}\\{dest_fds_map[key]}"):
                    os.makedirs(f"{path}\\{dest_fds_map[key]}")
    
    class NFeTagFix:
        
        def __init__(self, xml_content: str, config_file: str):
            # Inicializa com o conteúdo XML e o caminho para o arquivo de configuração
            self.tree = ET.ElementTree(ET.fromstring(xml_content))
            self.root = self.tree.getroot()
            
            # Carrega o arquivo de configuração JSON
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        
        def apply(self):
            
            # Percorre as regras no arquivo de configuração
            for rule in self.config.get("rules", []):
                namespace = rule.get("namespace", {})
                path = rule.get("path")
                tag = rule.get("tag")
                condition = rule.get("condition", {})
                new_value = rule.get("new_value")
                
                # Aplica a correção com base na condição
                self.apply_rule(path, namespace, tag, condition, new_value)
        
        def apply_rule(self, path, namespace, tag, condition: dict, new_value):
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
        
        def get_xml_content(self):
            return ET.tostring(self.root, encoding='unicode')