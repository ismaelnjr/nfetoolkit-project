import contextlib
import os
import warnings
import os
import xsdata
import inspect
import xml.etree.ElementTree as ET

from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from nfelib.nfe_evento_cancel.bindings.v1_0 import ProcEventoNfe as CancNFe
from nfelib.nfe_evento_cce.bindings.v1_0.proc_cce_nfe_v1_00 import ProcEventoNfe as CCe
from xsdata.formats.dataclass.parsers import XmlParser
from lxml import etree
from typing import Optional, List, Any


class NFeHandler:
    '''
    The XMLHandler class provides static methods to serialize and validate XML of Nota Fiscal Eletrônica (NFe) documents.
    Also can be used to parse XML documents and generate in pdf format.  
    '''
        
    _parser = XmlParser()
    
    @staticmethod
    def nfe_from_path( path) -> NfeProc:
        return NFeHandler._parser.parse(path, NfeProc)
    
    @staticmethod
    def evento_canc_from_path(path) -> CancNFe:
        return NFeHandler._parser.parse(path, CancNFe)
    
    @staticmethod
    def evento_cce_from_path(path) -> CCe:
        return NFeHandler._parser.parse(path, CCe)
    
    @staticmethod
    def nfe_to_xml(nfeproc: NfeProc) -> str:
        return NFeHandler.to_xml(nfeproc)
    
    @staticmethod
    def evento_canc_to_xml(nfecanc: CancNFe) -> str:
        return  NFeHandler.to_xml(nfecanc)
    
    @staticmethod   
    def evento_cce_to_xml(cce: CCe) -> str:
        return NFeHandler.to_xml(cce)
    
    @staticmethod
    def from_path(path) -> Any:
        with contextlib.suppress(Exception):
            for method in [
                NFeHandler.nfe_from_path, 
                NFeHandler.evento_canc_from_path, 
                NFeHandler.evento_cce_from_path
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
            return NFeHandler.sign_xml(xml, pkcs12_data, pkcs12_password, doc_id=doc_id)
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
    def _schema_validation(obj_xml: Any, xml: str, schema_path: Optional[str] = None) -> List:
        """Validate xml against xsd schema at given path."""
        validation_messages = []
        doc_etree = etree.fromstring(xml.encode("utf-8"))
        if schema_path is None:
            schema_path = NFeHandler._get_schema_path(obj_xml)
        xmlschema_doc = etree.parse(schema_path)
        parser = etree.XMLSchema(xmlschema_doc)

        if not parser.validate(doc_etree):
            validation_messages.extend(e.message for e in parser.error_log)
        return validation_messages

    @classmethod
    def _get_schema_path(cls, obj_xml: Any) -> str:

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
        xml = NFeHandler.to_xml(obj_xml)
        return NFeHandler._schema_validation(obj_xml, xml, schema_path) 
    
    @staticmethod
    def nfe_to_pdf(nfeProc: NfeProc, pdf_filename: str):
        pdf_bytes = nfeProc.to_pdf()
        with open(pdf_filename, 'wb') as arquivo:
            arquivo.write(pdf_bytes)
            
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