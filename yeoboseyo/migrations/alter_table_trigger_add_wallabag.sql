alter table trigger add column wallabag bolean not null default 0 check (wallabag in (0,1))

