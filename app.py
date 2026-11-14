"""VoxGuard - single-file app (Member 3). Run: streamlit run app.py"""
# ================= STYLE =================
# VoxGuard styling + hero visual (Member 3)
LIGHT = dict(bg="#f4f6fb", surf="#ffffff", surf2="#e9eef7", ink="#12151f", mute="#5d6678", accent="#2f5bff", vio="#8b5cf6", line="#dbe2ee")
DARK = dict(bg="#07080d", surf="#10121a", surf2="#181b26", ink="#f3f1ea", mute="#9a9fb0", accent="#d4af6a", vio="#9b7bff", line="#232736")

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
