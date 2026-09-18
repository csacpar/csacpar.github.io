/* ============================================================
   UFMS Chart Defaults — paleta institucional para Chart.js
   Uso:
     <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
     <script src="chart-defaults.js"></script>
     // ...todos os new Chart() já saem com fontes e paletas UFMS
   ============================================================ */
(function () {
  if (typeof window === "undefined" || typeof window.Chart === "undefined") return;

  const C = window.Chart;

  // Paleta categórica oficial (ordem de preferência)
  const CATEGORICAL = [
    "#0088B7", // azul UFMS
    "#00A859", // verde bandeira
    "#FFCD00", // amarelo
    "#001F5F", // azul marinho
    "#F57C00", // warning
    "#66BDDB", // primary-300
    "#7B8794", // gray
    "#D32F2F"  // danger
  ];

  // Sequencial azul UFMS (para heatmaps e medidas crescentes)
  const SEQUENTIAL = [
    "#E6F4F9", "#CCE9F3", "#99D3E7", "#66BDDB", "#33A3C8",
    "#0088B7", "#006A8F", "#005273", "#003A52"
  ];

  // Divergente (negativo ⇄ positivo)
  const DIVERGENT = [
    "#811919", "#D32F2F", "#F8B4B4", "#F5F7F9",
    "#99D3E7", "#0088B7", "#002233"
  ];

  // Fontes e cores
  C.defaults.font.family = "'Inter','Segoe UI',system-ui,sans-serif";
  C.defaults.font.size   = 12;
  C.defaults.color       = "#1A1A1A";
  C.defaults.borderColor = "#E0E5EA";

  // Animação respeitando reduced-motion
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    C.defaults.animation = false;
  } else {
    C.defaults.animation = { duration: 600, easing: "easeOutCubic" };
  }

  // Plugins padrões
  C.defaults.plugins.legend.labels.font = { family: "'Inter',sans-serif", size: 12, weight: 500 };
  C.defaults.plugins.tooltip.backgroundColor = "rgba(0,34,51,0.95)";
  C.defaults.plugins.tooltip.titleFont = { family: "'Poppins',sans-serif", weight: 700, size: 13 };
  C.defaults.plugins.tooltip.bodyFont  = { family: "'Inter',sans-serif", size: 12 };
  C.defaults.plugins.tooltip.padding   = 10;
  C.defaults.plugins.tooltip.cornerRadius = 8;
  C.defaults.plugins.tooltip.titleColor = "#66BDDB";
  C.defaults.plugins.tooltip.borderColor = "rgba(102,189,219,0.30)";
  C.defaults.plugins.tooltip.borderWidth = 1;

  // Eixos com grid sutil
  C.defaults.scale.grid.color = "rgba(0, 136, 183, 0.10)";
  C.defaults.scale.grid.drawTicks = false;
  C.defaults.scale.ticks.color = "#616E7C";
  C.defaults.scale.ticks.padding = 8;

  // Expor helpers no namespace UFMS
  window.UFMSChart = {
    categorical: CATEGORICAL.slice(),
    sequential:  SEQUENTIAL.slice(),
    divergent:   DIVERGENT.slice(),

    // Aplica paleta categórica em uma lista de datasets
    paint(datasets, { palette = "categorical", alpha } = {}) {
      const p = this[palette] || this.categorical;
      return datasets.map((d, i) => {
        const c = p[i % p.length];
        const fill = alpha != null ? hexToRgba(c, alpha) : c;
        return { ...d, backgroundColor: d.backgroundColor || fill, borderColor: d.borderColor || c };
      });
    },

    // Cria gradiente azul-UFMS (use no chart.js context)
    blueGradient(ctx, { from = "#0088B7", to = "rgba(0,136,183,0.05)" } = {}) {
      const grad = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
      grad.addColorStop(0, from);
      grad.addColorStop(1, to);
      return grad;
    }
  };

  function hexToRgba(hex, a) {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return m ? `rgba(${parseInt(m[1],16)},${parseInt(m[2],16)},${parseInt(m[3],16)},${a})` : hex;
  }
})();
