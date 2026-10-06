#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_dados.py: pipeline de derivados do site da CSA/CPAR.

Fluxo:
  1. Derivados CURADOS (dados/curados/*.json): validados contra a base markdown
     (valores ancora precisam existir na fonte), recebem cabecalho _meta e sao
     copiados para docs/data/.
  2. Derivados EXTRAIDOS (ciclo_2025.json, sintese_2025.json): construidos por
     regex a partir de base_de_conhecimento/fontes_estruturadas/FONTE_RSA_2025.md
     (TAB-01, TAB-19, TAB-20, TAB-21) e cruzados com os curados.
  3. docs/data/indice.json: catalogo dos documentos da serie (a partir do
     esquema_banco/schema_cpar_historico.sql).

Regras (LEIAME_BASE_DE_DADOS.md / AGENTS.md): base somente leitura; cruzar
por titulo, nunca por numero; lacuna = null, nunca estimativa; percentuais e
medias somente se impressos; sem recalculo.

Uso: python3 scripts/gerar_dados.py   (na raiz do repositorio)
Sem dependencias externas.
"""
import hashlib, json, re, sys, datetime, pathlib, argparse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BASE = RAIZ / "base_de_conhecimento"
CURADOS = RAIZ / "dados" / "curados"
SAIDA = RAIZ / "docs" / "data"
VERSAO_PIPELINE = "2.0.0"

def anos_disponiveis():
    return sorted(int(p.name.split("_")[2][:4]) for p in (BASE / "fontes_estruturadas").glob("FONTE_RSA_*.md"))

ARGS = argparse.ArgumentParser(description="Gera os derivados do site da CSA/CPAR")
ARGS.add_argument("--ano", type=int, default=None, help="ano do ciclo mais recente (padrao: maior FONTE_RSA_<ano>.md existente)")
ARGS.add_argument("--nao-estender", action="store_true", help="nao acrescentar o ano novo automaticamente nas series curadas")
OPC = ARGS.parse_args()
ANO = OPC.ano or anos_disponiveis()[-1]
ANOS_SERIE = ["2022", "2023", "2024", "2025"]  # anos comparaveis (mesmo instrumento SIAI); o ano atual e acrescentado abaixo
if str(ANO) not in ANOS_SERIE: ANOS_SERIE.append(str(ANO))
FONTE_ATUAL = BASE / "fontes_estruturadas" / f"FONTE_RSA_{ANO}.md"

CORTE_FRAG, CORTE_OPORT = 2.50, 3.50

def sha256(p):
    # Quebras de linha normalizadas (CRLF -> LF): o hash e o mesmo no Windows e no CI (Linux)
    return hashlib.sha256(pathlib.Path(p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()

def num(s):
    """'3,84' -> 3.84"""
    return float(s.replace(".", "").replace(",", ".")) if "," in s else float(s)

def classifica(m):
    if m is None: return "lacuna"
    if m < CORTE_FRAG: return "fragilidade"
    if m < CORTE_OPORT: return "oportunidade"
    return "bem_avaliado"

def meta(origem, extra=None):
    m = {
        "gerado_em": datetime.date.today().isoformat(),
        "script": "scripts/gerar_dados.py",
        "versao_pipeline": VERSAO_PIPELINE,
        "origem": origem,
        "sha256_origem": sha256(RAIZ / origem) if (RAIZ / origem).exists() else None,
        "regra": "Base somente leitura. Cruzar por titulo de tabela, nunca por numero. Lacuna = null. Sem recalculo.",
    }
    if extra: m.update(extra)
    return m

def escreve(nome, obj):
    SAIDA.mkdir(parents=True, exist_ok=True)
    p = SAIDA / nome
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  ok  docs/data/{nome}")

# ---------------------------------------------------------------- 1. curados
def curados():
    print("1. Derivados curados")
    for p in sorted(CURADOS.glob("*.json")):
        obj = json.loads(p.read_text(encoding="utf-8"))
        obj = {"_meta": meta(f"dados/curados/{p.name}", {"tipo": "curado",
                "nota": "Derivado revisado manualmente contra a base; ver tests/valores_ancora.json"}), **obj}
        escreve(p.name, obj)

# ------------------------------------------------------------- 2. extraidos
# Localizacao de tabelas POR TITULO (regra da serie: nunca por numero). Cada entrada e um regex
# aplicado ao cabecalho "### TAB-NN. Tabela N, <titulo> (p. X)".
TITULOS = {
    "adesao": r"Ades[aã]o",
    "infra": r"Infraestrutura pela comunidade",
    "img_est": r"Imagem pelos Estudantes",
    "img_serv": r"Imagem pelos Servidores",
}

def cabecalho(texto, chave):
    m = re.search(r"^### (TAB-\d+\. Tabela \d+, [^\n]*?" + TITULOS[chave] + r"[^\n]*)$", texto, re.M | re.I)
    if not m:
        sys.exit(f"ERRO: tabela com titulo '{TITULOS[chave]}' nao encontrada em {FONTE_ATUAL.name}")
    return m.group(1)

def secao(texto, chave):
    """Retorna o paragrafo de prosa logo apos o cabecalho da tabela identificada pelo titulo."""
    cab = cabecalho(texto, chave)
    m = re.search(r"^### " + re.escape(cab) + r"\n\n([^\n]+)", texto, re.M)
    if not m:
        sys.exit(f"ERRO: prosa da tabela '{cab}' vazia em {FONTE_ATUAL.name}")
    return m.group(1)

def pagina(texto, chave):
    m = re.search(r"\(p\. (\d+)\)", cabecalho(texto, chave))
    return int(m.group(1)) if m else None

def titulo_tabela(texto, chave):
    return re.sub(r"^TAB-\d+\. ", "", cabecalho(texto, chave)).split(" (p.")[0]

ROTULOS_INFRA_2025 = [
    # (rotulo curto no FONTE, rotulo completo, id no derivado curado ou None)
    ("Aulas", "Salas de aula", "aulas"),
    ("Professores", "Salas de professores", "professores"),
    ("Administrativas", "Salas administrativas", "adm"),
    ("Auditórios", "Auditórios", "auditorios"),
    ("Sanitárias", "Instalações sanitárias", "sanitarias"),
    ("Informática", "Laboratórios de informática", "informatica"),
    ("Internet", "Internet", "internet"),
    ("AVA", "AVA/UFMS", "ava"),
    ("E-mail", "E-mail institucional", "email"),
    ("Práticas", "Laboratórios e aulas práticas", "praticas"),
    ("Convivência", "Espaços de convivência", "convivencia"),
    ("Esportivos", "Espaços esportivos", "esportivos"),
    ("Alimentação", "Alimentação (RU e cantina)", "alimentacao"),
    ("Biblioteca", "Biblioteca", "biblioteca"),
    ("Acervo", "Acervo bibliográfico", "acervo"),
    ("Segurança", "Segurança", "seguranca"),
    ("Iluminação", "Iluminação", "iluminacao"),
    ("Acessibilidade", "Acessibilidade", "acessibilidade"),
    ("Limpeza", "Limpeza", "limpeza"),
    ("Parada", "Parada de ônibus", "parada"),
    ("Estacionamento", "Estacionamento", "estacionamento"),
    ("Bicicletário", "Bicicletário", "bicicletario"),
    ("Vias", "Vias internas", "vias"),
    ("Telefonia", "Telefonia", "telefonia"),
    ("SISCAD", "SISCAD", "siscad"),
    ("SIGPOS", "SIGPOS", "sigpos"),
    ("Secretaria", "Secretaria acadêmica (atendimento)", "secretaria"),
    ("Transporte", "Transporte", "transporte"),
    ("Secretaria qualidade", "Secretaria acadêmica (qualidade)", None),
]

MAPA_INFRA = {r[0]: (r[1], r[2] or "secretaria_qualidade") for r in ROTULOS_INFRA_2025}

def slug(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")

def extrai_infra(texto):
    prosa = secao(texto, "infra").split(" (percentuais")[0].rstrip(".")
    pares = [x.strip() for x in prosa.split(";") if x.strip()]
    itens, desconhecidos = [], []
    for i, par in enumerate(pares):
        m = re.match(r"^(.+?) (\d+,\d+)$", par)
        if not m: sys.exit(f"ERRO infraestrutura: nao entendi '{par}' (esperado 'Rotulo 9,99')")
        rot, val = m.group(1), num(m.group(2))
        if rot in MAPA_INFRA: rotulo, iid = MAPA_INFRA[rot]
        else: rotulo, iid = rot, slug(rot); desconhecidos.append(rot)
        itens.append({"n": i + 1, "id": iid, "rotulo": rotulo, "media": val, "classe": classifica(val)})
    if len(itens) < 20: sys.exit(f"ERRO infraestrutura: apenas {len(itens)} itens lidos")
    if desconhecidos:
        print(f"  AVISO infraestrutura: rotulos novos sem mapa (revisar ROTULOS_INFRA_2025): {desconhecidos}")
    return itens, pagina(texto, "infra")

def extrai_adesao(texto):
    prosa = secao(texto, "adesao")
    out = {}
    for sem in (f"{ANO}-1", f"{ANO}-2"):
        m = re.search(sem + r": (.*?)(?=\. " + str(ANO) + r"-2:|\. Defeito|$)", prosa)
        if not m:
            if sem.endswith("-2"): print(f"  AVISO adesao: semestre {sem} ausente na fonte (ciclo anual?)"); continue
            sys.exit(f"ERRO adesao: semestre {sem} nao encontrado (formato esperado: '{ANO}-1: diretora 100,0; ...')")
        bloco = m.group(1)
        d = {"segmentos": {}, "cursos": {}}
        for chave, rot in (("diretora", "direcao"), ("coords", "coordenadores"), ("professores", "docentes"),
                           ("estudantes", "discentes"), ("técnicos", "tecnicos"), ("total", "total")):
            mm = re.search(chave + r" (\d+,\d+)", bloco)
            d["segmentos"][rot] = num(mm.group(1)) if mm else None
        for curso, cid in (("Administração", "adm"), ("Matemática", "mat"), ("Medicina Veterinária", "medvet"), ("Psicologia", "psi")):
            mm = re.search(curso + r" (\d+,\d+)", bloco)
            d["cursos"][cid] = num(mm.group(1)) if mm else None
        out[sem] = d
    defeito = re.search(r"Defeito: ([^.]+)\.", prosa)
    return out, pagina(texto, "adesao"), (defeito.group(1) if defeito else None)

def extrai_imagem(texto):
    r = {}
    for tab, chave in (("img_est", "estudantes"), ("img_serv", "servidores")):
        prosa = secao(texto, tab)
        q1 = re.search(r"Q1 (\d+,\d+)", prosa); q2 = re.search(r"Q2 (\d+,\d+)", prosa)
        r[chave] = {"recomendar_q1": num(q1.group(1)), "prestigio_q2": num(q2.group(1)), "pagina": pagina(texto, tab)}
    return r

def estende_curados(infra, adesao, imagem, pag_infra, pag_ades):
    """Acrescenta o ano atual nas series curadas quando ainda nao consta (valores vindos da FONTE, com proveniencia)."""
    A = str(ANO); mudou = []
    p = CURADOS / "infraestrutura_2022_2025.json"; cur = json.loads(p.read_text(encoding="utf-8"))
    ids = {it["id"]: it for it in cur["itens"]}
    if any(A not in it for it in cur["itens"]):
        for x in infra:
            if x["id"] in ids and A not in ids[x["id"]]:
                ids[x["id"]][A] = x["media"]; ids[x["id"]]["prov"] += f"; {A} FONTE_RSA_{A} item {x['n']} p.{pag_infra} (auto)"
        for it in cur["itens"]: it.setdefault(A, None)
        cur["nota_metodo"] += f" {A}: acrescentado automaticamente pelo pipeline a partir da FONTE_RSA_{A}."
        p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); mudou.append(p.name)
    p = CURADOS / "imagem_2022_2025.json"; cur = json.loads(p.read_text(encoding="utf-8"))
    if not any(x["ano"] == A for x in cur["estudantes"]):
        cur["estudantes"].append({"ano": A, "q1": imagem["estudantes"]["recomendar_q1"], "q2": imagem["estudantes"]["prestigio_q2"], "prov": f"FONTE_RSA_{A} Imagem pelos Estudantes p.{imagem['estudantes']['pagina']} (auto)"})
        cur["servidores"].append({"ano": A, "q1": imagem["servidores"]["recomendar_q1"], "q2": imagem["servidores"]["prestigio_q2"], "prov": f"FONTE_RSA_{A} Imagem pelos Servidores p.{imagem['servidores']['pagina']} (auto)"})
        p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); mudou.append(p.name)
    p = CURADOS / "adesao_historica.json"; cur = json.loads(p.read_text(encoding="utf-8"))
    if not any(pt["rotulo"].startswith(A) for pt in cur["pontos"]):
        for sem, d in adesao.items():
            sg = d["segmentos"]
            cur["pontos"].append({"ano": ANO, "rotulo": sem, "discentes_pct": sg["discentes"], "discentes_abs": None, "docentes_pct": sg["docentes"], "docentes_abs": None,
                                  "tecnicos_pct": sg["tecnicos"], "tecnicos_abs": None, "total_pct": sg["total"],
                                  "proveniencia": f"FONTE_RSA_{A}, Tabela de Adesao, p.{pag_ades} (auto; absolutos a preencher)"})
        p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); mudou.append(p.name)
    p = CURADOS / "adesao_por_curso.json"; cur = json.loads(p.read_text(encoding="utf-8"))
    if not any(pt["rotulo"].startswith(A) for pt in cur["pontos"]):
        for sem, d in adesao.items():
            pt = {"rotulo": sem, "prov": f"FONTE_RSA_{A} Tabela de Adesao p.{pag_ades} (auto)"}
            for cid, v in d["cursos"].items(): pt[cid] = ({"pct": v} if v is not None else None)
            cur["pontos"].append(pt)
        p.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); mudou.append(p.name)
    if mudou: print(f"  curados estendidos com {A}: {mudou}  (REVISAR: absolutos, rupturas, fragilidades_recorrentes, planos_acao)")

def extraidos():
    print(f"2. Derivados extraidos de {FONTE_ATUAL.name}")
    texto = FONTE_ATUAL.read_text(encoding="utf-8")
    infra, pag_infra = extrai_infra(texto)
    adesao, pag_ades, defeito = extrai_adesao(texto)
    imagem = extrai_imagem(texto)
    if not OPC.nao_estender: estende_curados(infra, adesao, imagem, pag_infra, pag_ades)

    # Cruzamento com a serie curada: os valores do ano atual devem coincidir.
    A = str(ANO)
    cur = json.loads((CURADOS / "infraestrutura_2022_2025.json").read_text(encoding="utf-8"))
    mapa_cur = {it["id"]: it for it in cur["itens"]}
    divergencias, coincidem = [], 0
    for it in infra:
        c = mapa_cur.get(it["id"])
        if c and c.get(A) is not None and abs(c[A] - it["media"]) > 1e-9:
            divergencias.append(f"{it['id']}: curado {c[A]} x FONTE {it['media']}")
        elif c and c.get(A) is not None: coincidem += 1
        if c:
            it["serie"] = {a: c.get(a) for a in ANOS_SERIE}
            it["prov_serie"] = c["prov"]
    if divergencias:
        sys.exit("ERRO cruzamento infraestrutura x curado:\n  " + "\n  ".join(divergencias))
    print(f"  ok  cruzamento infraestrutura {A} x serie curada: {coincidem} itens coincidem")

    planos = json.loads((CURADOS / "planos_acao.json").read_text(encoding="utf-8"))
    frag = json.loads((CURADOS / "fragilidades_recorrentes.json").read_text(encoding="utf-8"))
    acoes_por_tema = {}
    for f in frag["recorrentes_2022_2025"]:
        acoes_por_tema[f["tema"]] = {"status": f["status"], "prov": f["prov"], "ciclos_fragil": f.get("ciclos_fragil"), "ciclos_oport": f.get("ciclos_oport")}
    # Mapa tema (fragilidades) -> id (infra)
    tema_para_id = {"Espaços esportivos": "esportivos", "Alimentação (RU/cantina)": "alimentacao",
                    "Transporte": "transporte", "Internet": "internet", "Instalações sanitárias": "sanitarias",
                    "Convivência": "convivencia", "Laboratórios e práticas": "praticas", "Iluminação": "iluminacao",
                    "Parada de ônibus": "parada"}
    acao_por_id = {}
    for tema, info in acoes_por_tema.items():
        if tema in tema_para_id: acao_por_id[tema_para_id[tema]] = info

    tt = lambda k: titulo_tabela(texto, k)
    idx_rsa = next((r for r in indice_rsa() if r["ano_ref"] == ANO), {})
    ciclo = {
        "_meta": meta(f"base_de_conhecimento/fontes_estruturadas/FONTE_RSA_{ANO}.md",
                      {"tipo": "extraido", "tabelas": [tt("adesao"), tt("infra"), tt("img_est"), tt("img_serv"), "Quadro de acompanhamento (via planos_acao.json)"]}),
        "relatorio": {"titulo": f"Relatório de Autoavaliação Setorial {ANO} do CPAR/UFMS", "ano_ref": ANO, "paginas": idx_rsa.get("paginas"), "url_publica": idx_rsa.get("url_publica"),
                       "escala": "1 (Discordo totalmente) a 5 (Concordo totalmente); NA/NQR/NSR fora das médias",
                       "classificacao": {"fragilidade": "média abaixo de 2,50", "oportunidade": "média de 2,50 a 3,49", "bem_avaliado": "média igual ou superior a 3,50"}},
        "adesao": {"pagina": pag_ades, "titulo_tabela": tt("adesao"), "defeito_original": defeito, **adesao},
        "infraestrutura": {"pagina": pag_infra, "titulo_tabela": tt("infra"),
                            "nota": planos.get("nota_infra_ciclo", ""),
                            "itens": infra},
        "imagem": {"titulo_tabelas": tt("img_est") + " e " + tt("img_serv"), **imagem},
        "planos": {"titulo_quadro": planos.get("titulo_quadro", "Quadro de acompanhamento das ações do plano anterior"),
                    **{k: planos["acompanhamento"][k] for k in ("total", "concluidas", "em_andamento", "nao_iniciadas", "pct_iniciadas", "por_responsavel")},
                    "smart_atual": planos["smart_atual"]},
    }
    escreve(f"ciclo_{ANO}.json", ciclo); escreve("ciclo_atual.json", ciclo)

    # Sintese para a pagina inicial: 5 mais criticos, 5 mais bem avaliados, acoes vinculadas
    ordenados = sorted(infra, key=lambda x: x["media"])
    criticos = [x for x in ordenados if x["classe"] != "bem_avaliado"]  # todos abaixo de 3,50 (4 em 2025)
    fortes = list(reversed(ordenados[-5:]))
    def cartao(x):
        c = {"id": x["id"], "rotulo": x["rotulo"], "media": x["media"], "classe": x["classe"],
             "serie": x.get("serie"), "prov": f"RSA {ANO}, {tt('infra')}, p. {pag_infra}, item {x['n']}"}
        if x["id"] in acao_por_id:
            a = acao_por_id[x["id"]]
            c["acao"] = a["status"]; c["acao_prov"] = a["prov"]
            c["ciclos_fragil"] = a["ciclos_fragil"]; c["ciclos_oport"] = a["ciclos_oport"]
        return c
    sintese = {
        "_meta": meta(f"base_de_conhecimento/fontes_estruturadas/FONTE_RSA_{ANO}.md",
                      {"tipo": "extraido", "nota": "Recorte da tabela de infraestrutura do ano cruzado com infraestrutura_2022_2025.json, fragilidades_recorrentes.json e planos_acao.json"}),
        "ano_ref": ANO,
        "criticos": [cartao(x) for x in criticos],
        "fortes": [cartao(x) for x in fortes],
        "acoes": {"total": planos["acompanhamento"]["total"], "concluidas": planos["acompanhamento"]["concluidas"],
                   "em_andamento": planos["acompanhamento"]["em_andamento"], "nao_iniciadas": planos["acompanhamento"]["nao_iniciadas"],
                   "pct_iniciadas": planos["acompanhamento"]["pct_iniciadas"], "prov": planos["acompanhamento"]["prov"],
                   "destaques": planos.get("destaques_direcao", [])},
        "adesao_total": {"semestres": {sem: d["segmentos"]["total"] for sem, d in adesao.items()},
                         "discentes_primeiro": adesao[f"{ANO}-1"]["segmentos"]["discentes"], "prov": f"RSA {ANO}, {tt('adesao')}, p. {pag_ades}"},
        "imagem": {"estudantes_recomendar": imagem["estudantes"]["recomendar_q1"], "servidores_recomendar": imagem["servidores"]["recomendar_q1"],
                   "prov": f"RSA {ANO}, {tt('img_est')} e {tt('img_serv')}"},
    }
    escreve(f"sintese_{ANO}.json", sintese); escreve("sintese_atual.json", sintese)

# --------------------------------------------------------------- 3. indice
def indice_rsa():
    rsa = []
    for p in sorted(BASE.glob("RSA_*_CPAR.md")):
        ano = int(p.name.split("_")[1])
        t = p.read_text(encoding="utf-8")
        did = re.search(r"ID `([^`]+)`", t)
        url = re.search(r"URL `(https?://[^`]+)`", t)
        pdf = re.search(r"\*\*Fonte primaria\*\*: `([^`]+\.pdf)`", t)
        pags = re.search(r"(\d+) paginas", t)
        url_pub = url.group(1) if url else (f"https://drive.google.com/file/d/{did.group(1)}/view" if did else None)
        rsa.append({"ano_ref": ano, "arquivo_md": p.name, "fonte_md": f"fontes_estruturadas/FONTE_RSA_{ano}.md",
                    "arquivo_pdf": pdf.group(1) if pdf else None,
                    "url_publica": url_pub,
                    "pagina_oficial": "https://cpar.ufms.br/avaliacao-institucional/",
                    "drive_id": did.group(1) if did else None, "paginas": int(pags.group(1)) if pags else None})
    return rsa

def indice():
    print("3. Indice de documentos (esquema_banco)")
    sql = (RAIZ / "esquema_banco" / "schema_cpar_historico.sql").read_text(encoding="utf-8")
    docs = []
    for m in re.finditer(r"\((\d+), (\d{4}), '([^']*)', '([^']*)', '([^']*)', (NULL|\d+), (NULL|'[^']*'), (NULL|'[^']*'), '([^']*)', '([^']*)'\)", sql):
        docs.append({"id": int(m.group(1)), "ano_ref": int(m.group(2)), "periodo": m.group(3), "tipo": m.group(4),
                     "titulo": m.group(5), "paginas": None if m.group(6) == "NULL" else int(m.group(6)),
                     "data_aprovacao": None if m.group(7) == "NULL" else m.group(7).strip("'"),
                     "drive_id": None if m.group(8) == "NULL" else m.group(8).strip("'"),
                     "arquivo_md": m.group(9), "cobertura": m.group(10)})
    rsa = indice_rsa()
    escreve("indice.json", {"_meta": meta("esquema_banco/schema_cpar_historico.sql", {"tipo": "indice"}), "ano_atual": ANO,
                            "pagina_oficial": "https://cpar.ufms.br/avaliacao-institucional/",
                            "raai_ufms": docs, "rsa_cpar": rsa,
                            "lacunas": ["2017: relatório institucional (RAAI) ausente; o relatório setorial de 2017 cobre o ano", "2013: sem relatório setorial na série",
                                        "2018 a 2020: relatório institucional trienal, com recorte apenas de 2020"]})

if __name__ == "__main__":
    print(f"Ano do ciclo mais recente: {ANO}")
    extraidos(); curados(); indice()
    print("Concluido.")
