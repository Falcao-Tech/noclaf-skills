---
title: Android / Kotlin — regras de stack
description: Específico de Android/Kotlin. Aperta o baseline de mobile — Compose + Coroutines/Flow, null-safety, StateFlow, DI com Hilt.
applies-to: mobile/android
extends: ./rules.md
---

> Assume as regras gerais de mobile (`rules.md`). Aqui só o específico de **Android / Kotlin**.

## Kotlin

- Jetpack Compose + Coroutines/Flow; sem `AsyncTask` nem callback aninhado.
- `val` por padrão; `var` só quando muda. Null-safety explícito — sem `!!`.
- ViewModel expõe estado via `StateFlow`; a UI só coleta.
- IO/CPU em `Dispatchers.IO`/`Default`, nunca na main.

## Projeto

- DI (Hilt) em vez de singleton manual.
- Recursos (strings, dimens, cores) em `res/`, nunca hardcoded.
- Lógica testável no ViewModel (sem Android framework) — teste sem instrumentação.
