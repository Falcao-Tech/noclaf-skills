---
title: Mobile — regras gerais da área
description: Regras que valem pra qualquer plataforma mobile (iOS/Android) — arquitetura em camadas, recursos, estado e qualidade. Os arquivos de plataforma só adicionam o específico.
applies-to: mobile
extends: ../general/general-rules.md
---

> Regras gerais de mobile — valem pra **qualquer** plataforma (iOS/Android).
> As regras de stack só adicionam o que é específico delas.

## Arquitetura

- Apresentação (View) separada da lógica (ViewModel/UseCase) — MVVM/Clean.
- Sem regra de negócio na View nem no controller de tela.
- Navegação centralizada, não espalhada pelas telas.

## Recursos e estado

- Trabalho pesado/IO fora da main/UI thread.
- Estado de tela imutável e unidirecional (fonte única de verdade).
- Libere recursos (listeners, observers) no fim do ciclo de vida.

## Qualidade

- Strings e assets fora do código (localização/resources), nunca hardcoded.
- Sem chamada de rede direto na View.
- Estados de **loading, erro e vazio** tratados na tela — nunca só o happy path.
