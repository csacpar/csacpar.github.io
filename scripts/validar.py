#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar.py: verificacao dos derivados publicados em docs/data/.

Checa: (1) JSON validos com cabecalho _meta; (2) valores ancora de
tests/valores_ancora.json; (3) trechos literais que precisam existir na base;
(4) paginas HTML referenciam apenas derivados existentes; (5) ausencia de
travessao longo nos textos do site (padrao de redacao da CSA); (6) links
internos e redirecionamentos apontam para paginas existentes.
Sai com codigo 1 em qualquer falha. Uso: python3 scripts/validar.py
"""
import json, re, sys, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "docs" / "data"
BASE = RAIZ / "base_de_conhecimento"
falhas = []

def get(obj, caminho):
    """Resolve 'a.b[2].c', 'a[id=x].b', 'len(a.b)'."""
    if caminho.startswith("len(") and caminho.endswith(")"):
        return len(get(obj, caminho[4:-1]))
    cur = obj
    for tok in re.findall(r"[^.\[\]]+|\[[^\]]+\]", caminho):
        if tok.startswith("["):
            sel = tok[1:-1]
            if "=" in sel:
                k, v = sel.split("=", 1)
                cur = next(x for x in cur if str(x.get(k)) == v)
            else:
                cur = cur[int(sel)]
        else:
            cur = cur[tok]
    return cur

# 1. JSON validos
derivados = {}
for p in sorted(DATA.glob("*.json")):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        falhas.append(f"{p.name}: JSON invalido ({e})"); continue
    if "_meta" not in d: falhas.append(f"{p.name}: sem cabecalho _meta")
    derivados[p.name] = d
print(f"1. {len(derivados)} derivados lidos")

# 2. Ancoras
anc = json.loads((RAIZ / "tests" / "valores_ancora.json").read_text(encoding="utf-8"))
ok = 0
for a in anc["ancoras"]:
    try:
        v = get(derivados[a["arquivo"]], a["caminho"])
    except Exception as e:
        falhas.append(f"{a['arquivo']}:{a['caminho']} nao resolvido ({e})"); continue
    if v != a["esperado"]:
        falhas.append(f"{a['arquivo']}:{a['caminho']} = {v!r}, esperado {a['esperado']!r}")
    else:
        ok += 1
print(f"2. {ok} de {len(anc['ancoras'])} valores ancora conferidos")

# 3. Textos na base
for t in anc["textos_na_base"]:
    txt = (BASE / t["arquivo"]).read_text(encoding="utf-8")
    if t["contem"] not in txt:
        falhas.append(f"base {t['arquivo']}: trecho '{t['contem']}' nao encontrado")
print(f"3. {len(anc['textos_na_base'])} trechos literais procurados na base")

# 4. Referencias das paginas
htmls = sorted((RAIZ / "docs").glob("*.html"))
for h in htmls:
    s = h.read_text(encoding="utf-8")
    for ref in re.findall(r"data/([A-Za-z0-9_\-]+\.json)", s):
        if ref not in derivados: falhas.append(f"{h.name}: referencia data/{ref} inexistente")
    for ref in re.findall(r"(?:src|href)=\"((?:css|js|assets)/[^\"]+)\"", s):
        if not (RAIZ / "docs" / ref).exists(): falhas.append(f"{h.name}: arquivo {ref} inexistente")
    # 5. Travessao longo / meia-risca no texto visivel
    visivel = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    if "—" in visivel or "–" in visivel:
        falhas.append(f"{h.name}: contem travessao longo ou meia-risca no texto")
print(f"4. {len(htmls)} paginas HTML verificadas")

# 6. Links internos e redirecionamentos apontam para paginas existentes
nlinks = 0
for h in htmls:
    s = h.read_text(encoding="utf-8")
    alvos = re.findall(r"href=\"([A-Za-z0-9_\-]+\.html)(?:#[^\"]*)?\"", s)
    alvos += re.findall(r"http-equiv=\"refresh\" content=\"0; url=([A-Za-z0-9_\-]+\.html)\"", s)
    for alvo in alvos:
        nlinks += 1
        if not (RAIZ / "docs" / alvo).exists(): falhas.append(f"{h.name}: link para {alvo} inexistente")
        elif alvo != h.name and "http-equiv=\"refresh\"" in (RAIZ / "docs" / alvo).read_text(encoding="utf-8") and "http-equiv=\"refresh\"" not in s:
            falhas.append(f"{h.name}: link para {alvo}, que e so um redirecionamento; apontar para a pagina nova")
print(f"6. {nlinks} links internos conferidos")

if falhas:
    print("\nFALHAS:"); [print("  - " + f) for f in falhas]; sys.exit(1)
print("Validacao concluida sem falhas.")
