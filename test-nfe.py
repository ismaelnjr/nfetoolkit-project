from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from xsdata.formats.dataclass.parsers import XmlParser

nfe_proc = NfeProc().from_path("etc//xml//35240406313527000152550010000688311001248352-nfe.xml")
print(nfe_proc.NFe.infNFe.emit.CNPJ)

#Dá ERRO esta chamada