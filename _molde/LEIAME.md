# Molde das páginas

As páginas de `docs/` são arquivos HTML completos e independentes (sem etapa de build no GitHub Pages).
Para não divergirem no cabeçalho, no menu e no rodapé, cada uma foi montada a partir de:

- `head.html`: `<head>`, cabeçalho e menu (marcadores `{{TITULO}}`, `{{DESCRICAO}}`, `{{PAGINA}}`);
- `<nome>.body.html`: conteúdo principal e script da página;
- `foot.html`: rodapé.

Para alterar o menu ou o rodapé em todas as páginas: editar `head.html` ou `foot.html` e remontar:

```
bash _molde/monta.sh inicio "Você falou, o câmpus fez" "descrição" _molde/index.body.html docs/index.html
```

O script `monta.sh` procura os moldes em `$HOME/molde`; ajuste a variável `M` ou copie esta pasta para lá.
Editar apenas uma página: pode-se editar `docs/<pagina>.html` diretamente e replicar a mudança no `.body.html` correspondente.
