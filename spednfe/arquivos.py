from datetime import datetime
   
from sped.arquivos import ArquivoDigital   
from .blocos import BlocoN
from .blocos import BlocoZ

from .registros import Registro0000
from .registros import Registro9999


class RepositorioNFe(ArquivoDigital):
    registro_abertura = Registro0000
    registro_encerramento = Registro9999        
    
    def __init__(self):
        ArquivoDigital.__init__(self)
        self._blocos['N'] = BlocoN()
        self._blocos['Z'] = BlocoZ()
        self._registro_factory_name = "spedpy.nfe.registros_nfe"
     
    @property
    def blocoN(self):
        return self._blocos['N']
    
    @property
    def blocoZ(self):
        return self._blocos['Z']
    
    def prepare(self):
        n = len(self._blocos['N'].registros) - 2
        self.blocoN.registro_abertura.IND_DAD = '1' if n > 0 else '0'
        self.blocoN.registro_encerramento.QTD_LIN_N = n
        z = len(self._blocos['Z'].registros) - 2
        self.blocoZ.registro_abertura.IND_DAD = '1' if z > 0 else '0'
        self.blocoZ.registro_encerramento.QTD_LIN_Z = z

        for ev in self.blocoZ.registros:
            if ev.REG == "Z100" and ev.TIPO_EVENTO == "110111":
                self._changeStatusNFe(ev.CHAVE_NFE, "CANCELADO")
                
    def _changeStatusNFe(self, chaveNFe, status):
        for r in self.blocoN.registros:
            if r.REG == "N100" and r.CHAVE_NFE == chaveNFe:
                r.STATUS_NFE = status

    def write_to(self, buff):
        self.prepare()
        buff.write(self._registro_abertura.as_line() + u'\n')
        reg_count = 2
        for key in self._blocos.keys():
            bloco = self._blocos[key]
            reg_count += len(bloco.registros)
            for registro in bloco.registros:
                buff.write(registro.as_line() + u'\n')
        self._registro_encerramento[2] = reg_count
        buff.write(self._registro_encerramento.as_line() + u'\n')