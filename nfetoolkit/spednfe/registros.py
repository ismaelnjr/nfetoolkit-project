from sped.registros import Registro
from sped.campos import Campo, CampoFixo, CampoData, CampoNumerico

class Registro0000(Registro):
    """
    ABERTURA DO ARQUIVO DIGITAL 
    """
    campos = [
        CampoFixo(1, 'REG', '0000'),
        Campo(2, 'NOME_EMPRESA'),
        Campo(3, 'CNPJ'),
    ]

class RegistroN001(Registro):
    """
    ABERTURA DO BLOCO N
    """
    campos = [
        CampoFixo(1, 'REG', 'N001'),
        Campo(2, 'IND_DAD'),
    ]

class RegistroN100(Registro):
    """
    CABEÇALHO DA NFE (NIVEL 1) (1:N)
    """
    campos = [
        CampoFixo(1, 'REG', 'N100'),
        Campo(2, 'CNPJ_EMIT'),
        Campo(3, 'NOME_EMIT'),
        Campo(4, 'NUM_NFE'),
        Campo(5, 'SERIE'),
        CampoData(6, 'DT_EMISSAO'),
        Campo(7, 'TIPO_NFE'),
        Campo(8, 'CHAVE_NFE'),    
        Campo(9, 'CNPJ_DEST'),
        Campo(10, 'CPF_DEST'),
        Campo(11, 'NOME_DEST'),
        Campo(12, 'UF'),
        CampoNumerico(13, 'VALOR_NFE', precisao=2),
        Campo(14, ''),        
        Campo(15, 'MES_ANO'),
        CampoData(16, 'DATA_IMPORTACAO'),
        Campo(17, 'STATUS_NFE'),
        Campo(18, 'X_USER1'),
        Campo(19, 'X_USER2'),
    ]

class RegistroN140(Registro):
    """
    FATURAS DA NFE (NIVEL 2) (1:N)
    """
    campos = [
        CampoFixo(1, 'REG', 'N140'),
        Campo(2, 'NUM_FAT'),
        CampoNumerico(3, 'VLR_ORIG', precisao=2),        
        CampoNumerico(4, 'VLR_DESC', precisao=2), 
        CampoNumerico(5, 'VLR_LIQ', precisao=2), 
    ]

class RegistroN141(Registro):
    """
    DUPLICATAS DA FATURA (NIVEL 3) (1:N)
    """
    campos = [
        CampoFixo(1, 'REG', 'N141'),
        Campo(2, 'NUM_DUP'),
        CampoData(3, 'DT_VENC'),
        CampoNumerico(4, 'VLR_DUP', precisao=2),        
    ]
    
class RegistroN170(Registro):
    """
    ITENS DA NFE (NIVEL 2) (1:N)
    """
    campos = [
        CampoFixo(1, 'REG', 'N170'),
        Campo(2, 'CNPJ_EMIT'),
        Campo(3, 'NUM_NFE'),
        Campo(4, 'SERIE'),
        CampoNumerico(5, 'NUM_ITEM'),
        Campo(6, 'COD_PROD'),
        Campo(7, 'DESC_PROD'),
        Campo(8, 'NCM'),
        Campo(9, 'CFOP'),
        CampoNumerico(10, 'VLR_UNIT', precisao=2),
        CampoNumerico(11, 'QTDE', precisao=4),
        Campo(12, 'UNID'),
        CampoNumerico(13, 'VLR_PROD', precisao=2),
        CampoNumerico(14, 'VLR_FRETE', precisao=2),
        CampoNumerico(15, 'VLR_SEGURO', precisao=2),
        CampoNumerico(16, 'VLR_DESC', precisao=2),
        CampoNumerico(17, 'VLR_OUTROS', precisao=2),
        CampoNumerico(18, 'VLR_ITEM', precisao=2),
        Campo(19, 'ORIGEM'),
        Campo(20, 'CST_ICMS'),
        CampoNumerico(21, 'BC_ICMS', precisao=2),
        CampoNumerico(22, 'ALQ_ICMS', precisao=2),
        CampoNumerico(23, 'VLR_ICMS', precisao=2),
        CampoNumerico(24, 'MVA', precisao=2),
        CampoNumerico(25, 'BC_ICMSST', precisao=2),
        CampoNumerico(26, 'ALQ_ICMSST', precisao=2),
        CampoNumerico(27, 'ICMSST', precisao=2),
        Campo(28, 'CST_IPI'),
        CampoNumerico(29, 'VLR_IPI', precisao=2),
    ]

class RegistroN990(Registro):
    """
    ENCERRAMENTO DO BLOCO N
    """
    campos = [
        CampoFixo(1, 'REG', 'N990'),
        CampoNumerico(2, 'QTD_LIN_N'),        
    ]

class RegistroZ001(Registro):
    """
    ABERTURA DO BLOCO Z
    """
    campos = [
        CampoFixo(1, 'REG', 'Z001'),
        Campo(2, 'IND_DAD'),
    ]

class RegistroZ100(Registro):
    """
    EVENTOS DA NFE
    """
    campos = [
        CampoFixo(1, 'REG', 'Z100'),
        Campo(2, 'CNPJ'),
        Campo(3, 'CPF'),
        Campo(4, 'CHAVE_NFE'),
        CampoData(5, 'DATA_EVENTO'),  
        Campo(6, 'TIPO_EVENTO'),    
        Campo(7, 'DESC_EVENTO'),  
        Campo(8, 'MOTIVO'),  
        Campo(8, 'PROTOCOLO'), 
    ]

class RegistroZ990(Registro):
    """
    ENCERRAMENTO DO BLOCO Z
    """
    campos = [
        CampoFixo(1, 'REG', 'Z990'),
        CampoNumerico(2, 'QTD_LIN_Z'),        
    ]

class Registro9999(Registro):
    """
    ENCERRAMENTO DO ARQUIVO DIGITAL
    """
    campos = [
        CampoFixo(1, 'REG', '9999'),
        CampoNumerico(2, 'QTD_LIN'),
    ]