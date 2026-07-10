anStack Query, nunca Zustand

## UI

- Usar ShadcnUI sempre que existir o componente
- Toasts apenas via Sonner
- Ícones apenas via Lucide React
- Tema segue `prefers-color-scheme` por padrão
- Nunca usar valores de estilo hardcoded (cores, espaçamentos, tamanhos) — usar os tokens da escala do Tailwind; valores arbitrários só quando explicitamente pedido
- Layout mobile-first usando os breakpoints e a escala do Tailwind
- Erros de validação de formulário aparecem abaixo do input correspondente, nunca como toast — usar o componente de erro do TanStack Form
- Estados vazios (empty states) sempre tratados, com mensagem e ação quando fizer sentido
- Ações destrutivas confirmadas via AlertDialog do ShadcnUI — nunca `window.confirm`
- Datas formatadas com date-fns e locale pt-BR
- Gráficos: Recharts via componentes de Chart do ShadcnUI — nunca instalar outra lib de gráficos
- Seleção múltipla: Combobox do ShadcnUI (Command + Popover) — nunca criar MultiSelect customizado

## API e roteamento

- Base URL via `VITE_API_URL`; token e tratamento de erro centralizados em interceptors do Axios em `src/services/api.ts`
- Pages carregadas com lazy loading; rotas protegidas por um wrapper de auth

## Stack obrigatória

- ShadcnUI + Tailwind
- TanStack Query v5 + Axios (instância customizada em `src/services/api.ts`)
- TanStack Form v1 + Zod (nunca usar a API v0)
- Zustand apenas para UI state global
- date-fns, Sonner, Lucide React

## Regras de código

- TypeScript strict, zero uso de `any`
- Named exports em tudo, exceto pages
- Variáveis de ambiente sempre com prefixo `VITE_`
- Nunca hardcodar URLs ou keys
- Formatação (datas, números, moeda) sempre via utilitários compartilhados em `src/utils/` — nunca reimplementar inline
- Todo conteúdo textual em português do Brasil — labels, placeholders, mensagens de erro, toasts e textos de UI
- Todo arquivo, váriavel ou valor deve ser em inglês, enquanto mensagens, status, sonners e valores, em português.

## Nomes e arquivos

- Componentes em PascalCase, um por arquivo (`UserCard.tsx`)
- Hooks em camelCase com prefixo `use` (`useUsuarios.ts`); utilitários em camelCase (`formatarData.ts`)
- Tipos e interfaces em PascalCase; schemas Zod com sufixo `Schema`
- Imports internos sempre via alias `@/` — nunca caminhos relativos longos (`../../../`)
- Pages com default export em `src/pages/`; todo o resto com named export

## Componentização

- Nunca criar componentes muito grandes, com limite de 400 linhas por arquivo — extraia em arquivos separados em `src/components/`, sempre em `.tsx`
- Formulários sempre em componente próprio, separado da page
- Mensagens de erro do formulário sempre generalizadas dentro de `src/utils/schema-messages`, como exemplo: `INVALID_TYPE: 'O tipo do campo é inválido.'`.
- Nunca colocar chamadas de API direto no componente — toda query é um hook em `src/hooks/query/` usando TanStack Query. Fetch no Server Side, e useQuery no ClientSide.

## Dados e formulários

- Query keys padronizadas em factory (`['usuarios', id]`) — nunca strings soltas
- Mutations invalidam as queries afetadas no `onSuccess`
- Todo fetch trata loading e error — loading com Skeleton do ShadcnUI, nunca spinner caseiro
- Schema Zod é a fonte de verdade; tipos derivados com `z.infer`, nunca duplicados à mão

## Segurança

- RLS habilitado em todas as tabelas, sem exceção
- Nunca criar tabela sem policies para SELECT, INSERT, UPDATE e DELETE
- Nunca usar service_role key no frontend
- Auth state via `onAuthStateChange` + T
