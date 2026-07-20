-- 002_reports_rls.sql — the tenant-owned table, isolated in the DATABASE, not
-- the app (Thursday). The wall an application bug — or a prompt injection —
-- cannot walk around.

create table reports (
  id         uuid primary key default gen_random_uuid(),
  tenant_id  uuid not null,
  author_id  uuid not null,
  title      text not null,
  body       text not null default '',
  shared     boolean not null default false,
  created_at timestamptz not null default now()
);

-- Enable RLS, and FORCE it so even the table owner is subject to the policy.
-- (Without FORCE, a superuser/owner connection silently bypasses RLS — the
-- exact footgun that produces "we had RLS but it still leaked" post-mortems.)
alter table reports enable row level security;
alter table reports force  row level security;

-- The policy: a request may only see/modify rows for the tenant currently set
-- on the connection via set_config('app.tenant_id', ...). If the setting is
-- absent it resolves to NULL and the comparison returns zero rows — fail closed.
create policy tenant_isolation on reports
  using      (tenant_id = current_setting('app.tenant_id', true)::uuid)
  with check (tenant_id = current_setting('app.tenant_id', true)::uuid);

-- CRITICAL: superusers (and BYPASSRLS roles) ignore RLS entirely, so migrations
-- and admin run above the wall — but request-time data access must NOT. We create
-- a non-superuser role and switch to it per request (see withTenant in db.ts), so
-- the policy actually applies. This is the exact footgun that makes RLS silently
-- fail open in production: the app connects as the DB owner and never notices.
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'app_user') then
    create role app_user nologin;
  end if;
end
$$;

grant usage on schema public to app_user;
grant select, insert, update, delete on reports to app_user;
grant insert on events to app_user;
grant usage, select on sequence events_id_seq to app_user;
