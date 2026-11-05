"""CSS + animated SVG robot. Robot states: welcome, listening, scanning, genuine, ai, neutral."""

CSS = """
<style>
.stApp{background:linear-gradient(180deg,#f4f7fb 0%,#e6ecf5 40%,#0b1530 40.1%,#0a1a3a 100%);}
.block-container{max-width:1150px;padding-top:1rem}
.nav{display:flex;gap:1.4rem;align-items:center;padding:.7rem 1.2rem;border-radius:14px;
 background:rgba(255,255,255,.65);backdrop-filter:blur(10px);border:1px solid rgba(59,130,246,.25);
 box-shadow:0 0 18px rgba(34,211,238,.15);flex-wrap:wrap}
.nav b{font-size:1.2rem;color:#0b1530;margin-right:auto;letter-spacing:.5px}
.nav a{color:#1e3a5f;text-decoration:none;font-weight:600;font-size:.92rem}
.nav a:hover{color:#06b6d4}
.hero{text-align:center;padding:1rem 0 2rem}
.hero h1{color:#0b1530;font-size:2.6rem;margin:.2rem 0}
.hero p{color:#334155;max-width:720px;margin:auto}
.card{background:rgba(255,255,255,.08);backdrop-filter:blur(12px);border:1px solid rgba(34,211,238,.35);
 border-radius:16px;padding:1.1rem 1.3rem;margin:.6rem 0;color:#e2e8f0;box-shadow:0 0 22px rgba(34,211,238,.12)}
.card h3,.sec{color:#67e8f9;margin-top:0}
.sec{font-size:1.5rem;font-weight:700;margin:1.6rem 0 .4rem}
.pill{display:inline-block;padding:.25rem .8rem;border-radius:99px;font-weight:700;font-size:.85rem}
.p-info{background:#0e7490;color:#fff}.p-warn{background:#b45309;color:#fff}
.p-ok{background:#15803d;color:#fff}.p-bad{background:#b91c1c;color:#fff}
.demo{border:1px dashed #f59e0b;color:#fde68a;padding:.6rem 1rem;border-radius:12px;background:rgba(245,158,11,.1)}
.stMarkdown,.stMetric label,[data-testid="stMetricValue"]{color:inherit}
[data-testid="stMetricValue"]{color:#67e8f9}[data-testid="stMetricLabel"] p{color:#cbd5e1}
.foot{color:#94a3b8;text-align:center;padding:2rem 0 1rem;font-size:.9rem}
.robot-wrap{display:flex;justify-content:center}
.robot{width:260px;height:300px;overflow:visible}
.ring{fill:none;stroke:#22d3ee;stroke-width:1.5;opacity:.5;transform-origin:130px 150px;animation:spin 8s linear infinite}
.ring2{stroke:#3b82f6;animation-duration:12s;animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes bob{50%{transform:translateY(-8px)}}
@keyframes pulse{50%{opacity:.35}}
@keyframes wave{50%{transform:scaleY(2.2)}}
.body{animation:bob 3.5s ease-in-out infinite}
.bar{fill:#22d3ee;transform-box:fill-box;transform-origin:center;animation:wave 1s ease-in-out infinite}
.bar:nth-child(2){animation-delay:.2s}.bar:nth-child(3){animation-delay:.4s}.bar:nth-child(4){animation-delay:.6s}
.eye{fill:#22d3ee;animation:pulse 3s infinite}
.scan{display:none;fill:#22d3ee;opacity:.35}
.st-scanning .scan{display:block;animation:sweep 1.2s linear infinite}
@keyframes sweep{from{transform:translateY(40px)}to{transform:translateY(210px)}}
.st-listening .eye{animation:pulse .6s infinite}
.st-genuine .eye,.st-genuine .ring{fill:#4ade80;stroke:#4ade80}
.st-ai .eye,.st-ai .ring{fill:#f87171;stroke:#f87171}
.st-ai .body{animation:none}
.st-neutral .eye{fill:#94a3b8}
@media(max-width:640px){.hero h1{font-size:1.8rem}.robot{width:200px;height:240px}.nav{gap:.7rem}}
</style>
"""

ROBOT_CAPTION = {
    "welcome": "Welcome - upload a recording to begin.",
    "listening": "Listening - audio received.",
    "scanning": "Scanning - analysing the signal...",
    "genuine": "Model result: genuine human voice.",
    "ai": "Model result: AI-generated / cloned voice - caution.",
    "neutral": "Signal analysis complete - no model connected, so no verdict.",
}


def robot_html(state="welcome"):
    mouth = ('M105 112 Q130 128 155 112' if state == "genuine"
             else 'M108 120 Q130 108 152 120' if state == "ai" else 'M110 116 L150 116')
    return f"""
<div class="robot-wrap"><svg class="robot st-{state}" viewBox="0 0 260 300" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#94a3b8"/></linearGradient>
<linearGradient id="d" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#0b1530"/></linearGradient></defs>
<ellipse class="ring" cx="130" cy="150" rx="120" ry="40"/><ellipse class="ring ring2" cx="130" cy="150" rx="100" ry="125"/>
<g class="body">
<rect x="70" y="55" width="120" height="85" rx="30" fill="url(#g)" stroke="#22d3ee"/>
<rect x="82" y="72" width="96" height="42" rx="18" fill="url(#d)"/>
<circle class="eye" cx="108" cy="92" r="7"/><circle class="eye" cx="152" cy="92" r="7"/>
<path d="{mouth}" stroke="#22d3ee" stroke-width="3" fill="none" stroke-linecap="round" transform="translate(0,-6)"/>
<rect x="124" y="30" width="12" height="25" fill="#94a3b8"/><circle cx="130" cy="26" r="6" fill="#22d3ee"/>
<rect x="55" y="150" width="150" height="95" rx="26" fill="url(#g)" stroke="#3b82f6"/>
<rect x="115" y="165" width="30" height="46" rx="15" fill="url(#d)" stroke="#22d3ee"/>
<path d="M105 195 Q130 225 155 195" stroke="#22d3ee" stroke-width="3" fill="none"/>
<g><rect class="bar" x="76" y="190" width="5" height="18" rx="2"/><rect class="bar" x="88" y="182" width="5" height="34" rx="2"/>
<rect class="bar" x="170" y="182" width="5" height="34" rx="2"/><rect class="bar" x="182" y="190" width="5" height="18" rx="2"/></g>
<rect x="30" y="155" width="26" height="70" rx="12" fill="url(#g)"/><rect x="204" y="155" width="26" height="70" rx="12" fill="url(#g)"/>
</g><rect class="scan" x="40" y="0" width="180" height="6" rx="3"/></svg></div>
<p style="text-align:center;color:#334155;font-size:.9rem">{ROBOT_CAPTION[state]}</p>"""
