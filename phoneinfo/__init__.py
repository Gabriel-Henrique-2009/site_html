"""Pacote para consulta de informações de aparelhos telefônicos.

Projeto final de POO - camada independente da agenda (Streamlit/SQLite).
"""

from .models import DeviceInfo
from .exceptions import (
    PhoneInfoError,
    ProviderError,
    QuotaExceededError,
    ProviderUnavailableError,
    DeviceNotFoundError,
)
from .provider import DeviceProvider
from .router import ProviderRouter

__all__ = [
    "DeviceInfo",
    "PhoneInfoError",
    "ProviderError",
    "QuotaExceededError",
    "ProviderUnavailableError",
    "DeviceNotFoundError",
    "DeviceProvider",
    "ProviderRouter",
]
