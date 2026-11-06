// Uma função por cena, com a mesma numeração de narration.md. Os tempos vêm da fala (c.w).
var SCENES = {
  "01": function (c) {
    var t = c.title("O que é um webhook", c.w("Imagine"));
    var box = c.token(120, 300, "pacote", c.w("encomenda"), { scale: 0.7 });
    t = c.w("ligar");
    c.text(120, 500, "ligar de hora em hora", { size: 62, color: c.RED }, t);
    t = c.w("avise");
    c.text(120, 610, "pedir que avisem", { size: 62, color: c.GREEN }, t);
    c.check(590, 630, {}, t + 0.9);
    t = c.w("webhook");
    c.text(1300, 430, "webhook = aviso", { size: 84, align: "center", mark: true }, t);
    c.move(box, 1140, 560, t, 0.8);
  },

  "02": function (c) {
    var t = c.title("Consultar ou ser avisado", c.w("Consultar"));
    c.divider(t, 760);
    c.text(120, 180, "Consultar", { size: 72, color: c.RED }, t + 0.4);
    t = c.w("repetidas");
    [0, 1, 2].forEach(function (i) {
      c.arrow(150, 340 + i * 110, 700, 340 + i * 110, { color: c.GRAY, noPen: i > 0, dur: 0.35 }, t + i * 0.5);
      c.text(420, 280 + i * 110, "tem novidade?", { size: 44, align: "center", color: c.GRAY }, t + 0.2 + i * 0.5);
    });
    t = c.w("Com");
    c.text(1040, 180, "Webhook", { size: 72, color: c.GREEN }, t);
    t = c.w("POST");
    c.box(1040, 340, 260, 120, "sistema", { color: c.GREEN, size: 50 }, t);
    c.arrow(1310, 400, 1480, 400, { color: c.GREEN, width: 7 }, t + 0.6);
    c.box(1490, 340, 280, 120, "sua URL", { color: c.GREEN, size: 50 }, t + 0.9);
    c.note(1250, 500, "POST", { size: 28 }, t + 0.4);
    t = c.w("Menos");
    c.text(960, 840, "Menos trabalho dos dois lados", { size: 76, align: "center", mark: true }, t);
  },
};
