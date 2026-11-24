"""Contrato comum que todo provedor de aparelhos deve implementar."""

from abc import ABC, abstractmethod

from .exceptions import QuotaExceededError, ProviderUnavailableError


class DeviceProvider(ABC):
    """Classe abstrata: obriga cada API/scraper a expor ``buscar``.

    O roteador só conhece esse contrato, por isso trocar de provedor
    (quando a cota acaba) não exige mudar quem consome os dados.
    """

    def __init__(self, nome, prioridade=0, limite=None, janela_segundos=60):
        self.__nome = nome
        self.__prioridade = prioridade
        self.__limite = limite
        self.__janela_segundos = janela_segundos
        self.__chamadas = []

    @property
    def nome(self):
        return self.__nome

    @property
    def prioridade(self):
        return self.__prioridade

    @property
    def limite(self):
        return self.__limite

    @abstractmethod
    def buscar(self, marca, modelo):
        """Retorna um ``DeviceInfo`` ou levanta uma exceção de provedor."""
        raise NotImplementedError

    def registrar_chamada(self, agora):
        """Contabiliza uma requisição localmente (para limites conhecidos)."""
        self.__chamadas = [
            instante for instante in self.__chamadas
            if agora - instante < self.__janela_segundos
        ]
        self.__chamadas.append(agora)

    def atingiu_limite(self, agora):
        if self.__limite is None:
            return False
        self.__chamadas = [
            instante for instante in self.__chamadas
            if agora - instante < self.__janela_segundos
        ]
        return len(self.__chamadas) >= self.__limite

    def reiniciar_contador(self):
        self.__chamadas = []

    def exigir_cota(self, agora):
        """Use nos adapters que conhecem seu próprio limite."""
        if self.atingiu_limite(agora):
            raise QuotaExceededError(
                "Limite local de %s requisições/%ss atingido" % (
                    self.__limite, self.__janela_segundos
                ),
                provedor=self.__nome,
                retry_after=self.__janela_segundos,
            )

    def falhar(self, mensagem):
        raise ProviderUnavailableError(mensagem, provedor=self.__nome)

    def __str__(self):
        return "%s (prioridade %s)" % (self.__nome, self.__prioridade)
