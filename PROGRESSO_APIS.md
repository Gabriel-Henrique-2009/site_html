# Progresso — Pesquisa e agregação de APIs de aparelhos telefônicos

Objetivo: encontrar as melhores APIs para buscar informações de celulares (estilo **GSMArenaParser**) e montar um sistema agregador/roteador com fallback automático (similar a um "free LLM router"): quando uma API esgota cota/tokens ou falha, trocar para a próxima.

---

## Status geral

| Etapa | Status | Observações |
|---|---|---|
| 1. Explorar repositório atual | ✅ Concluído | Python 3 + Streamlit + SQLite, camadas models/dao_sql/service/templates |
| 2. Pesquisar APIs candidatas | ⏳ Em andamento | GSMArenaParser, alternativas, licenças |
| 3. Avaliar cota / limites / custo | ⬜ Pendente | Identificar o que é "token" (rate limit, quota, créditos) |
| 4. Desenhar arquitetura do roteador | ✅ Concluído | Interface comum, fallback, cache, cooldown |
| 5. Implementar adapters | ⬜ Pendente | Um adaptador por API (depende da pesquisa) |
| 6. Implementar roteador com fallback | ✅ Concluído | `projeto/phoneinfo/router.py` + exceções + cache |
| 7. Testes e documentação | ⏳ Parcial | 3 testes do roteador passando; falta documentar as APIs |

---

## APIs candidatas (preenchimento em andamento)

| API / Lib | Tipo | Dados | Limites | Licença | Status |
|---|---|---|---|---|---|
| GSMArenaParser | Scraper (não-oficial) | Especificações completas | Sem API key; depende do HTML | MIT (verificar) | 🔎 Em pesquisa |
| _(a preencher)_ | | | | | |

---

## Decisões e notas

- Repositório é um **trabalho final de POO em Python 3 + Streamlit + SQLite**, com camadas claras: `models/` → `dao_sql/` → `service.py` → `templates/` → `index.py`.
- A solução deve seguir o mesmo padrão: `abc.ABC` + `@abstractmethod` (equivalente à interface), composição, nomes em `snake_case`, mensagens em português e sem type hints (convenção do projeto).
- Novos arquivos devem ficar em um pacote separado (ex.: `projeto/phoneinfo/`) para não misturar com a agenda.
- Ideia central (análoga a roteadores de LLM): existem vários **provedores** atrás de uma **interface comum**. O roteador escolhe o próximo provedor disponível; se ele esgotar cota / dar erro de limite, marca-o em *cooldown* e tenta o seguinte. Isso precisa de um `ProviderResult` padronizado e um erro específico `QuotaExceededException`.

### Rascunho de arquitetura (a validar com a pesquisa)

```
PhoneInfoService (fachada)
   └── ProviderRouter
         ├── DeviceProvider (interface)  ← getByModel(brand, model): DeviceInfo
         │     ├── GsmArenaProvider      (scraper / parser)
         │     ├── XProvider             (API REST)
         │     └── YProvider             (fallback)
         ├── QuotaTracker     ← contador de requisições por provedor
         ├── CooldownPolicy   ← tempo de espera após 429/403
         └── DeviceCache      ← evita gastar cota com repetições

DeviceInfo (modelo de domínio)
   brand, model, releaseDate, display, chipset, memory,
   camera, battery, os, prices, sourceProvider, fetchedAt
```

### Critérios de escolha do roteador

1. Provedor com maior prioridade/qualidade e com cota disponível.
2. Em caso de `QuotaExceeded`/`RateLimited`/`ProviderDown`, marcar em cooldown e tentar o próximo.
3. Cache-first: se já buscou o modelo recentemente, não consome cota.
4. Registrar qual provedor respondeu (`sourceProvider`) para transparência.

_Nota: nomes concretos dos provedores serão definidos após a pesquisa._

## Próximos passos imediatos

1. Concluir exploração do repositório.
2. Levantar APIs com documentação pública e limites claros.
3. Definir contrato comum (`getDevice(brand, model)` etc.).

---

_Arquivo criado automaticamente para acompanhamento do progresso. Atualizado ao longo da sessão._
