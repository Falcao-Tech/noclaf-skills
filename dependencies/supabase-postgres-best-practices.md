---
title: Supabase — Postgres best practices
description: Skill oficial da Supabase (skills.sh) com boas práticas de Postgres/RLS. Reforça as rules de Lovable (Supabase/RLS).
repo: https://github.com/supabase/agent-skills
skills: supabase/agent-skills/supabase-postgres-best-practices
install: npx skills add supabase/agent-skills/supabase-postgres-best-practices
---

# Supabase — Postgres best practices

Skill **externa** (skills.sh), oficial da Supabase. Reforça `rules/front-end/lovable-rules.md`
na parte de dados — RLS em toda tabela, policies por operação, sem `service_role` no client.

> Instalador de linha única; a CLI oferece rodar no `init`/`sync`.

## Reforça

- `rules/front-end/lovable-rules.md` — segurança Supabase/RLS.
