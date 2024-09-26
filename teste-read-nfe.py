from spednfe.nfetoolkit import NFeToolkit 
from spednfe.nfetoolkit import NfeProc

nfeToolkit = NFeToolkit()

#nfeProc = nfeToolkit.nfe_from_path("etc//35240523004906000180550010001354181002078142.xml")
nfeProc = nfeToolkit.nfe_from_path("etc//35240523004906000180550010001354231002078428.xml")


print(nfeToolkit._read_nfe_content(nfeProc))