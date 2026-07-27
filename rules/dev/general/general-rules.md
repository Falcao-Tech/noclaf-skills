---
title: Regras gerais de código
description: Convenções que valem pra TODO código do repo, independente de área ou stack — tamanho, forma, clareza, higiene e boas práticas. É a camada raiz; front-end/back-end/mobile herdam estas.
applies-to: todo o código
extends: "—"
---

> Camada **raiz** — valem pra qualquer área/stack. Front-end, back-end e mobile herdam estas e só adicionam o que é específico delas.

## Tamanho e forma

- Arquivo com no máximo **300 linhas** — acima disso, quebre por responsabilidade.
- Função com no máximo **30 linhas** e um único nível de abstração.
- Comentário com no máximo **1 linha**; se precisa de parágrafo, o código não está claro o bastante.
- Prefira **early-return** a aninhar `if`/`else`.

## Boas práticas

- **Componentize/modularize sempre**: bloco repetido ou com responsabilidade própria vira componente/função/módulo.
- **DRY** — antes de escrever uma função/util, **verifique se já existe** algo global equivalente; reuse em vez de duplicar.
- **YAGNI** — implemente só o que o requisito atual pede; sem abstração/config "pro futuro".
- Uma função faz **uma coisa**; sem efeito colateral escondido.
- Composição em vez de herança quando der.

## Nomes e clareza

- Código (variáveis, funções, tipos, arquivos) em **inglês**; texto de UI no idioma do produto.
- Nomes descritivos, sem abreviação obscura (`user`, não `usr`).
- Sem número/string mágico — extraia pra constante nomeada.

## Higiene

- Sem código morto, import não usado ou log de debug commitado.
- Tipagem explícita na borda — sem `any`/tipo escapado.
- Um arquivo, uma responsabilidade principal.

## Erros e testes

- **Trate ou propague** o erro — nunca engula silenciosamente.
- Comportamento novo ou bug corrigido merece **teste**; teste o **contrato**, não a implementação.

## Critérios de review

Subconjunto **verificável no diff** das regras acima (o gate consome; o guia de implementação — DRY, YAGNI, composição — fica nas seções anteriores):

- [ ] Nenhum arquivo passa de **300 linhas**; nenhuma função passa de **30 linhas**.
- [ ] Nenhum comentário com mais de **1 linha**.
- [ ] Sem código morto, import não usado ou log de debug commitado.
- [ ] Sem `any`/tipo escapado na borda; tipagem explícita nas interfaces públicas.
- [ ] Sem número/string mágico — constantes nomeadas.
- [ ] Identificadores em inglês; texto de UI no idioma do produto.
- [ ] Erro tratado ou propagado — nunca engolido em silêncio.
- [ ] Comportamento novo ou bug corrigido acompanha teste de contrato.
