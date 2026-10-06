#!/bin/bash
# uso: monta.sh <pagina-id> "<titulo>" "<descricao>" corpo.html saida.html
# Os moldes (head.html, foot.html, icones.json) sao lidos da pasta deste script.
set -e
M="$(cd "$(dirname "$0")" && pwd)"
PY="$(command -v python3 || command -v python)"
"$PY" - "$M" "$@" <<'PY'
import sys, pathlib, json, re
m, pag, tit, desc, corpo, saida = sys.argv[1:7]
m = pathlib.Path(m)
head = (m/"head.html").read_text(encoding="utf-8").replace("{{TITULO}}", tit).replace("{{DESCRICAO}}", desc).replace("{{PAGINA}}", pag)
foot = (m/"foot.html").read_text(encoding="utf-8")
ico = json.loads((m/"icones.json").read_text(encoding="utf-8"))
body = pathlib.Path(corpo).read_text(encoding="utf-8")
html = re.sub(r"\{\{ICO:([a-z]+)\}\}", lambda mm: ico[mm.group(1)], head + body + foot)
pathlib.Path(saida).write_text(html, encoding="utf-8", newline="\n")
print("montado", saida)
PY
