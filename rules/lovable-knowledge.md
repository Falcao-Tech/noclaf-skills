## Stack obrigatória

- ShadcnUI + Tailwind
- TanStack Query v5 + Axios (instância customizada em src/services/api.ts)
- TanStack Form v1 + Zod (nunca usar a API v0)
- Zustand apenas para UI state global
- React Router v7
- date-fns, Sonner, Lucide React

## Regras de código

- TypeScript strict, zero uso de `any`
- Named exports em tudo, exceto pages
- Variáveis de ambiente sempre com prefixo VITE\_
- Nunca hardcodar URLs ou keys
- Todo conteúdo textual em português do Brasil — labels, placeholders, mensagens de erro, toasts e textos de UI

## Segurança

- RLS habilitado em todas as tabelas, sem exceção
- Nunca criar tabela sem policies para SELECT, INSERT, UPDATE e DELETE
- Nunca usar service_role key no frontend
- Auth state via onAuthStateChange + TanStack Query, nunca Zustand

## UI

- Usar ShadcnUI sempre que existir o componente
- Toasts apenas via Sonner
- Ícones apenas via Lucide React
- Cor primária #f5c738 usada exclusivamente em botões de ação principal
- Tema segue prefers-color-scheme por padrão
- Erros de validação de formulário devem aparecer abaixo do input correspondente, nunca como toast — usar o componente de erro do TanStack Form para isso
- Início (/overview): resumo do dia — aniversários, tarefas pendentes, horas
- Visão Geral (/dashboard): dashboard detalhado — presença online, horas por projeto, tarefas em andamento
- Gráficos: Recharts via componentes de Chart do ShadcnUI — nunca instalar outra lib de gráficos
- Seleção múltipla: Combobox do ShadcnUI (Command + Popover) — nunca criar MultiSelect customizado
