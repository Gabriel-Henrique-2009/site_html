"""Modelo de domínio: informações padronizadas de um aparelho."""

import json


class DeviceInfo:
    """Representação comum, independente do provedor de origem."""

    def __init__(self, marca="", modelo="", dados=None, provedor="", consultado_em=None):
        self.__marca = marca
        self.__modelo = modelo
        self.__dados = dict(dados or {})
        self.__provedor = provedor
        self.__consultado_em = consultado_em

    @property
    def marca(self):
        return self.__marca

    @property
    def modelo(self):
        return self.__modelo

    @property
    def dados(self):
        return dict(self.__dados)

    @property
    def provedor(self):
        return self.__provedor

    @property
    def consultado_em(self):
        return self.__consultado_em

    def definir_provedor(self, provedor):
        self.__provedor = provedor

    def definir_consultado_em(self, instante):
        self.__consultado_em = instante

    def obter(self, campo, padrao=""):
        """Lê um campo normalizado (ex.: 'tela', 'chipset', 'bateria')."""
        return self.__dados.get(campo, padrao)

    def definir(self, campo, valor):
        self.__dados[campo] = valor

    def to_dict(self):
        return {
            "marca": self.__marca,
            "modelo": self.__modelo,
            "dados": dict(self.__dados),
            "provedor": self.__provedor,
            "consultado_em": self.__consultado_em,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_dict(cls, dados):
        return cls(
            marca=dados.get("marca", ""),
            modelo=dados.get("modelo", ""),
            dados=dados.get("dados", {}),
            provedor=dados.get("provedor", ""),
            consultado_em=dados.get("consultado_em"),
        )

    def __str__(self):
        return "%s %s (fonte: %s)" % (self.__marca, self.__modelo, self.__provedor or "desconhecida")
