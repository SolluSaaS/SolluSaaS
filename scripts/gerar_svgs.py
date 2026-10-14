"""Gera os SVGs do README do perfil SolluSaaS, em versão escura e clara."""
import math, random, sys, os

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
GLYPHS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789Z:・.=*+-<>¦｜"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#0d1117", border="#30363d", text="#e6edf3", sub="#8b949e",
                 acc="#3fb950", dim="#2ea043", faint="#1c3324", head="#aff5b4", mid="#2ea043",
                 tail="#1b4d2c", user="#79c0ff", path="#d2a8ff", bar="#161b22", veil=".55"),
    "light": dict(bg="#ffffff", panel="#ffffff", border="#d0d7de", text="#1f2328", sub="#59636e",
                  acc="#1a7f37", dim="#2da44e", faint="#dafbe1", head="#116329", mid="#4ac26b",
                  tail="#b4e8c2", user="#0969da", path="#8250df", bar="#f6f8fa", veil=".6"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rain(t, w, h, cols, size, seed):
    rnd = random.Random(seed)
    out, step, n = [], w / cols, int(h / size) + 2
    for c in range(cols):
        x = c * step + step / 2
        dur = rnd.uniform(4, 10)
        delay = -rnd.uniform(0, dur)
        chars = []
        for i in range(n):
            g = esc(rnd.choice(GLYPHS))
            k = i / n
            fill = t["head"] if i == n - 1 else (t["acc"] if k > .75 else t["mid"] if k > .4 else t["tail"])
            chars.append(f'<text x="{x:.1f}" y="{i*size}" fill="{fill}">{g}</text>')
        out.append(f'<g class="col" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s">'
                   + "".join(chars) + "</g>")
    return (f'<g font-size="{size}" text-anchor="middle" font-family="{FONT}">' + "".join(out) + "</g>")


def fall_css(h):
    return (".col { animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }"
            f" @keyframes fall {{ from {{ transform: translateY(-{h+40}px); }} to {{ transform: translateY({h+40}px); }} }}")


def frame(t, w, h):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{t["border"]}"/>'


def kt(times, total):
    return ";".join(f"{x/total:.5f}" for x in times)


def header(t):
    W, H = 1200, 340
    lines = ["Solution is more than software.", "Estratégia, processos, automação e IA.",
             "Vibe coder: dono das ideias, piloto da IA.", "Eu sei Kung Fu."]
    cycle = 4.5 * len(lines)
    typing = []
    for i, ln in enumerate(lines):
        n = len(ln); width = n * 13.8; x0 = 600 - width / 2; start = i * 4.5
        times, vals = [0, start], [0, 0]
        for j in range(1, n + 1):
            times.append(start + 1.6 * j / n); vals.append(width * j / n)
        times += [start + 4.0, start + 4.25]; vals += [width, 0]
        if times[-1] < cycle:
            times.append(cycle); vals.append(0)
        k = kt(times, cycle); v = ";".join(f"{x:.1f}" for x in vals)
        cx = ";".join(f"{x0 + x:.1f}" for x in vals)
        typing.append(f'''
  <clipPath id="t{i}"><rect x="{x0:.1f}" y="220" height="40" width="0">
    <animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{k}" values="{v}"/></rect></clipPath>
  <text x="{x0:.1f}" y="250" clip-path="url(#t{i})" class="typed">{esc(ln)}</text>
  <rect y="228" width="12" height="26" fill="{t['acc']}" opacity="0">
    <animate attributeName="x" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{k}" values="{cx}"/>
    <animate attributeName="opacity" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{start/cycle:.5f};{(start+4.25)/cycle:.5f}" values="0;1;0"/></rect>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Renatho Siqueira, CTO da NMK. Solution is more than software.">
<style>
  {fall_css(H)}
  .name {{ font: 700 64px {FONT}; fill: {t['text']}; letter-spacing: 2px; }}
  .role {{ font: 600 20px {FONT}; fill: {t['acc']}; letter-spacing: 4px; }}
  .typed {{ font: 500 23px {FONT}; fill: {t['acc']}; }}
  .glitch {{ animation: glitch 6s infinite steps(1); }}
  @keyframes glitch {{ 0%,92%,100% {{ transform: translate(0,0); opacity:1 }} 93% {{ transform: translate(-3px,1px); opacity:.8 }} 95% {{ transform: translate(3px,-1px); }} 97% {{ transform: translate(-1px,0); opacity:.9 }} }}
</style>
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{t['bg']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{t['bg']}" stop-opacity="{t['veil']}"/>
    <stop offset="1" stop-color="{t['bg']}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{t['bg']}"/>
  {rain(t, W, H, 60, 16, 7)}
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <rect x="150" y="70" width="900" height="210" rx="14" fill="{t['panel']}" fill-opacity=".86" stroke="{t['border']}"/>
  <text x="600" y="112" text-anchor="middle" class="role">CTO · NMK · BARUERI, SP</text>
  <g class="glitch"><text x="600" y="185" text-anchor="middle" class="name" filter="url(#glow)">RENATHO SIQUEIRA</text></g>
  {''.join(typing)}
</g>
{frame(t, W, H)}
</svg>'''


def whoami(t):
    rows = [("whoami", "Renatho Siqueira, o Nunes. Renatho com H."),
            ("cat cargo.txt", "CTO da NMK: soluções estratégicas para PMEs em Portugal e no Brasil."),
            ("cat stack-mental.txt", "Estratégia > processo > automação > software. Nessa ordem."),
            ("uptime", "35+ anos em tecnologia. Começou aos 13. Profissional desde os 16."),
            ("echo $LEMA", "Stay hungry, stay foolish.")]
    CW, PRE, X = 9.6, 13, 28
    TW, TH = 900, 60 + 30 * (2 * len(rows) + 1) + 20
    # linha do tempo de cada comando
    events, tcur = [], 0.8
    for cmd, out in rows:
        s = tcur; e = s + 0.06 * len(cmd)
        events.append((s, e, e + 0.35))  # início, fim da digitação, saída aparece
        tcur = e + 1.0
    final = tcur
    T = final + 4.0
    clear = T - 0.4
    parts = []
    prompt = (f'<tspan fill="{t["user"]}">nunes@nmk</tspan><tspan fill="{t["sub"]}">:</tspan>'
              f'<tspan fill="{t["path"]}">~</tspan><tspan fill="{t["sub"]}">$ </tspan>')
    for i, ((cmd, out), (s, e, o)) in enumerate(zip(rows, events)):
        y = 82 + 2 * i * 30
        full = (PRE + len(cmd)) * CW + 4
        times, vals = [0, s], [PRE * CW, PRE * CW]
        for j in range(1, len(cmd) + 1):
            times.append(s + (e - s) * j / len(cmd)); vals.append((PRE + j) * CW)
        times += [clear, T]; vals += [full, PRE * CW]
        # o prompt da linha só aparece quando chega a vez dela
        times = [0] + times[1:];
        k = kt(times, T); v = ";".join(f"{x:.1f}" for x in vals)
        parts.append(f'''<clipPath id="c{i}"><rect x="{X}" y="{y-20}" height="28" width="0">
  <animate attributeName="width" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{k}" values="{v}"/></rect></clipPath>
<g opacity="0"><animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{s/T:.5f};{clear/T:.5f}" values="0;1;0"/>
  <text x="{X}" y="{y}" fill="{t['acc']}" clip-path="url(#c{i})">{prompt}{esc(cmd)}</text></g>
<g class="blink"><rect y="{y-16}" width="10" height="20" fill="{t['acc']}" opacity="0">
  <animate attributeName="x" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{k}" values="{';'.join(f'{X + x:.1f}' for x in vals)}"/>
  <animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{s/T:.5f};{o/T:.5f}" values="0;1;0"/></rect></g>
<text x="{X}" y="{y+30}" fill="{t['text']}" opacity="0">{esc(out)}
  <animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{o/T:.5f};{clear/T:.5f}" values="0;1;0"/></text>''')
    yl = 82 + 2 * len(rows) * 30
    parts.append(f'''<g opacity="0"><animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{final/T:.5f};{clear/T:.5f}" values="0;1;0"/>
<text x="{X}" y="{yl}">{prompt}</text><rect class="blink" x="{X + PRE*CW:.1f}" y="{yl-16}" width="10" height="20" fill="{t['acc']}"/></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TW} {TH}" width="{TW}" height="{TH}" role="img" aria-label="Terminal: whoami. Renatho Siqueira, CTO da NMK, 35+ anos em tecnologia. Stay hungry, stay foolish.">
<style>text {{ font: 16px {FONT}; }} .blink {{ animation: b 1s steps(1) infinite; }} @keyframes b {{ 50% {{ opacity: 0; }} }}</style>
<rect width="{TW}" height="{TH}" rx="14" fill="{t['bg']}"/>
<path d="M0 14 a14 14 0 0 1 14 -14 h{TW-28} a14 14 0 0 1 14 14 v24 h-{TW} z" fill="{t['bar']}"/>
<line x1="0" y1="38" x2="{TW}" y2="38" stroke="{t['border']}"/>
<circle cx="24" cy="19" r="6.5" fill="#ff5f57"/><circle cx="46" cy="19" r="6.5" fill="#febc2e"/><circle cx="68" cy="19" r="6.5" fill="#28c840"/>
<text x="{TW/2}" y="24" text-anchor="middle" fill="{t['sub']}" style="font-size:13px">nunes@nmk: ~ (zion)</text>
{''.join(parts)}
{frame(t, TW, TH)}
</svg>'''


def trajetoria(t):
    steps = [("13 anos", "O primeiro código", "a tecnologia vira caminho"),
             ("16–17", "Profissional", "agências e software houses"),
             ("SEO", "Professor de SEO", "nasce o Renatho com H"),
             ("QA", "Quality assurance", "software houses"),
             ("Gestão", "Líder de times", "marketing, dev e estratégia"),
             ("Hoje", "CTO da NMK", "produtos com IA")]
    GW, GH = 1200, 300
    x0, x1, ly = 150, 1050, 150
    L, DASH, T, RUN = x1 - x0, 90, 6.0, 4.2
    nodes = []
    for i, (tag, title, sub) in enumerate(steps):
        x = x0 + L * i / (len(steps) - 1)
        last = i == len(steps) - 1
        r = 13 if last else 10
        hit = RUN * ((x - x0) + 6) / (L + DASH)  # quando a ponta do laser chega
        a, b, c = hit / T, min(hit + .12, T) / T, min(hit + .7, T - .01) / T
        flash = (f'<circle cx="{x:.0f}" cy="{ly}" r="{r}" fill="none" stroke="{t["acc"]}" stroke-width="2" opacity="0">'
                 f'<animate attributeName="r" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.4f};{c:.4f};1" values="{r};{r};{r+20};{r+20}"/>'
                 f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.4f};{b:.4f};{c:.4f};1" values="0;0;1;0;0"/></circle>')
        core = (f'<circle cx="{x:.0f}" cy="{ly}" r="{r-6}" fill="{t["acc"]}">'
                f'<animate attributeName="r" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.4f};{b:.4f};{c:.4f};1" values="{r-6};{r-6};{r-2};{r-6};{r-6}"/></circle>')
        up = i % 2 == 0
        ty = ly - 52 if up else ly + 62
        nodes.append(f'''<g>{flash}<circle cx="{x:.0f}" cy="{ly}" r="{r}" fill="{t['bg']}" stroke="{t['acc']}" stroke-width="3"/>{core}
  <text x="{x:.0f}" y="{ly + (34 if up else -26)}" text-anchor="middle" class="tag">{esc(tag)}</text>
  <text x="{x:.0f}" y="{ty}" text-anchor="middle" class="t">{esc(title)}</text>
  <text x="{x:.0f}" y="{ty + 22}" text-anchor="middle" class="s">{esc(sub)}</text></g>''')
    run = RUN / T
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW} {GH}" width="{GW}" height="{GH}" role="img" aria-label="Trajetória: o primeiro código aos 13 anos, profissional aos 16, professor de SEO, quality assurance, líder de times e hoje CTO da NMK.">
<style>
  .t {{ font: 700 18px {FONT}; fill: {t['text']}; }} .s {{ font: 14px {FONT}; fill: {t['sub']}; }}
  .tag {{ font: 600 13px {FONT}; fill: {t['acc']}; letter-spacing: 1px; }}
  .h {{ font: 600 14px {FONT}; fill: {t['dim']}; letter-spacing: 6px; }}
</style>
<defs>
  <linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="{t['acc']}" stop-opacity="0"/><stop offset="1" stop-color="{t['head']}"/></linearGradient>
  <filter id="laser" filterUnits="userSpaceOnUse" x="0" y="{ly-40}" width="{GW}" height="80"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{GW}" height="{GH}" rx="14" fill="{t['bg']}"/>
<text x="30" y="34" class="h">// TRAJETÓRIA</text>
<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{t['faint']}" stroke-width="4" stroke-linecap="round"/>
<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{t['head']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="{DASH} {L + DASH}" filter="url(#laser)">
  <animate attributeName="stroke-dashoffset" dur="{T}s" repeatCount="indefinite" keyTimes="0;{run:.4f};1" values="{DASH};{-L};{-L}"/>
  <animate attributeName="stroke-width" dur=".35s" repeatCount="indefinite" values="3;6;3"/>
  <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{run:.4f};{run+.02:.4f};1" values="1;1;0;0"/>
</line>
{''.join(nodes)}
{frame(t, GW, GH)}
</svg>'''


def maturidade(t):
    areas = [("Produto e UX", 7), ("Infra e operação", 7), ("Arquitetura", 7), ("Diagnóstico", 5),
             ("Pilotar a IA", 7), ("Segurança", 5), ("Escopo", 7)]
    RW, RH, cx, cy, R = 600, 470, 300, 238, 150
    n = len(areas)
    def pt(i, v):
        a = -math.pi / 2 + 2 * math.pi * i / n
        return cx + R * v / 7 * math.cos(a), cy + R * v / 7 * math.sin(a)
    grid = []
    for lvl in range(1, 8):
        pts = " ".join(f"{pt(i, lvl)[0]:.1f},{pt(i, lvl)[1]:.1f}" for i in range(n))
        grid.append(f'<polygon points="{pts}" fill="none" stroke="{t["border"]}" stroke-width="{1 if lvl < 7 else 1.5}"/>')
    for i in range(n):
        x, y = pt(i, 7)
        grid.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["border"]}"/>')
    labels = []
    for i, (name, v) in enumerate(areas):
        x, y = pt(i, 8.3)
        anchor = "middle" if abs(x - cx) < 20 else ("start" if x > cx else "end")
        lvl = {7: "Sênior", 5: "Pleno"}[v]
        labels.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="l">{esc(name)}</text>'
                      f'<text x="{x:.1f}" y="{y+17:.1f}" text-anchor="{anchor}" class="v">{lvl} · {v}/7</text>')
    zero = " ".join(f"{cx},{cy}" for _ in range(n))
    full = " ".join(f"{pt(i, v)[0]:.1f},{pt(i, v)[1]:.1f}" for i, (_, v) in enumerate(areas))
    dots = "".join(f'<circle cx="{pt(i, v)[0]:.1f}" cy="{pt(i, v)[1]:.1f}" r="4.5" fill="{t["acc"]}"/>' for i, (_, v) in enumerate(areas))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {RW} {RH}" width="{RW}" height="{RH}" role="img" aria-label="Mapa de maturidade em vibe coding: Sênior em produto, infraestrutura, arquitetura, pilotar a IA e escopo; Pleno em diagnóstico e segurança.">
<style>
  .l {{ font: 600 14px {FONT}; fill: {t['text']}; }} .v {{ font: 12px {FONT}; fill: {t['acc']}; }}
  .h {{ font: 600 14px {FONT}; fill: {t['dim']}; letter-spacing: 6px; }} .f {{ font: 11px {FONT}; fill: {t['sub']}; }}
  .pulse {{ animation: p 3s ease-in-out infinite; }} @keyframes p {{ 50% {{ fill-opacity: .32; }} }}
</style>
<rect width="{RW}" height="{RH}" rx="14" fill="{t['bg']}"/>
<text x="24" y="34" class="h">// MATURIDADE</text>
{''.join(grid)}
<polygon class="pulse" points="{full}" fill="{t['acc']}" fill-opacity=".16" stroke="{t['acc']}" stroke-width="2.5" stroke-linejoin="round">
  <animate attributeName="points" from="{zero}" to="{full}" dur="1.2s" begin="0s" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/>
</polygon>
{dots}
{''.join(labels)}
<text x="{RW/2}" y="{RH-14}" text-anchor="middle" class="f">diário de maturidade com a IA · escala de 7 degraus · out/2026</text>
{frame(t, RW, RH)}
</svg>'''


def pilares(t):
    pillars = [("Estratégia empresarial", "o problema do negócio vem antes"),
               ("Processos de negócio", "mapear, simplificar, medir"),
               ("Automação", "n8n, Make, Typebot, Edge Functions"),
               ("Software sob medida com IA", "do PRD ao app em produção")]
    PW, PH, T = 600, 470, 8.0
    items = []
    for i, (title, sub) in enumerate(pillars):
        y = 80 + i * 92
        a = (0.3 + i * 0.5) / T; b = a + 1.0 / T
        items.append(f'''<text x="34" y="{y}" class="n">0{i+1}</text>
  <text x="80" y="{y}" class="t">{esc(title)}</text>
  <text x="80" y="{y+24}" class="s">{esc(sub)}</text>
  <rect x="80" y="{y+40}" width="480" height="4" rx="2" fill="{t['faint']}"/>
  <rect x="80" y="{y+40}" width="480" height="4" rx="2" fill="{t['acc']}">
    <animate attributeName="width" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.4f};{b:.4f};.9;1" values="0;0;480;480;0"/></rect>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img" aria-label="O que eu faço: estratégia empresarial, processos de negócio, automação e software sob medida com IA.">
<style>
  .t {{ font: 700 19px {FONT}; fill: {t['text']}; }} .s {{ font: 14px {FONT}; fill: {t['sub']}; }}
  .n {{ font: 700 22px {FONT}; fill: {t['acc']}; }} .h {{ font: 600 14px {FONT}; fill: {t['dim']}; letter-spacing: 6px; }}
  .q {{ font: italic 15px {FONT}; fill: {t['acc']}; }}
</style>
<rect width="{PW}" height="{PH}" rx="14" fill="{t['bg']}"/>
<text x="24" y="34" class="h">// O QUE EU FAÇO</text>
{''.join(items)}
<text x="{PW/2}" y="{PH-22}" text-anchor="middle" class="q">"Solution is more than software."</text>
{frame(t, PW, PH)}
</svg>'''


def footer(t):
    FW, FH = 1200, 150
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {FW} {FH}" width="{FW}" height="{FH}" role="img" aria-label="Preferimos ter perguntas sem respostas a respostas que não podem ser questionadas.">
<style>
  {fall_css(FH)}
  .q {{ font: italic 18px {FONT}; fill: {t['text']}; }} .a {{ font: 600 14px {FONT}; fill: {t['acc']}; letter-spacing: 3px; }}
</style>
<defs><clipPath id="c"><rect width="{FW}" height="{FH}" rx="14"/></clipPath>
<linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['bg']}" stop-opacity=".1"/><stop offset=".5" stop-color="{t['bg']}" stop-opacity=".85"/><stop offset="1" stop-color="{t['bg']}" stop-opacity=".1"/></linearGradient></defs>
<g clip-path="url(#c)"><rect width="{FW}" height="{FH}" fill="{t['bg']}"/>{rain(t, FW, FH, 60, 14, 42)}<rect width="{FW}" height="{FH}" fill="url(#f)"/></g>
<text x="{FW/2}" y="70" text-anchor="middle" class="q">"Preferimos ter perguntas sem respostas a respostas que não podem ser questionadas."</text>
<text x="{FW/2}" y="106" text-anchor="middle" class="a">STAY HUNGRY · STAY FOOLISH</text>
{frame(t, FW, FH)}
</svg>'''


for name, t in THEMES.items():
    for fn in (header, whoami, trajetoria, maturidade, pilares, footer):
        open(f"{OUT}/{fn.__name__}-{name}.svg", "w").write(fn(t))
print("ok")
