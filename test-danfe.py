from nfelib.nfe.bindings.v4_0 import NfeProc
from xsdata.formats.dataclass.parsers import XmlParser


parser = XmlParser()
nfeProc = parser.parse("etc//xml//35240406313527000152550010000688321001248368-nfe.xml", NfeProc)

pdf_bytes = nfeProc.to_pdf()

with open("exemplo.pdf", 'wb') as arquivo:
    arquivo.write(pdf_bytes)
