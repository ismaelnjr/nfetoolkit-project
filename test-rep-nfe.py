from spednfe.nfetoolkit import NFeToolkit 
from spednfe.arquivos import RepositorioNFe

nfeToolkit = NFeToolkit()

rep_nfe = RepositorioNFe()
# C:\\vs_code\\nfetoolkit-project\\etc
# C:\\temp\\dest\\nfe
nfeToolkit.store_nfe_from_dir('C:\\temp\\dest\\nfe', rep_nfe)

with open('nfe_data.txt', 'w', encoding='utf-8') as file:
    rep_nfe.write_to(file)
