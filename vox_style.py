"""VoxGuard styling + hero visual (Member 3)."""
LIGHT = dict(bg="#f4f6fb", surf="#ffffff", surf2="#e9eef7", ink="#12151f", mute="#5d6678", accent="#2f5bff", vio="#8b5cf6", line="#dbe2ee")
DARK = dict(bg="#0b0e17", surf="#141926", surf2="#1b2233", ink="#eef1f8", mute="#99a3b8", accent="#6b8cff", vio="#a78bfa", line="#273049")

def css(t):
    v = "".join(f"--{k}:{x};" for k, x in t.items())
    return f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif&display=swap');
:root{{{v}}}
html,body,[class*="css"],.stApp{{font-family:'Inter',sans-serif;color:var(--ink)}}
.stApp{{background:radial-gradient(900px 500px at 85% -10%,color-mix(in srgb,var(--vio) 18%,transparent),transparent),var(--bg)}}
#MainMenu,footer,header[data-testid="stHeader"]{{visibility:hidden;height:0}}
.block-container{{max-width:1180px;padding:1rem 1.2rem 4rem}}
h1,h2,h3{{font-family:'Instrument Serif',serif!important;font-weight:400!important;letter-spacing:-.01em;color:var(--ink)}}
h2{{font-size:2.4rem!important}} p,li,label,span{{color:inherit}}
.brand{{font-weight:600;letter-spacing:.28em;font-size:.95rem}} .brand b{{color:var(--accent)}}
.eyebrow{{color:var(--accent);font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;font-weight:600}}
.mute{{color:var(--mute)}}
.card{{background:var(--surf);border:1px solid var(--line);border-radius:22px;padding:1.3rem 1.4rem;animation:up .6s both;transition:transform .25s,box-shadow .25s}}
.card:hover{{transform:translateY(-3px);box-shadow:0 18px 40px -22px var(--accent)}}
.hero-t{{font-family:'Instrument Serif',serif;font-size:clamp(2.6rem,7vw,5rem);line-height:1.02;margin:.3rem 0 1rem}}
.hero-t span{{background:linear-gradient(100deg,var(--accent),var(--vio),var(--accent));background-size:200%;-webkit-background-clip:text;color:transparent;animation:flow 6s linear infinite}}
.big{{font-family:'Instrument Serif',serif;font-size:2.2rem;line-height:1.1}}
.bar{{height:10px;border-radius:99px;background:var(--surf2);overflow:hidden;margin:.35rem 0 1rem}}
.bar i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--vio));animation:grow 1s both}}
.pill{{display:inline-block;padding:.25rem .8rem;border-radius:99px;background:var(--surf2);font-size:.78rem;margin:.15rem .2rem .15rem 0}}
.step{{flex:1;min-width:150px;position:relative}} .flow{{display:flex;gap:.8rem;flex-wrap:wrap}}
.num{{font-family:'Instrument Serif',serif;font-size:2.4rem;color:var(--accent)}}
.status{{border-left:4px solid var(--vio);background:var(--surf2);padding:1rem 1.2rem;border-radius:14px}}
div[data-testid="stRadio"]>div{{flex-direction:row;gap:.3rem;overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;padding:.3rem}}
div[data-testid="stRadio"] label{{background:var(--surf);border:1px solid var(--line);border-radius:99px;padding:.35rem .95rem;white-space:nowrap;cursor:pointer;transition:.2s}}
div[data-testid="stRadio"] label:hover{{border-color:var(--accent);transform:translateY(-1px)}}
div[data-testid="stRadio"] label:has(input:checked){{background:var(--ink);color:var(--bg)}}
div[data-testid="stRadio"] label>div:first-child{{display:none}}
.stButton>button,.stDownloadButton>button{{border-radius:99px;border:1px solid var(--line);background:var(--surf);color:var(--ink);padding:.55rem 1.3rem;font-weight:500;transition:.25s}}
.stButton>button:hover{{background:linear-gradient(100deg,var(--accent),var(--vio));color:#fff;border-color:transparent;transform:translateY(-2px)}}
div[data-testid="stFileUploader"] section{{border:2px dashed var(--line);border-radius:26px;background:var(--surf);padding:2.2rem 1rem;transition:.25s}}
div[data-testid="stFileUploader"] section:hover{{border-color:var(--accent);background:var(--surf2)}}
.stProgress>div>div>div{{background:linear-gradient(90deg,var(--accent),var(--vio))}}
@keyframes up{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
@keyframes flow{{to{{background-position:200%}}}} @keyframes grow{{from{{width:0}}}}
@media(max-width:640px){{.block-container{{padding:.6rem .8rem 4rem}}h2{{font-size:1.8rem!important}}.card{{padding:1rem}}.step{{min-width:100%}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style>"""

def hero(t):
    a, v, i = t["accent"], t["vio"], t["ink"]
    paths = "".join(f'<path class="w w{n}" d="M-400 {200+n*0} Q-300 {120-n*18} -200 200 T0 200 T200 200 T400 200 T600 200 T800 200 T1000 200" fill="none" stroke="url(#g)" stroke-width="{3-n*.6}" opacity="{.9-n*.22}"/>' for n in range(3))
    bars = "".join(f'<rect x="{150+k*22}" y="{200-10}" width="10" rx="5" height="20" fill="url(#g)" class="b" style="animation-delay:{k*.07:.2f}s"/>' for k in range(25))
    return f"""<div style="height:440px"><svg viewBox="0 0 800 400" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{v}"/></linearGradient>
<radialGradient id="o"><stop offset="0" stop-color="{v}" stop-opacity=".35"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>
<circle cx="400" cy="200" r="190" fill="url(#o)" class="p"/><circle cx="400" cy="200" r="130" fill="none" stroke="{a}" stroke-opacity=".25" class="p2"/>
{bars}{paths}
<g transform="translate(400 200)"><rect x="-30" y="-78" width="60" height="110" rx="30" fill="{i}" opacity=".92"/>
<path d="M-48 0v10a48 48 0 0 0 96 0V0" fill="none" stroke="{i}" stroke-width="6" stroke-linecap="round"/><path d="M0 58v34M-24 92h48" stroke="{i}" stroke-width="6" stroke-linecap="round"/>
<g stroke="#fff" stroke-opacity=".35" stroke-width="3"><path d="M-18 -50h36M-18 -34h36M-18 -18h36M-18 -2h36"/></g></g></svg>
<style>svg{{overflow:visible}}.w{{animation:m 9s linear infinite}}.w1{{animation-duration:13s}}.w2{{animation-duration:17s;animation-direction:reverse}}
@keyframes m{{to{{transform:translateX(-200px)}}}}.b{{transform-box:fill-box;transform-origin:center;animation:e 1.4s ease-in-out infinite}}
@keyframes e{{0%,100%{{transform:scaleY(.4)}}50%{{transform:scaleY(5)}}}}.p{{transform-origin:400px 200px;animation:pu 4s ease-in-out infinite}}
.p2{{transform-origin:400px 200px;animation:pu 4s 1s ease-in-out infinite}}@keyframes pu{{50%{{transform:scale(1.08)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style></div>"""
