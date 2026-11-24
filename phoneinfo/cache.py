"""Cache em memória para não gastar cota com consultas repetidas."""

import time


class DeviceCache:
    def __init__(self, ttl_segundos=86400):
        self.__ttl = ttl_segundos
        self.__registros = {}

    @staticmethod
    def chave(marca, modelo):
        return "%s::%s" % (
            str(marca or "").strip().lower(),
            str(modelo or "").strip().lower(),
        )

    def obter(self, marca, modelo):
        registro = self.__registros.get(self.chave(marca, modelo))
        if registro is None:
            return None
        instante, valor = registro
        if time.time() - instante > self.__ttl:
            del self.__registros[self.chave(marca, modelo)]
            return None
        return valor

    def guardar(self, marca, modelo, valor):
        self.__registros[self.chave(marca, modelo)] = (time.time(), valor)

    def limpar(self):
        self.__registros.clear()

    @property
    def tamanho(self):
        return len(self.__registros)
