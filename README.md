# Autoavaliação do Câmpus de Paranaíba (CPAR/UFMS): site histórico da CSA

Site estático que apresenta à comunidade acadêmica os resultados dos Relatórios de Autoavaliação Setorial do CPAR de 2014 a 2025, mantido pela Comissão Setorial de Avaliação (CSA/CPAR). Hospedado no GitHub Pages a partir da pasta `docs/`.

## Estrutura

| Pasta ou arquivo | Conteúdo | Publicado? |
| --- | --- | --- |
| `docs/` | O site: `index.html` (home em capítulos), `voce-pediu.html`, `cursos.html` (Meu curso), `campus.html` (Raio-X do câmpus), `adesao.html` (Participação), `metodo.html` (Fontes), mais `css/`, `js/`, `data/`, `assets/`. `ciclo.html`, `fragilidades.html` e `infraestrutura.html` só redirecionam para as páginas novas. | Sim |
| `_molde/` | Moldes das páginas (`head.html`, `foot.html`, `<pagina>.body.html`) e `monta_todas.sh`, que remonta `docs/*.html` e os redirecionamentos | Não é servido |
| `docs/data/` | Derivados JSON gerados por `scripts/gerar_dados.py`. Nunca editar à mão. | Sim |
| `docs/assets/` | Tokens do UFMS Design System (`colors_and_type.css`), `chart-defaults.js`, logotipos | Sim |
| `docs/js/vendor/` | Cópia local do Chart.js 4.4.0 (fallback quando o CDN estiver bloqueado) | Sim |
| `base_de_conhecimento/` | Extrações em markdown dos relatórios (RSA 2014 a 2025, FONTE_RSA, RAAI, Consolidado de Indicadores). Base canônica, somente leitura. | Sim, como auditoria |
| `esquema_banco/` | Esquema SQLite e dicionário de campos do banco histórico | Sim |
| `dados/curados/` | Derivados revisados manualmente contra a base (herdados do protótipo) | Não é servido |
| `scripts/` | `gerar_dados.py` (base para JSON) e `validar.py` (âncoras, referências, redação) | Não é servido |
| `tests/valores_ancora.json` | Valores de conferência que o validador exige | Não é servido |
| `.github/workflows/validar.yml` | Roda o validador a cada push | Não é servido |

## Regras editoriais

1. A base é somente leitura para o site. Correções são feitas na origem (markdown), nunca nos derivados.
2. Cruzar por título de tabela ou figura, nunca por número.
3. Lacunas aparecem como `null` (na tela: "sem dado"), nunca como zero nem estimativa.
4. Percentuais e médias somente quando impressos no relatório. Sem recálculo.
5. Feedback negativo sempre anonimizado; nomes apenas em elogio.
6. Classificação CPA/MEC: fragilidade abaixo de 2,50; oportunidade de melhoria de 2,50 a 3,49; bem avaliado a partir de 3,50.
7. Sem travessão longo nem meia-risca nos textos do site (o validador acusa).
8. O site é escrito para estudantes: frases curtas, em segunda pessoa, e o convite a responder o SIAI em toda página. O pedido da comunidade e a ação do câmpus só aparecem juntos (`voce_pediu.json`) quando a ação está registrada num quadro do relatório; lacuna de registro é mostrada como tal.

## Como atualizar a cada ciclo

O fluxo completo está na skill `atualizar-site-csa` (Claude). Em resumo:

1. `python3 scripts/novo_ciclo.py --pdf <RSA_<ano>.pdf> --ano <ano> --drive-id <id>`: extrai o texto, localiza as tabelas pelo título e cria os rascunhos `RSA_<ano>_CPAR.md` e `fontes_estruturadas/FONTE_RSA_<ano>.md`.
2. Preencher os rascunhos e os curados que dependem de leitura do relatório (`planos_acao.json`, `fragilidades_recorrentes.json`, `rupturas.json` e `voce_pediu.json`: notas do ano e situação de cada ação conforme o novo quadro de acompanhamento).
3. `python3 scripts/gerar_dados.py --ano <ano>`: acrescenta o ano nas séries (infraestrutura, imagem, adesão) e gera `ciclo_<ano>.json`, `sintese_<ano>.json` e as cópias `*_atual.json` que as páginas leem.
4. Acrescentar âncoras do ano em `tests/valores_ancora.json` e rodar `python3 scripts/validar.py`.
5. Revisar as frases-síntese e os textos que citam anos em `_molde/*.body.html` (principalmente `index` e `voce-pediu`), remontar com `bash _molde/monta_todas.sh` e conferir no navegador (`cd docs && python3 -m http.server 8000`) nos temas claro e escuro, no desktop e no celular.
6. `git commit` em um ramo `ciclo-<ano>`, revisão, `git push` e mesclagem em `main`. O GitHub Pages publica em poucos minutos.

As páginas não têm o ano gravado: leem `ciclo_atual.json` e `sintese_atual.json`. Os textos fixos que citam anos anteriores (memórias, marcos) são revisados a cada ciclo.

## A cada etapa do SIAI

Atualizar `periodo` (`inicio`, `fim`, `rotulo`) em `dados/curados/campanha.json` e rodar `gerar_dados.py`. Dentro do período, o botão fixo "Responda a avaliação" mostra "Aberta: <rotulo>"; fora dele, o texto padrão. O link do botão também vem desse arquivo.

## Publicação no GitHub Pages

Repositório `csacpar/csacpar.github.io` (site na raiz da URL). Em Settings, Pages: Source "Deploy from a branch", branch `main`, pasta `/docs`. O arquivo `docs/.nojekyll` desliga o processamento Jekyll.

## Licença

Código sob licença MIT. Dados, textos e gráficos sob Creative Commons Atribuição 4.0 (CC BY 4.0), com atribuição a "CSA/CPAR/UFMS". Ver `LICENSE`.
