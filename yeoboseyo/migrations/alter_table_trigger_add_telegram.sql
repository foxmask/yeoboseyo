alter table trigger add column telegram bolean not null default 0 check (telegram in (0,1))

