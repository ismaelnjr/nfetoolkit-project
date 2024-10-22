import os
import xml.etree.ElementTree as ET
import os

from datetime import date

from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc
from nfelib.nfe_evento_cancel.bindings.v1_0 import ProcEventoNfe as CancNFe
from nfelib.nfe_evento_cce.bindings.v1_0.proc_cce_nfe_v1_00 import ProcEventoNfe as CCe
from typing import List, Any, Union
from .nfe_organizer import NFeOrganizer
from .nfe_handler import NFeHandler
from sped.nfe.arquivos import ArquivoDigital
from sped.nfe.registros import RegistroN100, RegistroN140, RegistroN141, RegistroN170, RegistroZ100


class NFeRepository(ArquivoDigital):
    '''
    The NFeRepository is a extended version of the ArquivoDigital class.     
    The method store_nfe is used to store NFe information (NFeProc) in the repository.    
    The method store_evt is used to store events information (CCe e CancNFe) in the repository.
    NFeProc, CCe and CancNFe can be instantiated by the NFeHandler class.
    '''
    
    def store_evt(self, evt: Union[CancNFe, CCe]):
        
        z100 = RegistroZ100()
        z100.CNPJ = self.__format_CNPJ(evt.retEvento.infEvento.CNPJDest)
        z100.CPF = self.__format_CPF(evt.retEvento.infEvento.CPFDest)
        z100.CHAVE_NFE = evt.retEvento.infEvento.chNFe
        z100.DATA_EVENTO = evt.retEvento.infEvento.dhRegEvento[8:10] + evt.retEvento.infEvento.dhRegEvento[5:7] + evt.retEvento.infEvento.dhRegEvento[:4]
        z100.TIPO_EVENTO = evt.retEvento.infEvento.tpEvento
        z100.MOTIVO = evt.retEvento.infEvento.xMotivo
        z100.PROTOCOLO = evt.retEvento.infEvento.nProt
        z100.DESC_EVENTO = evt.retEvento.infEvento.xEvento
        self.blocoZ.add(z100)            

    
    def store_nfe(self, nfeProc: NfeProc):  # sourcery skip: extract-method

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
        self.blocoN.add(n100)

        # processa fatura/duplicatas
        if nfeProc.NFe.infNFe.cobr:
            if fat := nfeProc.NFe.infNFe.cobr.fat:
                n140 = RegistroN140()
                n140.NUM_FAT = fat.nFat
                n140.VLR_ORIG = self.__checkFloat(fat.vOrig)
                n140.VLR_DESC = self.__checkFloat(fat.vDesc)
                n140.VLR_LIQ = self.__checkFloat(fat.vLiq)
                self.blocoN.add(n140)

            for dup in nfeProc.NFe.infNFe.cobr.dup:
                n141 = RegistroN141()
                n141.NUM_DUP = dup.nDup
                n141.DT_VENC = self.__checkDate(dup.dVenc)
                n141.VLR_DUP = self.__checkFloat(dup.vDup)
                self.blocoN.add(n141)

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

            self.blocoN.add(n170)


    def __extract_icms_data(self,ICMS):
        
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
