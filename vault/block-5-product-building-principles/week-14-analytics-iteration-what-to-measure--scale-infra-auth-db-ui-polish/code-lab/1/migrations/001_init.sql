-- 001_init.sql — accounts (tenants), users, sessions, and the analytics event log.
-- Ordered, versioned, reviewed, reversible: never hand-edit prod schema (Friday).

create table accounts (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  created_at timestamptz not null default now()
);

create table users (
  id            uuid primary key default gen_random_uuid(),
  account_id    uuid not null references accounts(id),
  email         text not null unique,
  password_hash text not null,          -- scrypt(salt:hash); never plaintext
  role          text not null default 'member',  -- 'owner' | 'admin' | 'member'
  created_at    timestamptz not null default now()
);

-- Opaque server-side sessions. We store the SHA-256 of the token, never the
-- token itself, so a DB dump cannot be replayed as a login (Thursday).
create table sessions (
  token_hash text primary key,
  user_id    uuid not null references users(id),
  expires_at timestamptz not null
);

-- The analytics event log (Tuesday's Object-Action taxonomy). Every event
-- carries account_id AND user_id AND request_id so the two pipes can join.
create table events (
  id         bigserial primary key,
  name       text not null,            -- ReportGenerated | ReportShared | ...
  account_id uuid not null,
  user_id    uuid not null,
  request_id uuid not null,
  props      jsonb not null default '{}',
  created_at timestamptz not null default now()
);

create index events_name_created_idx on events (name, created_at);
