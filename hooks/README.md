# hooks

Hooks são **scripts + um gatilho** que o cliente de IA roda em eventos do seu ciclo
de vida (antes/depois de uma tool, no início de sessão, etc.). Diferente de skills e
commands — que são arquivos que o cliente lê sozinho de uma pasta — um hook só roda se
estiver **registrado no settings do cliente**. Copiar o script não basta.

Por isso cada pasta de role tem um manifesto `hooks.json` que **declara** o binding, e o
CLI (`@noclaf/mcp`) lê esse manifesto no `init`/`sync`, copia o script pra
`~/.claude/hooks/noclaf/<role>/` e registra o gatilho no `~/.claude/settings.json`.

## Layout

```
hooks/
  <role>/
    hooks.json            # manifesto: declara os bindings desta role
    <script>.py           # o script do hook
```

O `<role>` segue o mesmo modelo de seções das skills (`dev`, etc.): um hook em
`hooks/dev/` só é provisionado pra quem escolheu o perfil correspondente.

## Formato do `hooks.json`

```json
{
  "hooks": [
    {
      "id": 1,
      "event": "PreToolUse",
      "matcher": "Bash",
      "description": "O que o hook faz, quando dispara e como pular.",
      "script": "check-comment-length.py",
      "clients": ["claude-code"]
    }
  ]
}
```

| Campo         | Obrigatório | Descrição                                                                                              |
| ------------- | ----------- | ------------------------------------------------------------------------------------------------------ |
| `id`          | sim         | Inteiro sequencial estável (igual às skills) — chave de telemetria que sobrevive a renames.            |
| `event`       | sim         | Evento do ciclo de vida: `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, etc.                     |
| `matcher`     | não         | Regex do alvo do evento (ex.: `Bash`, `Write\|Edit`). Eventos sem alvo (ex.: `SessionStart`) omitem.    |
| `description` | sim         | O que o hook faz — usado no output do CLI.                                                              |
| `script`      | sim         | Nome do arquivo do script, relativo a esta pasta de role.                                               |
| `clients`     | sim         | Clientes que recebem o hook. Hoje só `claude-code`.                                                     |

## Notas

- **Escolha o evento certo pra intenção.** Pra **bloquear** uma ação, use `PreToolUse`
  (o hook roda antes e o `exit 2` cancela a tool). Em `PostToolUse` a tool já rodou —
  serve pra avisar/reagir, não pra impedir.
- O script é invocado como `python3 <caminho>`, então precisa de **`python3` no PATH**
  (o bit de execução é dispensável).
- O provisionamento é **não-destrutivo e idempotente**: o CLI só mexe nas entradas que
  ele mesmo criou (namespace `hooks/noclaf/`) no `settings.json` — hooks próprios do
  usuário ficam intactos. Renomear/remover um hook aqui remove a entrada correspondente
  no próximo `sync`.
