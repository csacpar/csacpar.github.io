# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é

Site estático (GitHub Pages, pasta `docs/`, repo `csacpar/csacpar.github.io`) com os resultados dos Relatórios de Autoavaliação Setorial (RSA) do Câmpus de Paranaíba (CPAR/UFMS), 2014 a 2025, mantido pela CSA/CPAR. Sem framework, sem etapa de build no Pages, sem dependências Python externas. Conteúdo e código em português.

A pasta-mãe (`../`) não é repositório: guarda o protótipo original (`../prototipo/`, referência intocada), o UFMS Design System (`../design-system/`) e cópias da base. Este repositório é `site/`.

## Comandos

Rodar da raiz do repositório (`site/`). No Windows, `python` no lugar de `python3`.

```bash
python3 scripts/gerar_dados.py              # regenera docs/data/*.json (ano = maior FONTE_RSA_<ano>.md)
python3 scripts/gerar_dados.py --ano 2026   # fixa o ciclo mais recente
python3 scripts/validar.py                  # âncoras, trechos na base, refs das páginas, travessões; sai 1 se falhar
python3 scripts/novo_ciclo.py --pdf RSA_2026.pdf --ano 2026 --drive-id <id>   # rascunhos RSA/FONTE do novo ciclo
cd docs && python3 -m http.server 8000      # pré-visualização local (fetch exige servidor)
```

Não há testes unitários; `validar.py` é a verificação. O CI (`.github/workflows/validar.yml`) regenera os derivados e falha se `docs/data/` versionado divergir do regenerado (ignorando `_meta.gerado_em`). Logo: sempre rodar `gerar_dados.py` e commitar o resultado junto com qualquer mudança em `base_de_conhecimento/` ou `dados/curados/`.

## Fluxo de dados

```
base_de_conhecimento/*.md  (canônica, somente leitura)
  ├─ fontes_estruturadas/FONTE_RSA_<ano>.md ──regex por título de tabela──┐
dados/curados/*.json  (revisados à mão; valores conferidos contra a base) ├─> scripts/gerar_dados.py ─> docs/data/*.json
esquema_banco/schema_cpar_historico.sql ──> indice.json ──────────────────┘
tests/valores_ancora.json ──> scripts/validar.py confere docs/data/
```

- `docs/data/` é derivado: nunca editar à mão. Cada JSON tem cabeçalho `_meta` (origem, hash, versão do pipeline).
- `gerar_dados.py` produz `ciclo_<ano>.json` e `sintese_<ano>.json` e copia para `ciclo_atual.json` / `sintese_atual.json`. As páginas leem só os `*_atual.json`; não gravar ano nas páginas.
- Sem `--nao-estender`, o ano novo é acrescentado automaticamente às séries curadas (infraestrutura, imagem, adesão).
- Âncoras em `tests/valores_ancora.json` usam caminhos tipo `itens[id=esportivos].2022`, `pontos[0].discentes_pct`, `len(a.b)` (resolvidos por `get()` em `validar.py`).

## Páginas

Páginas v2: `index` (home em capítulos), `voce-pediu`, `cursos` (Meu curso), `campus` (Raio-X), `adesao` (Participação), `metodo` (Fontes); `ciclo` fora do menu. `fragilidades.html` e `infraestrutura.html` são redirecionamentos gerados por `monta_todas.sh` (não editar). No celular o menu vira barra inferior (`.barra-app` em `head.html`).

`docs/*.html` são arquivos completos e independentes, montados a partir de `_molde/` (`head.html` com menu + `<nome>.body.html` + `foot.html`; `{{ICO:nome}}` vem de `icones.json`). Mudança de menu/rodapé: editar o molde e remontar tudo com `bash _molde/monta_todas.sh` (tabela de páginas, títulos e descrições dentro do script; `monta.sh` monta uma página só). Mudança em uma página só: editar `docs/<pagina>.html` e replicar no `.body.html` correspondente, senão a próxima remontagem desfaz.

`docs/js/site.js` concentra utilitários compartilhados (carregar JSON de `data/`, formatação pt-BR com "sem dado" para `null`, semáforo CPA, tabelas acessíveis, CSV com `;`, tema claro/escuro, Chart.js). Chart.js 4.4.0 por CDN com fallback em `docs/js/vendor/`. Estilo: tokens do UFMS Design System em `docs/assets/colors_and_type.css` + `docs/css/site.css` + `docs/css/v2.css` (camada v2: capítulos, números grandes, botão fixo do SIAI); conferir sempre nos dois temas.

`dados/curados/voce_pediu.json` liga cada pedido da comunidade à ação registrada nos quadros dos RSA, com `situacao` em `concluida | em_andamento | no_plano | sem_registro`; só entram ações documentadas, e a situação muda apenas quando um novo relatório a registrar. `dados/curados/campanha.json` é configuração editorial (link do SIAI, período da etapa aberta, meta de adesão): atualizar o `periodo` a cada etapa; o botão fixo mostra "Aberta" só dentro do período.

## Regras editoriais (o validador cobra parte delas)

1. Base somente leitura: corrigir na origem (markdown), nunca nos derivados.
2. Cruzar tabelas/figuras por título, nunca por número (numeração muda entre ciclos).
3. Lacuna = `null` (tela: "sem dado"), nunca zero nem estimativa. Lacunas conhecidas: RAAI 2017; ciclo setorial 2013.
4. Percentuais e médias só se impressos no relatório; sem recálculo.
5. Feedback negativo sempre anonimizado; nomes só em elogio.
6. Classificação CPA/MEC: fragilidade < 2,50; oportunidade de melhoria 2,50 a 3,49; bem avaliado ≥ 3,50.
7. Defeitos do original preservados com flag.
8. Sem travessão longo (—) nem meia-risca (–) em textos do site.
9. CSV: delimitador `;`, utf-8-sig.

`base_de_conhecimento/AGENTS.md` traz o protocolo de consulta à base (Matriz de Indexação: qual documento abrir para cada tipo de demanda) e o contexto institucional (cursos, estrutura do RSA).

## Novo ciclo

Fluxo completo na skill `atualizar-site-csa`. Resumo: `novo_ciclo.py` → preencher rascunhos `RSA_<ano>_CPAR.md` e `FONTE_RSA_<ano>.md` e curados de leitura (`planos_acao.json`, `fragilidades_recorrentes.json`, `rupturas.json`) → `gerar_dados.py --ano <ano>` → âncoras novas em `tests/valores_ancora.json` → `validar.py` → revisar frases-síntese e textos fixos que citam anos → commit em ramo `ciclo-<ano>`, push só após aprovação, merge em `main`.
