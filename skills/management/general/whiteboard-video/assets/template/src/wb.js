// Runtime de quadro branco: traços e escrita que se revelam no tempo, com uma caneta que acompanha.
var INK = "#20242b", GREEN = "#0a7d50", RED = "#c8381f", GRAY = "#566070", MARK = "#ffe36e", GOLD = "#ffc93d", BOARD = "#f7f6f1", NOTE = "#fff1a8";
var SVGNS = "http://www.w3.org/2000/svg";
var measureCtx = document.createElement("canvas").getContext("2d");

function norm(s) {
  return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]/g, "");
}

function makeScene(tl, cfg) {
  var root = document.getElementById("s" + cfg.id);
  var under = root.querySelector(".under"), ink = root.querySelector(".ink"), txt = root.querySelector(".txt"), er = root.querySelector(".er");
  var seed = 1000 + Number(cfg.id) * 97, cursor = 0, ops = [], pen = document.getElementById("pen");

  function r() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  function j(a) { return (r() - 0.5) * 2 * a; }
  function abs(t) { return cfg.start + t; }

  function linePts(x1, y1, x2, y2, a) {
    a = a === undefined ? 3 : a;
    var n = Math.max(2, Math.round(Math.hypot(x2 - x1, y2 - y1) / 80));
    var d = "M" + (x1 + j(a)).toFixed(1) + " " + (y1 + j(a)).toFixed(1);
    for (var i = 1; i <= n; i++) {
      var t = i / n;
      d += " L" + (x1 + (x2 - x1) * t + j(a)).toFixed(1) + " " + (y1 + (y2 - y1) * t + j(a)).toFixed(1);
    }
    return d;
  }

  function addPath(d, o, layer) {
    var p = document.createElementNS(SVGNS, "path");
    p.setAttribute("d", d);
    p.setAttribute("stroke", o.color || INK);
    p.setAttribute("stroke-width", o.width || 6);
    p.setAttribute("fill", "none");
    p.setAttribute("stroke-linecap", "round");
    p.setAttribute("stroke-linejoin", "round");
    p.setAttribute("pathLength", "1");
    p.style.strokeDasharray = "1";
    (layer || ink).appendChild(p);
    return p;
  }

  function reveal(p, t, dur, ease) {
    tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 0.001 }, abs(t));
    tl.fromTo(p, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease: ease || "power1.inOut" }, abs(t));
  }

  var c = {
    INK: INK, GREEN: GREEN, RED: RED, GRAY: GRAY,
    // Instante em que a próxima ocorrência da palavra começa na narração.
    w: function (word) {
      var want = norm(word);
      for (var i = cursor; i < cfg.words.length; i++) {
        if (norm(cfg.words[i].w).indexOf(want) === 0) {
          cursor = i + 1;
          return cfg.lead + cfg.words[i].s;
        }
      }
      console.error("Cena " + cfg.id + ": palavra sem correspondência: " + word);
      return cfg.lead + (cursor < cfg.words.length ? cfg.words[cursor].s : cfg.voice);
    },
    draw: function (d, o, t) {
      o = o || {};
      var p = addPath(d, o, o.under ? under : ink);
      var len = p.getTotalLength();
      var dur = o.dur || Math.min(1.1, 0.2 + len / 2400);
      reveal(p, t, dur);
      if (!o.noPen) {
        var pts = [];
        for (var i = 0; i <= 10; i++) { var q = p.getPointAtLength((len * i) / 10); pts.push({ x: q.x, y: q.y }); }
        ops.push({ t: t, dur: dur, pts: pts });
      }
      return t + dur;
    },
    line: function (x1, y1, x2, y2, o, t) { o = o || {}; return c.draw(linePts(x1, y1, x2, y2, o.a), o, t); },
    rect: function (x, y, w, h, o, t) {
      o = o || {};
      var a = o.a === undefined ? 3 : o.a;
      var d = linePts(x - 3, y, x + w + 4, y + 1, a) + " " + linePts(x + w, y - 3, x + w + 1, y + h + 4, a) + " " + linePts(x + w + 3, y + h, x - 2, y + h - 1, a) + " " + linePts(x, y + h + 3, x + 1, y - 3, a);
      return c.draw(d, o, t);
    },
    arrow: function (x1, y1, x2, y2, o, t) {
      o = o || {};
      var ang = Math.atan2(y2 - y1, x2 - x1), L = o.head || 26;
      var d = linePts(x1, y1, x2, y2, 2) + " M" + (x2 - L * Math.cos(ang - 0.5)).toFixed(1) + " " + (y2 - L * Math.sin(ang - 0.5)).toFixed(1) + " L" + x2 + " " + y2 + " L" + (x2 - L * Math.cos(ang + 0.5)).toFixed(1) + " " + (y2 - L * Math.sin(ang + 0.5)).toFixed(1);
      return c.draw(d, o, t);
    },
    dashed: function (x1, y1, x2, y2, o, t) {
      o = o || {};
      var n = Math.max(2, Math.round(Math.hypot(x2 - x1, y2 - y1) / 44)), d = "";
      for (var i = 0; i < n; i++) {
        var a = i / n, b = (i + 0.58) / n;
        d += " M" + (x1 + (x2 - x1) * a + j(1)).toFixed(1) + " " + (y1 + (y2 - y1) * a + j(1)).toFixed(1) + " L" + (x1 + (x2 - x1) * b + j(1)).toFixed(1) + " " + (y1 + (y2 - y1) * b + j(1)).toFixed(1);
      }
      if (o.head !== 0) {
        var ang = Math.atan2(y2 - y1, x2 - x1), L = 24;
        d += " M" + (x2 - L * Math.cos(ang - 0.5)).toFixed(1) + " " + (y2 - L * Math.sin(ang - 0.5)).toFixed(1) + " L" + x2 + " " + y2 + " L" + (x2 - L * Math.cos(ang + 0.5)).toFixed(1) + " " + (y2 - L * Math.sin(ang + 0.5)).toFixed(1);
      }
      return c.draw(d, o, t);
    },
    circle: function (cx, cy, rx, ry, o, t) {
      o = o || {};
      var d = "", n = 40;
      for (var i = 0; i <= n + 3; i++) {
        var a = (i / n) * Math.PI * 2 - 1.2;
        d += (i ? " L" : "M") + (cx + (rx + j(2.5)) * Math.cos(a)).toFixed(1) + " " + (cy + (ry + j(2.5)) * Math.sin(a)).toFixed(1);
      }
      return c.draw(d, o, t);
    },
    text: function (x, y, s, o, t) {
      o = o || {};
      var size = o.size || 48, font = "700 " + size + "px Caveat";
      measureCtx.font = font;
      var w = measureCtx.measureText(s).width;
      var left = o.align === "center" ? x - w / 2 : o.align === "right" ? x - w : x;
      var el = document.createElement("div");
      el.className = "t";
      el.textContent = s;
      el.style.left = left.toFixed(1) + "px";
      el.style.top = y + "px";
      el.style.fontSize = size + "px";
      el.style.color = o.color || INK;
      txt.appendChild(el);
      var dur = o.dur || Math.min(1.4, 0.22 + s.length * 0.028);
      tl.fromTo(el, { clipPath: "inset(-20% 102% -20% -3%)" }, { clipPath: "inset(-20% -3% -20% -3%)", duration: dur, ease: "none" }, abs(t));
      var pts = [];
      for (var i = 0; i <= 12; i++) pts.push({ x: left + (w * i) / 12, y: y + size * (i % 2 ? 0.45 : 0.8) });
      ops.push({ t: t, dur: dur, pts: pts });
      if (o.mark) {
        var band = addPath(linePts(left - 6, y + size * 0.72, left + w + 6, y + size * 0.72, 1.2), { color: MARK, width: size * 0.5 }, under);
        reveal(band, t + dur, 0.35, "none");
      }
      return t + dur;
    },
    lines: function (x, y, list, o, t) {
      o = o || {};
      var size = o.size || 48, gap = o.gap || size * 1.08;
      list.forEach(function (s, i) { t = c.text(x, y + i * gap, s, o, t); });
      return t;
    },
    // Etiqueta de post-it. Código fica em letra de máquina para ser legível.
    note: function (x, y, s, o, t) {
      o = o || {};
      var el = document.createElement("div"), rot = o.rot === undefined ? -1.6 : o.rot;
      el.className = o.hand ? "note hand" : "note";
      el.textContent = s;
      el.style.left = x + "px";
      el.style.top = y + "px";
      if (o.size) el.style.fontSize = o.size + "px";
      if (o.width) { el.style.width = o.width + "px"; el.style.whiteSpace = "normal"; }
      txt.appendChild(el);
      tl.fromTo(el, { scale: 0.7, opacity: 0, rotation: rot - 4 }, { scale: 1, opacity: 1, rotation: rot, duration: 0.32, ease: "back.out(2)" }, abs(t));
      return t + 0.32;
    },
    box: function (x, y, w, h, labels, o, t) {
      o = o || {};
      t = c.rect(x, y, w, h, { color: o.color, width: o.width || 6, dur: o.dur || 0.45 }, t);
      labels = [].concat(labels);
      var size = o.size || 42, total = labels.length * size * 1.05, top = y + (h - total) / 2 - size * 0.02;
      labels.forEach(function (s, i) { t = c.text(x + w / 2, top + i * size * 1.05, s, { size: size, align: "center", color: o.textColor || o.color }, t); });
      return t;
    },
    title: function (s, t) {
      t = c.text(960, 34, s, { size: 90, align: "center" }, t);
      measureCtx.font = "700 90px Caveat";
      var w = measureCtx.measureText(s).width;
      return c.line(960 - w / 2 - 20, 134, 960 + w / 2 + 20, 137, { color: GOLD, width: 9, a: 2, noPen: true, under: true, dur: 0.4 }, t);
    },
    divider: function (t, y2) { return c.line(960, 172, 962, y2 || 1035, { color: "#9aa0a8", width: 5, a: 4, dur: 0.5, noPen: true }, t); },
    cross: function (x, y, w, h, o, t) {
      o = o || {};
      o.color = o.color || RED; o.width = o.width || 10; o.dur = 0.22;
      t = c.line(x, y, x + w, y + h, o, t);
      return c.line(x + w, y, x, y + h, o, t + 0.05);
    },
    check: function (x, y, o, t) {
      o = o || {};
      return c.draw("M" + x + " " + (y + 18) + " L" + (x + 14) + " " + (y + 34) + " L" + (x + 42) + " " + (y - 6), { color: o.color || GREEN, width: 8, dur: 0.22 }, t);
    },
    // Objeto que anda pelo quadro: o fio condutor da explicação. Mede 360x180 em escala 1.
    token: function (x, y, label, t, o) {
      o = o || {};
      var scale = o.scale || 1, el = document.createElement("div");
      el.className = "token";
      el.textContent = label;
      if (o.color) { el.style.color = o.color; el.style.borderColor = o.color; el.style.background = o.color === GREEN ? "#e2f4ea" : o.bg || "#ffffff"; }
      txt.appendChild(el);
      tl.fromTo(el, { x: x, y: y, scale: 0, opacity: 0 }, { x: x, y: y, scale: scale, opacity: 1, duration: 0.35, ease: "back.out(2)" }, abs(t));
      return el;
    },
    move: function (el, x, y, t, dur) {
      tl.to(el, { x: x, y: y, duration: dur || 0.6, ease: "power2.inOut" }, abs(t));
      return t + (dur || 0.6);
    },
    finish: function () {
      // Apaga o quadro no fim da cena; a próxima já começa limpa.
      var d = "M-160 40", rows = 6;
      for (var i = 0; i < rows; i++) {
        var y = 40 + i * 200;
        d += " L" + (i % 2 ? -160 : 2080) + " " + y + (i < rows - 1 ? " L" + (i % 2 ? -160 : 2080) + " " + (y + 200) : "");
      }
      // A última cena fica na tela: é o fechamento do vídeo.
      if (!cfg.last) reveal(addPath(d, { color: BOARD, width: 300 }, er), cfg.duration - 0.6, 0.55, "power1.inOut");
      ops.sort(function (a, b) { return a.t - b.t; });
      var penEnd = -1;
      ops = ops.filter(function (op) {
        if (op.t < penEnd) return false;
        penEnd = op.t + op.dur;
        return op.t + op.dur < cfg.duration - 0.6;
      });
      ops.forEach(function (op, i) {
        var next = ops[i + 1], at = abs(op.t), step = op.dur / (op.pts.length - 1);
        tl.set(pen, { x: op.pts[0].x, y: op.pts[0].y, opacity: 1 }, at);
        tl.to(pen, { keyframes: op.pts.slice(1).map(function (q) { return { x: q.x, y: q.y, duration: step, ease: "none" }; }) }, at);
        if (!next || next.t - (op.t + op.dur) > 0.35) tl.set(pen, { opacity: 0 }, at + op.dur + 0.2);
      });
    },
  };
  return c;
}
