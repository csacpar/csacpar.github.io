#!/bin/bash
# uso: monta.sh <pagina-id> "<titulo>" "<descricao>" corpo.html saida.html
set -e
python3 - "$@" <<'PY'
import sys, pathlib, json, re
pag, tit, desc, corpo, saida = sys.argv[1:6]
m = pathlib.Path(__file__).resolve().parent if "__file__" in globals() else pathlib.Path.home()/"molde"
m = pathlib.Path.home()/"molde"
head = (m/"head.html").read_text(encoding="utf-8").replace("{{TITULO}}", tit).replace("{{DESCRICAO}}", desc).replace("{{PAGINA}}", pag)
foot = (m/"foot.html").read_text(encoding="utf-8")
ico = json.loads((m/"icones.json").read_text(encoding="utf-8"))
body = pathlib.Path(corpo).read_text(encoding="utf-8")
body = re.sub(r"\{\{ICO:([a-z]+)\}\}", lambda mm: ico[mm.group(1)], body)
pathlib.Path(saida).write_text(head + body + foot, encoding="utf-8")
print("montado", saida)
PY
