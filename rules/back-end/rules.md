---
title: Back-end — regras gerais da área
description: Regras que valem pra qualquer stack de back-end (django, …) — verticalização por domínio, camadas, dados, erros e segurança. Os arquivos de stack só adicionam o específico.
applies-to: back-end
extends: ../general/general-rules.md
skills: mattpocock/skills/domain-modeling
---

> Regras gerais de back-end — valem pra **qualquer** stack da área (django, …).
> As regras de stack só adicionam o que é específico delas.

## Organização

- **Verticalização por domínio/feature**: cada feature agrupa seus próprios models, services, schemas e rotas — não separe por camada técnica global.
- Regra de negócio no **service layer** — nunca na view/controller nem espalhada no model.
- Validação de entrada na **borda** (schema/serializer), uma vez — não repetida por toda parte.

## Dados e erros

- Nada de regra de negócio dentro de migration.
- Erros explícitos e tipados; nunca engula exceção (`except: pass`).
- Sem query dentro de loop — resolva em lote (evite N+1).
- Listagem sempre **paginada** por padrão; nunca retorne coleção ilimitada.

## Efeitos e consistência

- Escrita multi-passo é **transacional** (tudo ou nada).
- Efeito colateral externo (email, pagamento, fila) é **idempotente** — retry não duplica.

## Segurança

- Segredo só via variável de ambiente; nunca no código nem versionado.
- Toda entrada externa é não-confiável até validada.
