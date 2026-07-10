---
id: 15
name: review-changes
description: Review de qualidade/limpeza do diff que vai ser commitado — higiene de comentários (destaque), além de duplicação, abstração, formatação e qualidade geral. Análise read-only via subagente; propõe correções, é consultiva (nunca bloqueia). Use antes de commitar/shipar, quando pedirem pra "revisar/limpar minhas mudanças" ou "checar excesso de comentário", ou quando invocada pelo /ship. NÃO é caça-bug — isso é o /code-review.
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent
---

Revise as **mudanças prestes a serem commitadas** buscando qualidade e limpeza — **não** bugs de correção (isso é o `/code-review`). Só qualidade.

## Escopo
- Padrão: o diff a ser commitado — **mudanças staged + unstaged em arquivos trackeados**, mais o diff do branch vs a base (`main`/`master`/`dev`) quando você está num branch de feature/fix. Ignore lixo untracked, arquivos gerados, dependências, `.env*`.
- Um argumento de path estreita o escopo pra aquele path.

## Procedimento
1. **Delegue a leitura a um subagente read-only.** Spawne um agente `Explore` (ou read-only) sobre o diff + o código imediatamente ao redor, com os critérios abaixo. Ele **não pode editar** — só retorna achados. Isso mantém a análise fora do contexto do chamador e não-destrutiva. Peça que retorne cada achado como: `severidade` · `arquivo:linha` · `o quê` · `porquê` · `correção sugerida`.
2. **Apresente** os achados agrupados por severidade, **excesso de comentário primeiro**, depois duplicação / abstração / formatação / qualidade. Seja enxuto — sem encher linguiça; se o diff está limpo, diga isso em uma linha.
3. **Aplique só o que for aprovado.** Comentários + limpezas triviais → ofereça aplicar em lote. Qualquer coisa substantiva (mudança de abstração real / refactor) → descreva e deixe o usuário decidir. **Consultivo — nunca bloqueia.**
4. Se as correções aplicadas mexeram em código, avise que lint/build devem ser rodados de novo.

## Critérios (ordem de prioridade)

### 1. Higiene de comentários — o destaque (código gerado por LLM comenta demais)
**Sinalize pra deletar:** comentários que repetem o código; narração de passos óbvios (`// loop over users`); comentários que descrevem a *mudança/diff* (`// Added to handle X`, `// Now also does Y`); prosa tutorial; código comentado; docstrings que só ecoam uma assinatura auto-evidente.
**Mantenha:** o **porquê** não-óbvio; invariantes, pegadinhas, footguns; racional de perf/segurança; refs externas (ticket/spec/RFC); contratos de API pública.
**Limite de tamanho (duro):** todo comentário que sobreviver ≤ **2 linhas**. Descrições de função/método ≤ **3 linhas** de prosa, e só quando o *porquê* realmente precisar — linhas de param/return/type/example não contam nas 3. Acima do limite → sinalize pra **encurtar**, não pra manter.
**Teste:** um comentário só se justifica se um leitor esperto não conseguiria inferi-lo do código + bons nomes. **Padrão: nenhum.**

### 2. Duplicação
Copy-paste, gêmeos estruturais, reimplementar um util que já existe. Dedup profunda → sugira `/drytify`.

### 3. Abstração
Abstração prematura/vazada; um wrapper que não agrega nada; a costura errada. Também o inverso — um bloco cabeludo que genuinamente pede um helper nomeado.

### 4. Formatação
Inconsistente com o arquivo ao redor / o formatter do repo. Prefira rodar o formatter do repo a editar na mão.

### 5. Qualidade geral
Código morto, vars/imports não usados, nomes enganosos, ineficiência óbvia nas linhas **alteradas**.

### 6. Idioma do código (código = inglês)
Convenção do projeto: **código se escreve em inglês** — nomes de variáveis, funções, classes, tipos, comentários no código, mensagens de commit e strings de log/erro voltadas ao dev. **Skills, commands e docs são em pt-BR** (pra clareza do time brasileiro).
**Sinalize pra traduzir pro inglês** qualquer código escrito em português: identificadores (`calcularTotal` → `calculateTotal`), comentários em pt dentro do código, nomes de arquivo de código em pt. **NÃO sinalize:** strings voltadas ao usuário final (UI/mensagens do produto — seguem o idioma do produto); nem conteúdo de skills/commands/docs/specs (esse é pt-BR de propósito).
**Teste rápido:** é identificador, símbolo ou comentário técnico → é **código** → inglês. É prosa explicativa pra humano (doc, skill, command, spec) → **pt-BR**.

## Regras
- **Só qualidade** — não reporte bugs de correção/segurança aqui; se achar um de verdade, mencione em uma linha e aponte pro `/code-review`, não corrija.
- **Combine com o código ao redor** — as convenções dele ganham de ideais genéricos.
- **Consultivo** — proponha; aplique só o aprovado; nunca bloqueie o ship.
- Fique dentro do diff — não faça gold-plating nem alargue o escopo.
