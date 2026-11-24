"""Testes simples do roteador, sem depender de APIs externas."""

import unittest

from phoneinfo.exceptions import DeviceNotFoundError, QuotaExceededError
from phoneinfo.models import DeviceInfo
from phoneinfo.provider import DeviceProvider
from phoneinfo.router import ProviderRouter


class ProvedorFalso(DeviceProvider):
    def __init__(self, nome, prioridade, resultado=None, erro=None):
        super().__init__(nome, prioridade)
        self.__resultado = resultado
        self.__erro = erro
        self.chamadas = 0

    def buscar(self, marca, modelo):
        self.chamadas += 1
        if self.__erro is not None:
            raise self.__erro
        if self.__resultado is None:
            raise DeviceNotFoundError(provedor=self.nome)
        return self.__resultado


class TestProviderRouter(unittest.TestCase):
    def test_troca_de_provedor_quando_cota_esgota(self):
        sem_cota = ProvedorFalso(
            "API-A", 10, erro=QuotaExceededError(provedor="API-A", retry_after=1)
        )
        disponivel = ProvedorFalso("API-B", 5, resultado=DeviceInfo("Samsung", "S24"))

        roteador = ProviderRouter().adicionar_provedor(sem_cota).adicionar_provedor(disponivel)
        resultado = roteador.buscar("Samsung", "S24")

        self.assertEqual(resultado.provedor, "API-B")
        self.assertEqual(sem_cota.chamadas, 1)
        self.assertEqual(disponivel.chamadas, 1)
        self.assertFalse(roteador.status()[0]["disponivel"])

    def test_cache_evita_segunda_chamada(self):
        provedor = ProvedorFalso("API-A", 10, resultado=DeviceInfo("Apple", "iPhone 15"))
        roteador = ProviderRouter().adicionar_provedor(provedor)

        roteador.buscar("apple", "iphone 15")
        roteador.buscar("Apple", "iPhone 15")

        self.assertEqual(provedor.chamadas, 1)

    def test_erro_quando_todos_esgotam(self):
        a = ProvedorFalso("A", 2, erro=QuotaExceededError(provedor="A"))
        b = ProvedorFalso("B", 1, erro=QuotaExceededError(provedor="B"))
        roteador = ProviderRouter().adicionar_provedor(a).adicionar_provedor(b)

        with self.assertRaises(Exception):
            roteador.buscar("X", "Y")


if __name__ == "__main__":
    unittest.main()
