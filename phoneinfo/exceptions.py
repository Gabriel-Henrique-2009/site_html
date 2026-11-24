"""Exceções específicas da camada de consulta de aparelhos."""


class PhoneInfoError(Exception):
    """Erro base de toda a camada phoneinfo."""

    def __init__(self, mensagem):
        super().__init__(mensagem)


class ProviderError(PhoneInfoError):
    """Falha genérica de um provedor de dados."""

    def __init__(self, mensagem, provedor=None):
        self.__provedor = provedor
        super().__init__(mensagem)

    @property
    def provedor(self):
        return self.__provedor


class QuotaExceededError(ProviderError):
    """Cota/tokens esgotados ou limite de requisições atingido.

    É esse erro que dispara a troca automática de provedor no roteador.
    """

    def __init__(self, mensagem="Cota esgotada", provedor=None, retry_after=None):
        self.__retry_after = retry_after
        super().__init__(mensagem, provedor)

    @property
    def retry_after(self):
        """Segundos sugeridos pelo provedor para nova tentativa."""
        return self.__retry_after


class ProviderUnavailableError(ProviderError):
    """Provedor fora do ar, bloqueado ou com falha de rede."""

    pass


class DeviceNotFoundError(PhoneInfoError):
    """O aparelho não existe naquele provedor (não é falha de cota)."""

    def __init__(self, mensagem="Aparelho não encontrado", provedor=None):
        self.__provedor = provedor
        super().__init__(mensagem)

    @property
    def provedor(self):
        return self.__provedor
