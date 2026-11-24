"""Roteador com fallback automático entre provedores.

Funciona como um roteador de LLM: se o provedor atual esgota a cota
(ou fica indisponível), ele entra em cooldown e o próximo é tentado.
"""

import time

from .cache import DeviceCache
from .exceptions import DeviceNotFoundError, ProviderError, QuotaExceededError, ProviderUnavailableError


class ProviderRouter:
    def __init__(self, cooldown_segundos=300, cache=None):
        self.__provedores = []
        self.__cooldown_segundos = cooldown_segundos
        self.__cache = cache if cache is not None else DeviceCache()
        self.__pausas = {}
        self.__ultimo_erros = []

    @property
    def cache(self):
        return self.__cache

    @property
    def ultimos_erros(self):
        return list(self.__ultimo_erros)

    def adicionar_provedor(self, provedor):
        self.__provedores.append(provedor)
        return self

    def quantidade_provedores(self):
        return len(self.__provedores)

    def buscar(self, marca, modelo):
        """Busca o aparelho, alternando de provedor quando necessário."""
        em_cache = self.__cache.obter(marca, modelo)
        if em_cache is not None:
            return em_cache

        erros = []
        agora = time.time()

        for provedor in self._provedores_ordenados():
            if self.__esta_pausado(provedor, agora):
                erros.append("%s em cooldown" % provedor.nome)
                continue

            try:
                provedor.exigir_cota(agora)
                info = provedor.buscar(marca, modelo)
                if not info.provedor:
                    info.definir_provedor(provedor.nome)
                if info.consultado_em is None:
                    info.definir_consultado_em(agora)
                self.__cache.guardar(marca, modelo, info)
                self.__ultimo_erros = erros
                return info
            except DeviceNotFoundError as erro:
                # Ausência no catálogo não desqualifica o provedor.
                erros.append("%s: %s" % (provedor.nome, erro))
            except QuotaExceededError as erro:
                segundos = erro.retry_after or self.__cooldown_segundos
                self.__pausas[provedor.nome] = agora + segundos
                erros.append("%s: cota esgotada (pausa %ss)" % (provedor.nome, segundos))
            except ProviderUnavailableError as erro:
                self.__pausas[provedor.nome] = agora + self.__cooldown_segundos
                erros.append("%s: %s" % (provedor.nome, erro))
            except ProviderError as erro:
                erros.append("%s: %s" % (provedor.nome, erro))

        self.__ultimo_erros = erros
        raise ProviderError(
            "Nenhum provedor conseguiu responder. Detalhes: %s" % "; ".join(erros)
        )

    def status(self):
        """Snapshot simples para debug/UI."""
        agora = time.time()
        return [
            {
                "provedor": provedor.nome,
                "prioridade": provedor.prioridade,
                "disponivel": not self.__esta_pausado(provedor, agora),
                "cooldown_restante": max(
                    0, int(self.__pausas.get(provedor.nome, 0) - agora)
                ),
            }
            for provedor in self._provedores_ordenados()
        ]

    def liberar_todos(self):
        """Força o fim do cooldown (útil em testes/manual)."""
        self.__pausas.clear()
        for provedor in self.__provedores:
            provedor.reiniciar_contador()

    def _provedores_ordenados(self):
        return sorted(self.__provedores, key=lambda p: p.prioridade, reverse=True)

    def __esta_pausado(self, provedor, agora):
        return self.__pausas.get(provedor.nome, 0) > agora
