-- Esquema do banco de dados historico do CPAR para o site da CSA/CPAR
-- Banco alvo: SQLite (compativel com Postgres com ajustes minimos de tipos)
-- Codificacao: UTF-8. CSVs de carga: delimitador ; e utf-8-sig
-- Regra de serie: cruzar por TITULO de tabela ou figura, nunca por numero. Regra do trienio: 2018 a 2020 rendeu somente o recorte 2020. 2017 e lacuna declarada.

PRAGMA foreign_keys = ON;

CREATE TABLE documento (
  id INTEGER PRIMARY KEY,
  ano_ref INTEGER NOT NULL,
  periodo TEXT NOT NULL DEFAULT 'anual' CHECK (periodo IN ('anual','2020-1','2020-2','2021-1','2021-2','parcial','recorte','trienal')),
  tipo TEXT NOT NULL CHECK (tipo IN ('anual','parcial','trienal','recorte')),
  titulo TEXT NOT NULL,
  paginas INTEGER,
  data_aprovacao TEXT,
  drive_id TEXT,
  arquivo_md TEXT NOT NULL,
  cobertura TEXT,
  metodo TEXT DEFAULT 'viewer via DOM acessivel (download bloqueado)'
);

CREATE TABLE gestao (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  nivel TEXT NOT NULL CHECK (nivel IN ('CPAR','UFMS Central','CPA','SEAVI')),
  cargo TEXT NOT NULL,
  nome TEXT NOT NULL,
  portaria_ref TEXT,
  pagina INTEGER
);

CREATE TABLE adesao (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  periodo TEXT NOT NULL DEFAULT 'anual',
  unidade TEXT NOT NULL,
  segmento TEXT NOT NULL,
  valor_pct REAL,
  posicao_rank INTEGER,
  qualidade TEXT NOT NULL DEFAULT 'definitivo' CHECK (qualidade IN ('definitivo','estimativa_visual','parcial','ausente')),
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT,
  observacao TEXT
);

CREATE TABLE oferta_curso (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_psu INTEGER NOT NULL,
  curso TEXT NOT NULL,
  unidade TEXT NOT NULL DEFAULT 'CPAR',
  ingresso_sem TEXT,
  turno TEXT,
  vagas INTEGER,
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT
);

CREATE TABLE visita_inloco (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_visita INTEGER NOT NULL,
  unidade TEXT NOT NULL,
  curso TEXT NOT NULL,
  data_visita TEXT,
  ato TEXT,
  dim1 REAL,
  dim2 REAL,
  dim3 REAL,
  conceito_final INTEGER,
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT
);

CREATE TABLE enade_curso (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_enade INTEGER NOT NULL,
  curso TEXT NOT NULL,
  unidade TEXT NOT NULL,
  modalidade TEXT,
  inscritos INTEGER,
  participantes INTEGER,
  nota_fg_bruta REAL,
  nota_fg_pad REAL,
  nota_ce_bruta REAL,
  nota_ce_pad REAL,
  conceito_enade_cont REAL,
  conceito_enade_faixa INTEGER,
  cpc_cont REAL,
  cpc_faixa INTEGER,
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT
);

CREATE TABLE clinica_atendimento (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  total INTEGER,
  feminino INTEGER,
  masculino INTEGER,
  adulto INTEGER,
  adolescente INTEGER,
  crianca INTEGER,
  pre_agendado INTEGER DEFAULT 0 CHECK (pre_agendado IN (0,1)),
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT,
  observacao TEXT
);

CREATE TABLE patrimonio (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  terreno_m2 REAL,
  construida_m2 REAL,
  valor_terreno REAL,
  valor_benfeitorias REAL,
  valor_total REAL,
  pct_ufms REAL,
  fonte TEXT,
  pagina INTEGER,
  titulo_tabela TEXT
);

CREATE TABLE escala_ufms (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  grad_pres INTEGER,
  grad_ead INTEGER,
  stricto_cursos INTEGER,
  lato_cursos INTEGER,
  residencias INTEGER,
  estudantes_total INTEGER,
  fonte TEXT,
  pagina INTEGER,
  observacao TEXT
);

CREATE TABLE observacao (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  tema TEXT NOT NULL,
  texto TEXT NOT NULL,
  pagina INTEGER
);

