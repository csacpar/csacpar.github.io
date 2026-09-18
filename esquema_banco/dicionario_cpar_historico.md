# Dicionario de campos do banco historico do CPAR

Regra geral: dado publicado no site precisa de fonte com tabela por titulo, pagina e ano. Estimativa visual nunca entra como definitivo. 2017 e lacuna declarada.

## documento
Uma linha por produto da serie. ano_ref e o ano de referencia para o site. periodo usa anual, 2020-1, 2020-2, 2021-1, 2021-2, parcial, recorte ou trienal. tipo usa anual, parcial, trienal ou recorte. arquivo_md e o nome em base_de_conhecimento. cobertura descreve o alcance real.

## gestao
Quem dirigia o CPAR e a UFMS em cada ano. nivel usa CPAR, UFMS Central, CPA ou SEAVI. Nao atribuir dirigente sem pagina e portaria.

## adesao
Participacao percentual por unidade e segmento. unidade usa sigla (CPAR, UFMS). segmento usa discente, docente, tecnico, coord grad, coord pos, diretor ou media geral. qualidade usa definitivo, estimativa_visual, parcial ou ausente. Estimativas das Figuras 2015 e 2016 entram como estimativa_visual, nunca como definitivo.

## oferta_curso
Vagas e turnos do CPAR nos PSU. ano_psu e o ano do processo seletivo. curso usa Administracao, Matematica licenciatura ou Psicologia bacharelado.

## visita_inloco
Avaliacoes externas por curso. conceito_final de 1 a 5. Zero visita em ano sem curso do CPAR deve ser registrado como ausencia, nao como nota zero.

## enade_curso
Desempenho por curso no Enade. inscritos e participantes sempre juntos. conceito_enade_faixa e cpc_faixa de 1 a 5. Sem juizo causal no site.

## clinica_atendimento
Clientes por ano. pre_agendado marca 1 para os 15 pre de 2020 antes da pandemia. Criterios distintos entre anos vao em observacao.

## patrimonio
Area e valores do CPAR, com fonte CPO ou PROINFRA. pct_ufms e o percentual sobre a UFMS.

## escala_ufms
Tamanho da UFMS para contexto. Divergencias entre anos ficam em observacao, sem conciliacao forcada.

## observacao
Notas livres por ano e tema, por exemplo pandemia, greve ou missao.

## lacuna
Tudo que falta, com motivo. Exemplos: dirigente 2018 e 2020, segmentos exatos de 2020, Figuras sem tabela, 2017 sem fonte.

## Carga
CSVs com ; e utf-8-sig, um por tabela, com os mesmos nomes de coluna. Revisao antes de publicar: grep por Paranaiba e CPAR nos md, conferencia de pagina e fonte, e marcacao de qualidade.
