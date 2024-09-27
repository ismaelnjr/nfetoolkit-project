from sped.blocos import Bloco
from .registros import RegistroN001
from .registros import RegistroN990
from .registros import RegistroZ001
from .registros import RegistroZ990


class BlocoN(Bloco):
    """
    Abertura, Identificação e Referências
    """
    registro_abertura = RegistroN001()
    registro_encerramento = RegistroN990()   

    def __init__(self):
        Bloco.__init__(self, "N")

class BlocoZ(Bloco):
    """
    Eventos da NFe
    """
    registro_abertura = RegistroZ001()
    registro_encerramento = RegistroZ990()   

    def __init__(self):
        Bloco.__init__(self, "Z")