CREATE TABLE lacuna (
  id INTEGER PRIMARY KEY,
  documento_id INTEGER NOT NULL REFERENCES documento(id),
  ano_ref INTEGER NOT NULL,
  item TEXT NOT NULL,
  motivo TEXT NOT NULL
);

-- Indices para as consultas do site
CREATE INDEX idx_adesao_ano_unidade ON adesao(ano_ref, unidade, segmento);
CREATE INDEX idx_clinica_ano ON clinica_atendimento(ano_ref);
CREATE INDEX idx_enade_curso_ano ON enade_curso(ano_enade, unidade, curso);
CREATE INDEX idx_visita_ano ON visita_inloco(ano_visita, unidade);

-- Carga inicial de documentos da serie 2014 a 2025 (2017 ausente)
INSERT INTO documento (id, ano_ref, periodo, tipo, titulo, paginas, data_aprovacao, drive_id, arquivo_md, cobertura) VALUES
(1, 2014, 'anual', 'anual', 'Relatorio ano base 2014', 281, NULL, '1RbvTY65r3kjmF9rJlFuiuFXhP9BBV8WS', 'RAAI_2014_UFMS.md', 'parcial e seletiva'),
(2, 2015, 'parcial', 'parcial', 'Relatorio parcial 2015', 39, NULL, '1ccxj_BUmcQjCtNdUAQXb0DOFDBUGLVDJ', 'RAAI_2015_UFMS.md', 'integral do texto relevante, figuras sem tabela como lacuna'),
(3, 2016, 'parcial', 'parcial', 'Relatorio parcial 2016', 39, NULL, '1vXtz7jj8K5D-qKJbyPm1GARAfnilj7ss', 'RAAI_2016_UFMS.md', 'seletiva, valores de figuras como estimativa visual'),
(4, 2018, 'anual', 'anual', 'RAAI 2018', 544, '2019-03-13', '1H3G1uVVRs8bQO1yQTCE1Bqxx4azAhkrv', 'RAAI_2018_UFMS.md', 'seletiva'),
(5, 2019, 'anual', 'anual', 'RAAI 2019', 525, '2020-03-03', '1_3RhRFSlKSAIvEXH24YIjRW0xliohEY0', 'RAAI_2019_UFMS.md', 'seletiva'),
(6, 2020, 'recorte', 'recorte', 'Trienio 2018-2020 recorte 2020', 762, '2021-03-15', '1CJdQcwI3lW-gjhndrNc1xja4Z-CBJ_Gd', 'RAAI_2020_UFMS.md', 'seletiva do intervalo 2020'),
(7, 2021, 'anual', 'anual', 'RAAI 2021', 336, '2022-03-21', '1zT6Tqg4en6CociBpgj9akEmLRYDqHIGS', 'RAAI_2021_UFMS.md', 'seletiva'),
(8, 2022, 'anual', 'anual', 'RAAI 2022', 82, '2023-03-21', '1pJR_tPLIt5mbNS0rZjvUBMWgm_6UEGCM', 'RAAI_2022_UFMS.md', 'cerca de 70 pct'),
(9, 2023, 'anual', 'anual', 'RAAI 2023', 102, '2024-03-25', '1UUAYjIFBBK3YV9z2QWanMDiN4nQFMkMH', 'RAAI_2023_UFMS.md', 'cerca de 60 pct'),
(10, 2024, 'anual', 'anual', 'RAAI 2024', 112, '2025-03-27', '17wYpOdpldDD49xHe1aJQTeGYKtoxWs3N', 'RAAI_2024_UFMS.md', 'cerca de 65 pct'),
(11, 2025, 'anual', 'anual', 'RAAI 2025', NULL, NULL, NULL, 'RAAI_2025_UFMS.md', 'padrao da serie');

-- Exemplos de carga com achados ja validados (amostra, restante via CSV)
-- Adesao CPAR media geral: 2018 58.81, 2019 49.7, 2020-1 42.3, 2020-2 37.1, 2021-1 37.9, 2021-2 48.3, 2022 43.08, 2023 48.68, 2024 26.77
-- Clinica: 2018 211, 2019 163, 2020 2 mais 15 pre, 2021 209
