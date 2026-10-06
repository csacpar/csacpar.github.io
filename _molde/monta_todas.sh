#!/bin/bash
# Remonta todas as paginas de docs/ a partir de _molde/. Uso: bash _molde/monta_todas.sh
# Tabela: arquivo|pagina-id|titulo|descricao
set -e
M="$(cd "$(dirname "$0")" && pwd)"
R="$(dirname "$M")"
while IFS='|' read -r arq id tit desc; do
  [ -z "$arq" ] && continue
  bash "$M/monta.sh" "$id" "$tit" "$desc" "$M/$arq.body.html" "$R/docs/$arq.html"
done <<'TAB'
index|inicio|Você falou, o câmpus fez|Resultados da autoavaliação do Câmpus de Paranaíba (CPAR/UFMS) desde 2014: pontos críticos, pontos fortes e ações em andamento, em linguagem simples.
ciclo|ciclo|Ciclo atual em resumo|Resumo do Relatório de Autoavaliação Setorial mais recente do CPAR/UFMS: adesão, infraestrutura, imagem do câmpus e situação das ações.
fragilidades|fragilidades|Fragilidades recorrentes e ações|Temas apontados repetidamente pela comunidade do CPAR desde 2022 e situação das ações planejadas.
infraestrutura|infraestrutura|Infraestrutura e imagem|Avaliação da infraestrutura do CPAR/UFMS pela comunidade desde 2022, itens críticos, raio-X do ciclo e imagem do câmpus.
adesao|adesao|Adesão à autoavaliação|Participação da comunidade do CPAR/UFMS na autoavaliação desde 2014, por segmento e por curso, com marcos e lacunas.
cursos|cursos|Os cursos em números|Ingressantes, ocupação de vagas, diplomação, evasão e metas do PDU 2025 a 2030 dos cursos do CPAR/UFMS.
metodo|metodo|Fontes e método|De onde vêm os números da autoavaliação do CPAR/UFMS, como ler o semáforo e onde estão os relatórios.
TAB
