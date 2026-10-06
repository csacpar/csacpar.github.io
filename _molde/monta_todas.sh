#!/bin/bash
# Remonta todas as paginas de docs/ a partir de _molde/ e gera os redirecionamentos
# dos enderecos antigos. Uso: bash _molde/monta_todas.sh
set -e
M="$(cd "$(dirname "$0")" && pwd)"
R="$(dirname "$M")"
# Tabela: arquivo|pagina-id|titulo|descricao
while IFS='|' read -r arq id tit desc; do
  [ -z "$arq" ] && continue
  bash "$M/monta.sh" "$id" "$tit" "$desc" "$M/$arq.body.html" "$R/docs/$arq.html"
done <<'TAB'
index|inicio|Você avaliou, o câmpus ouviu|Resultados da autoavaliação do Câmpus de Paranaíba (CPAR/UFMS): o que a comunidade apontou, o que já está mudando e por que a sua resposta no SIAI conta.
voce-pediu|voce-pediu|Você pediu, o câmpus fez|Temas apontados repetidamente pela comunidade do CPAR desde 2022 e o que foi feito a respeito de cada um.
cursos|cursos|Meu curso|Ingressantes, ocupação de vagas, diplomação, evasão e metas do PDU 2025 a 2030 dos cursos do CPAR/UFMS.
campus|campus|Raio-X do câmpus|Como a comunidade avalia a infraestrutura e os serviços do CPAR/UFMS desde 2022 e o quanto recomenda o câmpus.
adesao|adesao|Participação|Quantas pessoas do CPAR/UFMS responderam a autoavaliação desde 2014, por segmento e por curso.
metodo|metodo|Fontes|De onde vêm os números da autoavaliação do CPAR/UFMS, como ler o semáforo e onde estão os relatórios.
TAB
# Redirecionamentos: antigo|novo
while IFS='|' read -r velho novo; do
  [ -z "$velho" ] && continue
  cat > "$R/docs/$velho.html" <<HTML
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página movida | Autoavaliação CPAR/UFMS</title>
<meta http-equiv="refresh" content="0; url=$novo.html">
<link rel="canonical" href="$novo.html">
<meta name="robots" content="noindex">
</head>
<body>
<p>Esta página mudou de endereço: <a href="$novo.html">$novo.html</a>.</p>
<script>location.replace("$novo.html" + location.hash);</script>
</body>
</html>
HTML
  echo "redireciona docs/$velho.html -> $novo.html"
done <<'RED'
fragilidades|voce-pediu
infraestrutura|campus
ciclo|campus
RED
