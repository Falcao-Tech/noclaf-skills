---
title: Django — regras de stack
description: Específico de Django/DRF. Aperta o baseline de back-end no ORM, camadas e config — nomear queryset pela entidade (nunca qs), fat services/thin views, N+1, paginação.
applies-to: back-end/django
extends: ./rules.md
---

> Assume as regras gerais de back-end (`rules.md`). Aqui só o específico de **Django**.

## ORM

- Nomeie o queryset pela **entidade**, nunca `qs` (`users = User.objects.filter(...)`).
- QuerySet reutilizável vive num **Manager/QuerySet customizado**, não repetido nas views.
- Sempre `select_related`/`prefetch_related` no que a view serializa — mate o N+1.
- Filtre no banco, não em Python; evite `.objects.all()` sem necessidade.
- Listagem pesada com `values()`/`only()` — não puxe colunas que não usa.

## Camadas

- **Fat services, thin views**: a view orquestra, o service tem a regra de negócio.
- Serializer/form só valida e (de)serializa — sem regra de negócio dentro.
- Operação multi-write dentro de `transaction.atomic`.

## Config

- `settings` por ambiente; nenhum segredo hardcoded.
- Paginação **default** no DRF (`DEFAULT_PAGINATION_CLASS`) — nunca listagem sem limite.
- Migration revisada e determinística; sem lógica de negócio dentro dela.
