#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
novo_ciclo.py: prepara a atualização anual do site a partir do PDF do novo
Relatório de Autoavaliação Setorial (RSA).

O que faz (nada é publicado; tudo fica em trabalho/<ano>/ e em rascunhos na base):
  1. Extrai o texto do PDF página a página (pdfplumber; fallback pdftotext).
  2. Localiza as tabelas e quadros pelo TÍTULO e anota a página de cada um.
  3. Cria, se ainda não existirem, os rascunhos
       base_de_conhecimento/fontes_estruturadas/FONTE_RSA_<ano>.md
       base_de_conhecimento/RSA_<ano>_CPAR.md
     já com os cabeçalhos que scripts/gerar_dados.py espera.
  4. Imprime o roteiro de preenchimento (o que copiar de cada tabela).

Uso: python3 scripts/novo_ciclo.py --pdf caminho/Relatorio_CSA_CPAR_2026.pdf --ano 2026 [--drive-id ID]
"""
import argparse, pathlib, re, subprocess, sys, json, datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BASE = RAIZ / "base_de_conhecimento"

ap = argparse.ArgumentParser()
ap.add_argument("--pdf", required=True)
ap.add_argument("--ano", type=int, required=True)
ap.add_argument("--drive-id", default=None, help="ID do arquivo no Drive institucional (link publicado em cpar.ufms.br/avaliacao-institucional)")
ap.add_argument("--url", default=None, help="URL pública do PDF, se hospedado fora do Drive")
a = ap.parse_args()
pdf = pathlib.Path(a.pdf).expanduser().resolve()
if not pdf.exists(): sys.exit(f"PDF não encontrado: {pdf}")
ANO = a.ano
trab = RAIZ / "trabalho" / str(ANO); trab.mkdir(parents=True, exist_ok=True)
(RAIZ / "trabalho" / ".gitignore").write_text("*\n!.gitignore\n", encoding="utf-8")

# 1. texto por página
paginas = []
try:
    import pdfplumber
    with pdfplumber.open(str(pdf)) as doc:
        for i, pg in enumerate(doc.pages, 1):
            paginas.append(pg.extract_text() or "")
except Exception as e:
    print(f"pdfplumber indisponível ({e}); usando pdftotext")
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    paginas = txt.split("\f")
n = len(paginas)
(trab / "texto_completo.txt").write_text("\n".join(f"\n===== PÁGINA {i} =====\n{t}" for i, t in enumerate(paginas, 1)), encoding="utf-8")
print(f"1. {n} páginas extraídas para trabalho/{ANO}/texto_completo.txt")

# 2. tabelas e quadros por título
achados = []
padrao = re.compile(r"^\s*(Tabela|Quadro|Figura|Gráfico)\s+(\d+)\s*[\.\-:–]?\s*(.{5,120})$", re.I | re.M)
for i, t in enumerate(paginas, 1):
    for m in padrao.finditer(t):
        achados.append((m.group(1).title(), int(m.group(2)), m.group(3).strip(), i))
chaves = {"Adesão": r"ades", "Infraestrutura pela comunidade": r"infraestrutura", "Imagem pelos Estudantes": r"imagem.*estudante",
          "Imagem pelos Servidores": r"imagem.*servidor", "Processo pelos Estudantes": r"processo.*estudante", "Acompanhamento do plano": r"acompanhamento|plano de a"}
linhas = ["# Tabelas, quadros e figuras localizados por título", f"PDF: {pdf.name}, {n} páginas, extraído em {datetime.date.today().isoformat()}", "",
          "| Tipo | Nº | Título | Página |", "| --- | --- | --- | --- |"]
vistos = set()
for tipo, num, tit, pg in achados:
    k = (tipo, num, tit[:40])
    if k in vistos: continue
    vistos.add(k); linhas.append(f"| {tipo} | {num} | {tit} | {pg} |")
linhas += ["", "## Tabelas essenciais para o site (localizadas pelo título)", ""]
for nome, rx in chaves.items():
    hits = [(t, nu, ti, pg) for t, nu, ti, pg in achados if re.search(rx, ti, re.I)]
    linhas.append(f"- {nome}: " + ("; ".join(f"{t} {nu} p.{pg} ({ti[:60]})" for t, nu, ti, pg in hits[:4]) if hits else "NÃO LOCALIZADA, procurar manualmente"))
(trab / "tabelas_localizadas.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"2. {len(vistos)} títulos localizados em trabalho/{ANO}/tabelas_localizadas.md")

# 3. rascunhos na base
fonte = BASE / "fontes_estruturadas" / f"FONTE_RSA_{ANO}.md"
rsa = BASE / f"RSA_{ANO}_CPAR.md"
ref = f"`{pdf.name}`" + (f", Google Drive, ID `{a.drive_id}`" if a.drive_id else "") + (f", URL `{a.url}`" if a.url else "")
if not fonte.exists():
    fonte.write_text(f"""# FONTE PRIMÁRIA ESTRUTURADA — Relatório de Autoavaliação Setorial {ANO} do CPAR/UFMS

> **Fonte primaria**: {ref}.
> **Tipo**: Relatorio setorial anual do CPAR, ano base {ANO}. {n} paginas.
> **Data de extracao**: {datetime.date.today().strftime('%d %b %Y')}. **Metodo**: PDF extraido por scripts/novo_ciclo.py e conferido manualmente.
> **Regra**: cruzar por TITULO de tabela, nunca por numero. Percentuais e medias somente se impressos. Lacuna declarada, sem estimativa.

## Sumário do documento fonte

(colar o sumário)

## Lista de Tabelas do documento

(colar a lista de tabelas, com página)

