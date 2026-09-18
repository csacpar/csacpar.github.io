/* Site da CSA/CPAR: utilitários comuns a todas as páginas.
   Regras: base somente leitura; lacuna = null (tela: "sem dado"); médias e
   percentuais declarados, sem recálculo; classificação CPA/MEC. */
(function () {
  "use strict";

  var CORTE_FRAG = 2.5, CORTE_OPORT = 3.5;

  // Paleta categórica validada (Delta E CVD >= 8, contraste >= 3:1 sobre branco).
  // Ordem fixa por entidade: nunca reatribuir cor ao filtrar séries.
  var PALETA = ["#0088B7", "#C2410C", "#5B3FA6", "#008F5A", "#7B8794"];
  var COR = { frag: "#D32F2F", oport: "#F57C00", bem: "#00A859", lacuna: "#C4CDD5" };

  function fmtNum(v, dec) {
    if (v === null || v === undefined || isNaN(v)) return "sem dado";
    return Number(v).toFixed(dec === undefined ? 2 : dec).replace(".", ",");
  }
  function fmtPct(v, dec) { return v === null || v === undefined ? "sem dado" : fmtNum(v, dec) + "%"; }
  function fmtInt(v) { return v === null || v === undefined ? "sem dado" : String(v).replace(/\B(?=(\d{3})+(?!\d))/g, "."); }

  function classe(m) {
    if (m === null || m === undefined) return { id: "lacuna", rotulo: "sem dado", cls: "sem-lacuna", cor: COR.lacuna };
    if (m < CORTE_FRAG) return { id: "frag", rotulo: "Fragilidade", cls: "sem-frag", cor: COR.frag };
    if (m < CORTE_OPORT) return { id: "oport", rotulo: "Oportunidade de melhoria", cls: "sem-oport", cor: COR.oport };
    return { id: "bem", rotulo: "Bem avaliado", cls: "sem-bem", cor: COR.bem };
  }
  function semaforo(m) { var c = classe(m); return '<span class="sem ' + c.cls + '">' + c.rotulo + "</span>"; }
  function legendaSemaforo() {
    return '<p class="legenda-sem"><span class="sem sem-frag">Fragilidade: abaixo de 2,50</span>' +
      '<span class="sem sem-oport">Oportunidade: 2,50 a 3,49</span>' +
      '<span class="sem sem-bem">Bem avaliado: 3,50 ou mais</span></p>';
  }

  function esc(s) { return String(s === null || s === undefined ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function loadJSON(path) {
    return fetch(path).then(function (r) {
      if (!r.ok) throw new Error("Falha ao ler " + path + " (" + r.status + ")");
      return r.json();
    });
  }
  function carregar(lista) { return Promise.all(lista.map(function (n) { return loadJSON("data/" + n); })); }

  function erro(msg) {
    var el = document.getElementById("erro-carga");
    if (!el) { el = document.createElement("div"); el.id = "erro-carga"; el.className = "alert alert-danger"; document.querySelector(".csa-main").prepend(el); }
    el.innerHTML = "<span><span class=\"alert-title\">Não foi possível carregar os dados</span>" + esc(msg) + ". Se abriu o arquivo direto do computador, use um servidor local (python3 -m http.server) ou o endereço publicado.</span>";
  }

  /* Tabela acessível equivalente a um gráfico.
     alvo: id do container; cab: array de cabeçalhos; linhas: array de arrays (valores já formatados ou null). */
  function tabelaDados(alvo, cab, linhas, titulo) {
    var el = document.getElementById(alvo); if (!el) return;
    var html = '<details class="tabela-dados"><summary>' + esc(titulo || "Ver os dados deste gráfico em tabela") + '</summary><div class="tabela-rolagem"><table class="table-dados"><thead><tr>';
    cab.forEach(function (c) { html += "<th scope=\"col\">" + esc(c) + "</th>"; });
    html += "</tr></thead><tbody>";
    linhas.forEach(function (l) {
      html += "<tr>";
      l.forEach(function (v, i) {
        var s = (v === null || v === undefined) ? '<span class="sem-dado">sem dado</span>' : esc(v);
        html += (i === 0 ? '<th scope="row">' : "<td>") + s + (i === 0 ? "</th>" : "</td>");
      });
      html += "</tr>";
    });
    html += "</tbody></table></div></details>";
    el.innerHTML = html;
  }

  function baixarCSV(nome, linhas) {
    var blob = new Blob(["﻿" + linhas.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = nome; a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  }
  function csvNum(v) { return (v === null || v === undefined) ? "" : String(v).replace(".", ","); }

  /* Gráficos: opções padrão sobre chart-defaults.js */
  function opcoesBase(extra) {
    var o = { responsive: true, maintainAspectRatio: false, spanGaps: false,
      interaction: { mode: "index", intersect: false },
      plugins: { legend: { position: "bottom", labels: { usePointStyle: true, boxWidth: 8 } } },
      elements: { line: { borderWidth: 2.5, tension: 0.2 }, point: { radius: 4, hoverRadius: 7, borderWidth: 2, backgroundColor: temaAtual() === "dark" ? "#112536" : "#fff" }, bar: { borderRadius: 6, borderSkipped: "bottom" } } };
    return mescla(o, extra || {});
  }
  function mescla(a, b) {
    Object.keys(b).forEach(function (k) {
      if (b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) && a[k] && typeof a[k] === "object") mescla(a[k], b[k]);
      else a[k] = b[k];
    });
    return a;
  }
  function pinta(datasets) {
    return datasets.map(function (d, i) {
      var c = d.cor || PALETA[i % PALETA.length];
      return mescla({ borderColor: c, backgroundColor: d.type === "line" || d.fill === false ? c : c, pointBorderColor: c }, d);
    });
  }
  var graficos = [];
  function grafico(id, cfg) {
    var el = document.getElementById(id); if (!el || typeof Chart === "undefined") return null;
    cfg.data.datasets = pinta(cfg.data.datasets);
    cfg.options = opcoesBase(cfg.options);
    var g = new Chart(el.getContext("2d"), cfg);
    graficos.push(g);
    return g;
  }

  /* Tema claro/escuro: tokens do UFMS Design System via [data-theme="dark"] no <html>.
     A escolha fica no localStorage (conveniência por navegador); sem escolha, segue o sistema. */
  function temaAtual() { return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light"; }
  function aplicaTemaGraficos() {
    if (typeof Chart === "undefined") return;
    var escuro = temaAtual() === "dark";
    Chart.defaults.color = escuro ? "#C4CDD5" : "#1A1A1A";
    Chart.defaults.borderColor = escuro ? "rgba(255,255,255,0.10)" : "#E0E5EA";
    Chart.defaults.scale.grid.color = escuro ? "rgba(255,255,255,0.08)" : "rgba(0,136,183,0.10)";
    Chart.defaults.scale.ticks.color = escuro ? "#9AA5B1" : "#616E7C";
    Chart.defaults.plugins.tooltip.backgroundColor = escuro ? "rgba(17,37,54,0.97)" : "rgba(0,34,51,0.95)";
    graficos.forEach(function (g) {
      g.options.scales && Object.keys(g.options.scales).forEach(function (k) {
        var sc = g.options.scales[k]; sc.grid = sc.grid || {}; sc.ticks = sc.ticks || {};
        sc.grid.color = Chart.defaults.scale.grid.color; sc.ticks.color = Chart.defaults.scale.ticks.color;
      });
      if (g.options.plugins && g.options.plugins.legend) { g.options.plugins.legend.labels = g.options.plugins.legend.labels || {}; g.options.plugins.legend.labels.color = Chart.defaults.color; }
      g.data.datasets.forEach(function (d) { if (d.pointBackgroundColor === undefined || d.pointBackgroundColor === "#fff" || d.pointBackgroundColor === "#112536") d.pointBackgroundColor = escuro ? "#112536" : "#fff"; });
      g.update("none");
    });
  }
  function defineTema(t, guardar) {
    document.documentElement.setAttribute("data-theme", t);
    if (guardar) { try { localStorage.setItem("csa-tema", t); } catch (e) {} }
    var b = document.querySelector(".csa-tema");
    if (b) { b.setAttribute("aria-pressed", t === "dark" ? "true" : "false"); b.setAttribute("title", t === "dark" ? "Mudar para tema claro" : "Mudar para tema escuro"); }
    aplicaTemaGraficos();
  }
  // Plugin: linhas de corte horizontais (2,50 e 3,50) em gráficos de média
  var cortes = { id: "cortesCPA", afterDraw: function (chart, args, opts) {
    if (!opts || !opts.eixo) return;
    var y = chart.scales[opts.eixo === "x" ? "x" : "y"]; if (!y) return;
    var ctx = chart.ctx, area = chart.chartArea;
    [[CORTE_FRAG, COR.frag], [CORTE_OPORT, COR.oport]].forEach(function (p) {
      ctx.save(); ctx.strokeStyle = p[1]; ctx.setLineDash([4, 4]); ctx.lineWidth = 1; ctx.globalAlpha = 0.7; ctx.beginPath();
      if (opts.eixo === "x") { var x = y.getPixelForValue(p[0]); ctx.moveTo(x, area.top); ctx.lineTo(x, area.bottom); }
      else { var yy = y.getPixelForValue(p[0]); ctx.moveTo(area.left, yy); ctx.lineTo(area.right, yy); }
      ctx.stroke(); ctx.restore();
    });
  } };
  if (typeof Chart !== "undefined") Chart.register(cortes);

  /* Filtros de série: checkboxes com data-serie="<índice>" ligados ao gráfico */
  function ligaFiltros(container, chart) {
    var el = document.getElementById(container); if (!el || !chart) return;
    el.querySelectorAll("input[type=checkbox][data-serie]").forEach(function (cb) {
      var i = parseInt(cb.getAttribute("data-serie"), 10);
      chart.setDatasetVisibility(i, cb.checked);
      cb.addEventListener("change", function () { chart.setDatasetVisibility(i, cb.checked); chart.update(); });
    });
    chart.update();
  }

  /* Navegação */
  function nav() {
    var bt = document.querySelector(".csa-tema");
    if (bt) bt.addEventListener("click", function () { defineTema(temaAtual() === "dark" ? "light" : "dark", true); });
    defineTema(temaAtual(), false);
    if (window.matchMedia) window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
      var salvo = null; try { salvo = localStorage.getItem("csa-tema"); } catch (x) {}
      if (!salvo) defineTema(e.matches ? "dark" : "light", false);
    });
    var t = document.querySelector(".csa-nav-toggle"), n = document.querySelector(".csa-nav");
    if (t && n) t.addEventListener("click", function () { var aberta = n.classList.toggle("aberta"); t.setAttribute("aria-expanded", aberta ? "true" : "false"); });
    var pagina = document.body.getAttribute("data-pagina");
    document.querySelectorAll(".csa-nav a[data-pagina]").forEach(function (a) {
      if (a.getAttribute("data-pagina") === pagina) a.setAttribute("aria-current", "page");
    });
    var ano = document.getElementById("ano-atual"); if (ano) ano.textContent = new Date().getFullYear();
    linksExternos(document);
  }
  function linksExternos(raiz) {
    (raiz || document).querySelectorAll("a[href^='http']").forEach(function (a) {
      if (a.host === location.host) return;
      a.setAttribute("target", "_blank"); a.setAttribute("rel", "noopener noreferrer");
      if (!a.querySelector(".visually-hidden")) { var sp = document.createElement("span"); sp.className = "visually-hidden"; sp.textContent = " (abre em nova aba)"; a.appendChild(sp); }
    });
  }
  document.addEventListener("DOMContentLoaded", nav);

  window.CSA = { PALETA: PALETA, COR: COR, fmtNum: fmtNum, fmtPct: fmtPct, fmtInt: fmtInt, classe: classe, semaforo: semaforo,
    legendaSemaforo: legendaSemaforo, esc: esc, loadJSON: loadJSON, carregar: carregar, erro: erro, tabelaDados: tabelaDados,
    baixarCSV: baixarCSV, csvNum: csvNum, grafico: grafico, ligaFiltros: ligaFiltros, mescla: mescla, defineTema: defineTema, temaAtual: temaAtual, linksExternos: linksExternos };
})();
