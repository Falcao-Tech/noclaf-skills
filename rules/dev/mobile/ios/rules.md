---
title: iOS / Swift — regras de stack
description: Específico de iOS/Swift. Aperta o baseline de mobile — SwiftUI + async/await, value types, sem force-unwrap, UI em @MainActor.
applies-to: mobile/ios
extends: ./rules.md
---

> Assume as regras gerais de mobile (`rules.md`). Aqui só o específico de **iOS / Swift**.

## Swift

- SwiftUI + `async/await`; nada de pirâmide de callback.
- `struct`/value types por padrão; `class` só quando precisa de referência/identidade.
- Opcional tratado explicitamente — sem force-unwrap (`!`) fora de teste.
- UI em `@MainActor`; trabalho pesado em `Task`/actor.

## Projeto

- Dependências via SPM; nada de lib não versionada.
- `AppDelegate`/`SceneDelegate` só com bootstrap — sem regra de negócio.
- Lógica testável no ViewModel (sem UIKit/SwiftUI) — teste sem renderizar tela.
