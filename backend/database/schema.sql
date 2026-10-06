CREATE TABLE IF NOT EXISTS organizations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sectors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  organization_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_sectors_organization_id ON sectors (organization_id);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  senha_hash TEXT NOT NULL,
  curso TEXT,
  classe TEXT,
  xp INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  organization_id INTEGER REFERENCES organizations (id) ON DELETE RESTRICT,
  sector_id INTEGER REFERENCES sectors (id) ON DELETE RESTRICT,
  role TEXT CHECK (role IS NULL OR role IN ('manager', 'collaborator'))
);

CREATE TABLE IF NOT EXISTS professional_profiles (
  user_id INTEGER PRIMARY KEY,
  biografia TEXT,
  objetivo_profissional TEXT,
  tecnologias_favoritas TEXT,
  github TEXT,
  linkedin TEXT,
  portfolio TEXT,
  cidade TEXT,
  estado_regiao TEXT,
  disponivel_estagio INTEGER,
  curriculo_path TEXT,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS initial_disc_results (
  user_id INTEGER PRIMARY KEY,
  d_score INTEGER NOT NULL,
  i_score INTEGER NOT NULL,
  s_score INTEGER NOT NULL,
  c_score INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS missions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mission_key TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL,
  descricao TEXT NOT NULL,
  xp_recompensa INTEGER NOT NULL,
  ordem INTEGER NOT NULL,
  tipo_evento TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_missions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  mission_key TEXT NOT NULL,
  nome TEXT NOT NULL,
  descricao TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'Pendente',
  xp_recompensa INTEGER NOT NULL,
  data_conclusao TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id),
  UNIQUE (user_id, mission_key)
);

CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  titulo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  tecnologias TEXT NOT NULL,
  link TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS certificates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  nome TEXT NOT NULL,
  instituicao TEXT NOT NULL,
  carga_horaria INTEGER NOT NULL,
  data_conclusao TEXT NOT NULL,
  arquivo_path TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS achievement (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  achievement_key TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL,
  descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_achievement (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  achievement_key TEXT NOT NULL,
  data_desbloqueio TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (achievement_key) REFERENCES achievement (achievement_key),
  UNIQUE (user_id, achievement_key)
);

CREATE TABLE IF NOT EXISTS evolution_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  event_key TEXT NOT NULL,
  event_type TEXT NOT NULL,
  titulo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id),
  UNIQUE (user_id, event_key)
);

CREATE TABLE IF NOT EXISTS observed_disc_results (
  user_id INTEGER PRIMARY KEY,
  d_observed INTEGER NOT NULL DEFAULT 0,
  i_observed INTEGER NOT NULL DEFAULT 0,
  s_observed INTEGER NOT NULL DEFAULT 0,
  c_observed INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
