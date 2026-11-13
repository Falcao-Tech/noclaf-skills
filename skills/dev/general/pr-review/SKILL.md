---
id: 44
name: pr-review
description: Review de PR com veredito — lê o diff E o código que ele toca, confere contra o harness do repo e os critérios do ticket, classifica cada achado por severidade (crítico, alto, médio, baixo) e aprova só sem crítico nem alto. Read-only. É a skill do Lorem, o revisor de código do turno da noite, e serve para qualquer revisão de PR que precise de veredito. Use quando pedirem "revisa esse PR", "faz o code review" ou quando o Lorem pegar uma parte em code_review.
effort: high
allowed-tools: Bash, Read, Grep, Glob
---

# PR Review

Você revisa um PR já aberto e devolve **um veredito**. Não edita, não commita, não comenta no
GitHub, não escreve no NOS: quem consome o veredito é o worker (ou quem chamou a skill).

Base: o `pr-reviewer` do harness Noclaf (diff + base + ticket). Severidade, checklists de segurança e
desempenho adaptados de [everything-claude-code](https://github.com/worldflowai/everything-claude-code)
(MIT), trazidos para as stacks e os limites da Noclaf.

## 1. Carregue o contexto, nesta ordem

1. **O ticket**: o briefing recebido (título, descrição, critérios de aceitação, Roteiro de QA,
   **Fora de escopo**). Sem briefing → corpo do PR ou `nos_get_task`.
2. **O diff**: `git diff <base>...HEAD` (base = branch de destino do PR).
3. **A base tocada**: leia **por inteiro** cada arquivo alterado no estado atual. Onde o diff muda
   assinatura, contrato, schema ou invariante, procure os call-sites (Grep) e leia o suficiente para
   julgar se ainda casam. É aqui que um revisor de diff sozinho erra.
4. **O harness**: `docs/_review.md`; se faltar, `docs/_rules/noclaf.md` + `docs/_patterns.md` +
   `AGENTS.md`. As regras do repo mandam sobre esta skill.
5. **Os handoffs** das dependências, se vieram no briefing: o PR precisa consumir o contrato que a
   parte anterior entregou.

## 2. Guards mecânicos (sem julgamento)

Conte no conjunto alterado: arquivo ≤ 300 linhas, função ≤ 30 linhas, comentário novo ≤ 3 linhas.
Rode os gates do repositório que existirem (lint, typecheck, testes). Violação ou gate vermelho é
achado **ALTO**.

## 3. Revise por categoria

### Correção e integração
- Faz o que os critérios de aceitação pedem? Cada critério é verificável no diff ou num teste?
- Contrato alterado com todos os call-sites atualizados; invariante do módulo preservada.
- Consome o que o handoff da dependência entregou (campos, rota, formato), sem inventar parâmetro.
- Tratamento de erro nos caminhos novos; estado vazio e nulo.

### Escopo
- Nada do **Fora de escopo** do ticket; nada além do pedido (refactor não solicitado, dependência
  nova, mudança de CI, migration em ticket que não pede).

### Segurança
- Segredo, token ou senha no código ou em arquivo versionado.
- Consulta montada por concatenação (SQL cru, `extra()`, `raw()` com f-string); filtro de ORM
  vindo direto do request sem whitelist.
- Permissão: rota nova sem a classe de permissão do repo, `view_name` ausente, objeto de outro
  projeto/cliente acessível (IDOR), dado interno exposto para cliente.
- Entrada não validada (serializer sem campos explícitos, `__all__`); upload e caminho de arquivo
  controlados pelo usuário (path traversal).
- Front: HTML não escapado vindo de dado do usuário (XSS), token em `localStorage` quando o repo usa cookie.

### Desempenho
- Consulta dentro de loop (N+1); listagem sem `select_related`/`prefetch_related` onde o padrão do
  repo exige; contagem de consultas que cresce com o volume.
- Algoritmo quadrático onde há estrutura melhor (busca em lista dentro de loop, sort repetido).
  Dúvida sobre estrutura ou complexidade → aplique a skill `dsa-optimization`.
- Front: re-render ou requisição repetida evitável.

### Qualidade
- Padrões do repo (`docs/_patterns.md`): onde o código novo deveria reusar algo que já existe.
- Nomes, duplicação, abstração prematura, código morto, `print`/`console.log` esquecido.
- Teste: comportamento novo sem teste quando o repo tem suíte e o Roteiro de QA marca `[auto]`.

## 4. Classifique cada achado

| Severidade | Quando | Efeito |
|---|---|---|
| **CRÍTICO** | Falha de segurança, perda ou corrupção de dado, quebra de contrato usado em produção | Bloqueia |
| **ALTO** | Critério de aceitação não atendido, fora de escopo, gate vermelho, guard mecânico, N+1 em listagem, call-site quebrado | Bloqueia |
| **MÉDIO** | Padrão do repo não seguido, teste faltando onde não é `[auto]`, erro não tratado em caminho raro | Não bloqueia |
| **BAIXO** | Nome, legibilidade, sugestão | Não bloqueia |

Na dúvida entre dois níveis, escolha o mais baixo e diga por quê. Gosto pessoal não é achado.

## 5. Veredito

- `approved`: nenhum CRÍTICO nem ALTO.
- `changes_requested`: um ou mais CRÍTICO ou ALTO.

## 6. Saída

Primeiro o relatório, um achado por linha, os bloqueantes primeiro:

```
[ALTO] core/modules/x/view.py:42 — rota nova sem view_name; qualquer interno acessa — adicionar view_name e registrar no conftest
```

Formato: `[SEVERIDADE] arquivo:linha — o que está errado — o que fazer`. Quem corrige é outro bot,
à noite, sem ninguém para perguntar: o "o que fazer" precisa ser executável sem contexto.

Por último, **uma linha só** com o JSON que o worker lê:

```json
{"verdict": "approved|changes_requested", "reasons": "os bloqueantes, um por linha", "notes": "médios e baixos, resumidos"}
```

## Nunca

Editar arquivo, commitar, dar push, comentar ou aprovar no GitHub, dar merge, rodar migration,
escrever no NOS.
