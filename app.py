"""VoxGuard - single-file app. Run: streamlit run app.py"""
import os, json, time, tempfile, hashlib
from pathlib import Path
import numpy as np, librosa, soundfile as sf
import plotly.graph_objects as go
import streamlit as st, streamlit.components.v1 as components

CONTACT = "aaa.miniproject@gmail.com"

# ================= STYLE =================
T = dict(ink="#f4f1ea", accent="#e2b866", vio="#8b7bff")

STYLE = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap');
:root{--bg:#06070b;--ink:#f4f1ea;--mute:#8d93a6;--gold:#e2b866;--gold2:#f6dc9b;--vio:#8b7bff;--good:#5ee0a0;--bad:#ff6b81;--line:rgba(255,255,255,.09);--glass:rgba(255,255,255,.04)}
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif;color:var(--ink)}
.stApp{background:radial-gradient(800px 520px at 8% -6%,rgba(139,123,255,.22),transparent 60%),radial-gradient(850px 520px at 96% 8%,rgba(226,184,102,.15),transparent 60%),radial-gradient(900px 600px at 50% 115%,rgba(139,123,255,.13),transparent 60%),var(--bg);background-attachment:fixed}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0}
.block-container{max-width:1160px;padding:1.2rem 1.2rem 3rem}
h1,h2,h3{font-family:'Instrument Serif',serif!important;font-weight:400!important;letter-spacing:-.01em;color:var(--ink)}
h2{font-size:2.8rem!important;line-height:1.05!important}
.stApp p,.stApp li,.stApp label,.stApp summary,.stApp [data-testid="stMarkdownContainer"]{color:var(--ink)!important}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] *{color:var(--mute)!important}
.stApp .mute{color:var(--mute)!important}
.stApp a{color:var(--gold)!important;text-decoration:none}
.brand{font-weight:600;letter-spacing:.38em;font-size:.95rem;padding-top:.7rem}
.stApp .brand b,.stApp .eyebrow,.stApp .num{color:var(--gold)!important}
.eyebrow{font-size:.72rem;letter-spacing:.26em;text-transform:uppercase;font-weight:600;margin-bottom:.35rem}
.gold{background:linear-gradient(100deg,#f6dc9b,#e2b866 45%,#b88a3e);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent!important;color:transparent}
.card{background:linear-gradient(155deg,rgba(255,255,255,.075),rgba(255,255,255,.02));border:1px solid var(--line);border-radius:26px;padding:1.4rem 1.5rem;margin-bottom:.9rem;backdrop-filter:blur(14px);box-shadow:0 30px 60px -42px #000,inset 0 1px 0 rgba(255,255,255,.07);animation:up .6s both;transition:transform .3s,border-color .3s,box-shadow .3s}
.card:hover{transform:translateY(-3px);border-color:rgba(226,184,102,.45);box-shadow:0 26px 60px -34px rgba(226,184,102,.45)}
.hero-t{font-family:'Instrument Serif',serif;font-size:clamp(2.8rem,7vw,5.2rem);line-height:1;margin:.4rem 0 1.1rem}
.big{font-family:'Instrument Serif',serif;font-size:2.1rem;line-height:1.1}
.num{font-family:'Instrument Serif',serif;font-size:2.4rem}
.ico{font-size:1.8rem;margin-bottom:.3rem}
.bar{height:8px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;margin:.35rem 0 1rem}
.bar i{display:block;height:100%;border-radius:99px;animation:grow 1s both}
.bar i.g{background:linear-gradient(90deg,#2fbf85,var(--good))}
.bar i.s{background:linear-gradient(90deg,#e0475f,var(--bad))}
.pill{display:inline-block;padding:.28rem .85rem;border-radius:99px;background:rgba(255,255,255,.06);border:1px solid var(--line);font-size:.76rem;margin:.15rem .25rem .15rem 0}
.status{border-left:4px solid var(--vio);background:rgba(255,255,255,.05);padding:1rem 1.2rem;border-radius:16px;margin-bottom:.9rem}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.7rem;margin-top:.5rem}
.tile{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:18px;padding:.8rem 1rem}
.tk{color:var(--mute);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase}
.tv{font-family:'Instrument Serif',serif;font-size:1.7rem;line-height:1.2}
.vrow{display:flex;gap:1.4rem;align-items:center;flex-wrap:wrap}
.ring{width:150px;height:150px;flex:none}
.ring .rg{animation:ringgrow 1.2s ease both}
.ring .rt{font-family:'Instrument Serif',serif;font-size:30px;fill:var(--ink)}
.ring .rl{font-size:9px;letter-spacing:.2em;fill:var(--mute);text-transform:uppercase}
.flow{display:flex;gap:.8rem;flex-wrap:wrap}.step{flex:1;min-width:150px}
.avatar{width:62px;height:62px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Instrument Serif',serif;font-size:1.7rem;color:#1a1304;background:linear-gradient(135deg,#f6dc9b,#e2b866 55%,#b88a3e);margin-bottom:.8rem}
.cta{display:inline-block;padding:.65rem 1.5rem;border-radius:99px;background:linear-gradient(100deg,#f6dc9b,#e2b866);font-weight:600;transition:.25s}
.stApp a.cta{color:#1a1304!important}
.cta:hover{transform:translateY(-2px);box-shadow:0 14px 34px -12px var(--gold)}
.foot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.8rem;border-top:1px solid var(--line);margin-top:3rem;padding-top:1.4rem;font-size:.85rem}
.foot .brand{padding-top:0;font-size:.8rem}
div[data-testid="stRadio"]{display:flex;justify-content:flex-end}
div[data-testid="stRadio"]>div{flex-direction:row;gap:.2rem;overflow-x:auto;flex-wrap:nowrap;scrollbar-width:none;padding:.35rem;background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:99px;backdrop-filter:blur(12px);max-width:100%}
div[data-testid="stRadio"] label{background:transparent;border:0;border-radius:99px;padding:.4rem 1.1rem;white-space:nowrap;cursor:pointer;transition:.25s;font-weight:500}
div[data-testid="stRadio"] label:hover{background:rgba(255,255,255,.07)}
div[data-testid="stRadio"] label:has(input:checked){background:linear-gradient(100deg,#f6dc9b,#e2b866)}
div[data-testid="stRadio"] label>div:first-child{display:none}
.stApp div[data-testid="stRadio"] label:has(input:checked),.stApp div[data-testid="stRadio"] label:has(input:checked) *{color:#1a1304!important}
.stButton>button,.stDownloadButton>button{border-radius:99px;border:1px solid var(--line);background:rgba(255,255,255,.05);padding:.6rem 1.4rem;font-weight:500;transition:.25s;backdrop-filter:blur(10px)}
.stApp .stButton button,.stApp .stButton button *{color:var(--ink)!important}
.stButton>button:hover{background:linear-gradient(100deg,#f6dc9b,#e2b866);border-color:transparent;transform:translateY(-2px);box-shadow:0 14px 34px -14px var(--gold)}
.stApp .stButton button:hover,.stApp .stButton button:hover *{color:#1a1304!important}
div[data-testid="stFileUploader"] section{border:1.5px dashed rgba(226,184,102,.4);border-radius:26px;background:rgba(255,255,255,.03);padding:1.8rem 1rem;transition:.25s}
div[data-testid="stFileUploader"] section:hover{border-color:var(--gold);background:rgba(226,184,102,.06)}
.stApp [data-testid="stFileUploaderDropzone"] *{color:var(--mute)!important}
.stApp [data-testid="stFileUploaderDropzone"] button{background:linear-gradient(100deg,#f6dc9b,#e2b866)!important;border-radius:99px!important;border:none!important}
.stApp [data-testid="stFileUploaderDropzone"] button *{color:#1a1304!important}
div[data-baseweb="select"]>div{background:rgba(255,255,255,.05)!important;border:1px solid var(--line)!important;border-radius:16px!important}
[data-testid="stAudioInput"]>div{background:rgba(255,255,255,.04)!important;border:1px solid var(--line)!important;border-radius:22px!important}
[data-testid="stExpander"] details{background:rgba(255,255,255,.03);border:1px solid var(--line)!important;border-radius:18px}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--gold),var(--vio))}
.stApp [data-testid="stAlert"]{background:rgba(18,24,42,.92)!important;border:1px solid rgba(226,184,102,.35)!important;border-radius:18px!important}
.stApp [data-testid="stAlert"] *{color:#fff!important}
.stApp [data-testid="stAlert"] svg{fill:#fff!important}
.marq{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:.7rem 0;margin:2rem 0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent);mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.marq .track{display:flex;gap:2.2rem;width:max-content;animation:scrollx 30s linear infinite}
.marq span{font-family:'Instrument Serif',serif;font-size:1.7rem;white-space:nowrap}
.marq span:nth-child(even){color:var(--gold)}
.eq{display:flex;gap:4px;align-items:flex-end;height:46px;margin:.8rem 0}
.eq i{width:6px;height:100%;border-radius:4px;background:linear-gradient(var(--gold),var(--vio));transform-origin:bottom;animation:eqb 1.2s ease-in-out infinite}
.band{background:linear-gradient(120deg,#0d0f1c,#1d1b4b 60%,#3b2a8c);border:1px solid var(--line);border-radius:30px;padding:2.2rem 1.8rem;margin:1.6rem 0 .8rem}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes grow{from{width:0}}
@keyframes ringgrow{from{stroke-dasharray:0 400}}
@keyframes scrollx{to{transform:translateX(-50%)}}
@keyframes eqb{0%,100%{transform:scaleY(.15)}50%{transform:scaleY(1)}}
.stApp ::-webkit-scrollbar{width:8px;height:8px}
.stApp ::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:99px}
@media(max-width:640px){.block-container{padding:.8rem .8rem 3rem}h2{font-size:2rem!important}.card{padding:1.1rem}.step{min-width:100%}div[data-testid="stRadio"]{justify-content:flex-start}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