## Lista de Quadros do documento

(colar a lista de quadros)

## 1. Rosto, composição e processo

(síntese: composição da CSA, metodologia, etapas e datas da coleta)

## 2. Unidade setorial: dados, planejamento e percepção

(síntese; incluir o quadro de acompanhamento das ações do plano anterior com contagem: concluídas, em andamento, não iniciadas, por responsável)

## 8. Apêndice de tabelas: contexto quantitativo

Padrão das tabelas: escala de 5 (Concordo totalmente) a 1 (Discordo totalmente), com NA/NQR/NSR. Nenhum valor estimado.

### TAB-01. Tabela N, Adesão em {ANO} (p. X)

{ANO}-1: diretora 0,0; coords 0,0; professores 0,0; estudantes 0,0 (Administração 0,00, Matemática 0,00, Medicina Veterinária 0,00, Psicologia 0,00); técnicos 0,0; total 0,00. {ANO}-2: professores 0,0; estudantes 0,0 (Administração 0,00, Matemática 0,00, Medicina Veterinária 0,00, Psicologia 0,00); total 0,00. Defeito: (se houver).

### TAB-02. Tabela N, Infraestrutura pela comunidade, 29 itens (p. X)

Aulas 0,00; Professores 0,00; Administrativas 0,00; Auditórios 0,00; Sanitárias 0,00; Informática 0,00; Internet 0,00; AVA 0,00; E-mail 0,00; Práticas 0,00; Convivência 0,00; Esportivos 0,00; Alimentação 0,00; Biblioteca 0,00; Acervo 0,00; Segurança 0,00; Iluminação 0,00; Acessibilidade 0,00; Limpeza 0,00; Parada 0,00; Estacionamento 0,00; Bicicletário 0,00; Vias 0,00; Telefonia 0,00; SISCAD 0,00; SIGPOS 0,00; Secretaria 0,00; Transporte 0,00; Secretaria qualidade 0,00 (percentuais na seção 2).

### TAB-03. Tabela N, Imagem pelos Estudantes (p. X)

Q1 0,00; Q2 0,00 (percentuais na seção 2).

### TAB-04. Tabela N, Imagem pelos Servidores (p. X)

Q1 0,00; Q2 0,00 (percentuais na seção 2).
""", encoding="utf-8")
    print(f"3. rascunho criado: {fonte.relative_to(RAIZ)}  (preencher os valores 0,00 com os da tabela; manter o formato 'Rótulo 9,99;')")
else:
    print(f"3. {fonte.relative_to(RAIZ)} já existe; não sobrescrito")
if not rsa.exists():
    rsa.write_text(f"""# Relatorio de Autoavaliacao Setorial {ANO} (RSA {ANO}) — CPAR/UFMS. Extracao com foco no banco historico

> **Fonte primaria**: {ref}.
> **Tipo**: Relatorio setorial anual do CPAR, ano base {ANO}. {n} paginas.
> **Data de extracao**: {datetime.date.today().strftime('%d %b %Y')}. **Metodo**: scripts/novo_ciclo.py + conferencia manual.

## Aviso de cobertura

(declarar o que foi e o que não foi extraído)

## 1. Composicao

(Direção, portaria da CSA, membros, metodologia, etapas)

## 2. Adesao {ANO}

(números absolutos e percentuais por segmento e por curso, com página)

## 3. Unidade

(auxílios, infraestrutura: fragilidades e oportunidades declaradas pelo relatório, imagem, questões abertas agregadas e anonimizadas)

## 4. Planos de acao

(acompanhamento do plano anterior e novos quadros SMART por responsável)

## 5. Balanco critico e consideracoes finais

(síntese)
""", encoding="utf-8")
    print(f"   rascunho criado: {rsa.relative_to(RAIZ)}")

# 4. roteiro
print(f"""
4. ROTEIRO DE PREENCHIMENTO (ano {ANO})
   a) FONTE_RSA_{ANO}.md, apêndice: preencher TAB-01 (adesão), TAB-02 (infraestrutura), TAB-03/04 (imagem)
      copiando os valores das tabelas localizadas em trabalho/{ANO}/tabelas_localizadas.md. Rótulos da infraestrutura
      devem seguir a lista curta (Aulas, Professores, ...); item novo: acrescentar ao fim e avisar.
   b) RSA_{ANO}_CPAR.md: síntese analítica (composição, adesão com absolutos, fragilidades declaradas, planos).
   c) dados/curados/planos_acao.json: atualizar 'acompanhamento' (totais e por_responsavel), 'smart_atual',
      'destaques_direcao', 'titulo_quadro', 'nota_infra_ciclo' e 'ano_ref' com o novo relatório.
   d) dados/curados/fragilidades_recorrentes.json: acrescentar a coluna "{ANO}" em cada tema, atualizar ciclos_fragil /
      ciclos_oport conforme a classificação do relatório e o 'status' com a ação vinculada.
   e) dados/curados/rupturas.json: registrar marcos do ano (greve, curso novo, mudança de instrumento) se houver.
   f) python3 scripts/gerar_dados.py --ano {ANO}   (acrescenta {ANO} nas séries de infraestrutura, imagem e adesão)
      depois completar em adesao_historica.json os absolutos (99/436) marcados 'a preencher'.
   g) tests/valores_ancora.json: acrescentar 4 a 6 âncoras do novo ano (adesão total, pior item, melhor item, ações).
   h) python3 scripts/validar.py; conferir as frases-síntese das páginas (index, ciclo, fragilidades, infraestrutura,
      adesao) e o alerta 'O que aconteceu em cada ano' da página de adesão.
""")
