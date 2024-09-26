from spednfe.nfetoolkit import NFeToolkit 
from spednfe.nfetoolkit import CCe
from spednfe.nfetoolkit import CancNFe
from spednfe.nfetoolkit import NfeProc

nfeToolkit = NFeToolkit()

nfeProc = nfeToolkit.nfe_from_path("etc//xml//35240406313527000152550010000688321001248368-nfe.xml")
print(f"NFe Id: {nfeProc.NFe.infNFe.Id}")

nfecanc = nfeToolkit.evento_canc_from_path("etc//xml//35240406313527000152550010000688311001248352-caneve.xml")
print(f"Motivo cancelamento: {nfecanc.evento.infEvento.detEvento.xJust}")

cce = nfeToolkit.evento_cce_from_path("etc//xml//32230758507468001986551010000039381010039382-cce-nfe.xml")
print(f"Correção CCe: {cce.evento.infEvento.detEvento.xCorrecao}")

#print(nfeToolkit.evento_cce_to_xml(cce))

#print(f"Validate xml: {nfeToolkit.validate_xml(nfeProc)}")

obj = nfeToolkit.from_path("etc//xml//35240406313527000152550010000688311001248352-caneve.xml")
if isinstance(obj, NfeProc):
    print("É uma nfe")
elif isinstance(obj, CancNFe):
    print("É um cancelamento nfe")