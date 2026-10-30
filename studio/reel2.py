# Reel Ciao Milo v2: sigla, testo animato a tempo, Milo animato, effetti sonori sintetizzati, cartolina finale.
import os, json, subprocess, shutil, wave
import numpy as np
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
S = os.environ.get('MILO_WORK', '/tmp/milo-work/'); os.makedirs(S + 'gen', exist_ok=True)
FN = HERE + 'fonts/'; IMG = HERE + 'img/'
FPS = 30; SR = 44100
OUT = os.environ.get('MILO_OUT', HERE + 'out/'); os.makedirs(OUT, exist_ok=True)

def ff(fam, f, w, st='normal'): return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(file://{FN}{f})}}"
FONTS = ff('PJ', 'plus-jakarta-sans/files/plus-jakarta-sans-latin-800-normal.woff2', 800) + \
        ff('PJ', 'plus-jakarta-sans/files/plus-jakarta-sans-latin-ext-800-normal.woff2', 800) + \
        ''.join(ff('DM', f'dm-sans/files/dm-sans-latin-{w}-{s}.woff2', w, s) for w in (500, 700) for s in ('normal', 'italic'))

def env(n, a=0.005, r=None):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) if a else np.ones(n)
    if r: e *= np.exp(-t / r)
    return e
def tone(f0, dur, f1=None, r=0.15, harm=0.0):
    n = int(SR * dur); t = np.arange(n) / SR
    f = f0 if f1 is None else f0 + (f1 - f0) * t / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + harm * np.sin(2 * ph)) * env(n, r=r)
def noise(dur, r=0.1, lp=0.2):
    n = int(SR * dur); x = np.random.default_rng(1).standard_normal(n)
    y = np.zeros(n)
    for i in range(1, n): y[i] = y[i-1] + lp * (x[i] - y[i-1])
    return y / (np.abs(y).max() + 1e-9) * env(n, a=0.02, r=r)
SFX = {
 'pop':   lambda: 0.55 * tone(900, 0.09, 320, r=0.04),
 'kiss':  lambda: 0.5 * tone(1600, 0.06, 900, r=0.02) + 0.25 * noise(0.06, r=0.01, lp=0.6),
 'whoosh':lambda: 0.35 * noise(0.4, r=0.18, lp=0.08),
 'ding':  lambda: 0.35 * (tone(1318, 0.7, r=0.25, harm=0.3) + 0.6 * tone(1760, 0.7, r=0.2)),
 'buzz':  lambda: 0.22 * np.sign(tone(140, 0.35, r=1.0)) * env(int(SR*0.35), r=0.25),
 'tick':  lambda: 0.4 * tone(2200, 0.012, r=0.004),
 'boing': lambda: 0.45 * tone(220, 0.45, 520, r=0.2),
 'msg':   lambda: 0.35 * np.concatenate([tone(880, 0.07, r=0.05), tone(1320, 0.1, r=0.06)]),
 'jingle':lambda: 0.4 * np.concatenate([tone(f, 0.11, r=0.12, harm=0.25) for f in (523, 659, 784)] + [tone(1047, 0.5, r=0.25, harm=0.25)]),
 'outro': lambda: 0.4 * np.concatenate([tone(f, 0.1, r=0.1, harm=0.25) for f in (784, 659)] + [tone(1047, 0.6, r=0.3, harm=0.25)]),
}

def mix(events, T, path):
    buf = np.zeros(int(SR * (T + 1)))
    for t, name in events:
        s = SFX[name](); i = int(t * SR); buf[i:i+len(s)] += s[:len(buf)-i]
    buf = np.clip(buf[:int(SR * T)], -1, 1); pcm = (buf * 32767 * 0.9).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())

CSS = '''*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:'DM';}
#bg{position:absolute;inset:0}
.sc{position:absolute;inset:0;padding:580px 90px 470px;display:flex;flex-direction:column;justify-content:center;gap:38px;opacity:0}
.k{font-size:40px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.big{font-family:'PJ';font-weight:800;font-size:140px;line-height:1;letter-spacing:-.03em}
.mid{font-family:'PJ';font-weight:800;font-size:100px;line-height:1.05;letter-spacing:-.02em}
.sm{font-family:'PJ';font-weight:800;font-size:76px;line-height:1.1;letter-spacing:-.01em}
.p{font-size:54px;line-height:1.3}
.num{font-family:'PJ';font-weight:800;font-size:400px;line-height:.9;letter-spacing:-.05em}
.strike{position:relative;display:inline-block}
.strike::after{content:'';position:absolute;left:-6px;top:52%;height:12px;background:#d93025;border-radius:6px;width:calc(var(--w,0)*100% + 12px)}
.chip{align-self:flex-start;border-radius:999px;padding:16px 30px;font-size:40px;font-weight:700}
#head{position:absolute;top:120px;left:90px;right:90px;display:flex;gap:22px;align-items:center;font-family:'PJ';font-weight:800;font-size:44px}
#head img{width:90px;height:90px;border-radius:50%;background:#fff}
#head .ser{margin-left:auto;font-family:'DM';font-weight:700;font-size:32px;padding:12px 22px;border-radius:999px;background:#ffd84d;color:#0e2b60}
#milo{position:absolute;right:90px;top:250px;width:330px;height:264px;object-fit:cover;border-radius:44px;box-shadow:0 20px 50px rgba(0,0,0,.25)}
#bar{position:absolute;left:0;bottom:0;height:18px;background:#ffd84d}
#intro{position:absolute;inset:0;background:#1769ef;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;color:#fff}
#intro img{width:300px;height:300px;border-radius:50%;background:#fff}
#intro span{font-family:'PJ';font-weight:800;font-size:96px;letter-spacing:-.02em}
#intro i{font-style:normal;font-size:44px;font-weight:700;color:#ffd84d;letter-spacing:.08em;text-transform:uppercase}
'''
JS = '''
const SC=__SC__, T=__T__, INTRO=__IN__;
const cl=(x)=>Math.max(0,Math.min(1,x)); const eo=(x)=>1-Math.pow(1-x,3);
const back=(x)=>{const c=1.7;x=cl(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
function render(t){
  const io=document.getElementById('intro');
  if(INTRO>0){ io.style.opacity = t<INTRO-0.15?1:cl((INTRO-t)/0.15);
    io.querySelector('img').style.transform=`scale(${back(t/0.45)})`;
    io.querySelector('span').style.transform=`translateY(${40*(1-eo(cl((t-0.15)/0.3)))}px)`; io.querySelector('span').style.opacity=cl((t-0.15)/0.25);
    io.querySelector('i').style.opacity=cl((t-0.35)/0.25);} else io.style.display='none';
  let cur=null;
  SC.forEach((s,i)=>{const el=document.getElementById('s'+i); const a=t-s.t0, d=s.t1-s.t0; let o=0;
    if(a>=0&&a<d){cur=s; const fi=cl(a/0.25), fo=s.keep?1:cl((d-a)/0.2); o=Math.min(fi,fo); el.style.transform=`translateY(${50*(1-eo(fi))}px)`;}
    el.style.opacity=o;
    el.querySelectorAll('[data-at]').forEach(e=>{const at=+e.dataset.at; const x=cl((a-at)/0.25);
      if(e.classList.contains('m')){e.style.display=a>=at?'flex':'none'; e.style.opacity=1; e.style.transform=`scale(${a<at?0.5:back((a-at)/0.3)})`;}
      else if(e.classList.contains('pop')){e.style.opacity=x>0?1:0; e.style.transform=`scale(${a<at?0.4:back((a-at)/0.35)})`; e.style.transformOrigin=e.dataset.origin||'left center';}
      else {e.style.opacity=x; e.style.transform=`translateY(${30*(1-eo(x))}px)`;}});
    el.querySelectorAll('.typ').forEach(e=>{const on=a>=+e.dataset.from&&a<+e.dataset.to; e.style.display=on?'flex':'none';
      e.querySelectorAll('i').forEach((d,k)=>{d.style.opacity=0.35+0.65*Math.max(0,Math.sin(a*9-k*0.9))});});
    el.querySelectorAll('.stat').forEach(e=>{const on=a>=+e.dataset.from&&a<+e.dataset.to; e.style.display=on?'block':'none'});
    el.querySelectorAll('.strike[data-s]').forEach(e=>{e.style.setProperty('--w',eo(cl((a-+e.dataset.s)/0.3)))});
  });
  const m=document.getElementById('milo');
  if(cur){document.getElementById('bg').style.background=cur.bg; document.body.style.color=cur.fg; document.getElementById('head').style.display=cur.nohead?'none':'flex';
    if(cur.milo){m.style.display='block'; m.src=cur.milo; const a=t-cur.t0; let tr='';
      if(cur.anim=='shake') tr=`rotate(${6*Math.sin(a*28)*Math.exp(-a*3)}deg) scale(${back(a/0.4)})`;
      else if(cur.anim=='bounce') tr=`translateY(${-60*Math.abs(Math.sin(a*7))*Math.exp(-a*2.5)}px) scale(${back(a/0.4)})`;
      else tr=`translateY(${10*Math.sin(a*2.5)}px) scale(${back(a/0.4)})`;
      m.style.transform=tr;} else m.style.display='none';}
  document.getElementById('bar').style.width=(100*t/T)+'%';
}'''

def build(name, scenes, series='Milo in 15 secondi', intro=0.9):
    t = intro; sc = []; blocks = ''; sfx = [(0.05, 'jingle')] if intro else []
    for i, s in enumerate(scenes):
        s = dict(s); s['t0'] = t; s['t1'] = t + s['d']; t = s['t1']
        if s.get('milo'): s['milo'] = 'file://' + IMG + 'milo-' + s['milo'] + '.webp'
        for (o, n) in s.get('sfx', []): sfx.append((s['t0'] + o, n))
        sc.append(s); blocks += f'<div class="sc" id="s{i}" style="{s.get("style","")}">{s["html"]}</div>'
    T = t
    meta = json.dumps([{k: v for k, v in s.items() if k not in ('html', 'sfx')} for s in sc])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body>
<div id="bg"></div><div id="head"><img src="file://{IMG}milo-icon.png"><span>Ciao Milo</span><span class="ser">{series}</span></div>
{blocks}<img id="milo"><div id="bar"></div>
<div id="intro"><img src="file://{IMG}milo-icon.png"><span>Ciao Milo</span><i>{series}</i></div>
<script>{JS.replace('__SC__', meta).replace('__T__', str(T)).replace('__IN__', str(intro))}</script></body></html>'''
    fr = S + f'gen/fr_{name}/'; shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    p = S + f'gen/reel_{name}.html'; open(p, 'w').write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}); pg.goto('file://' + p)
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        for f in range(int(T * FPS)):
            pg.evaluate(f'render({f / FPS})'); pg.screenshot(path=fr + f'{f:05d}.jpg', type='jpeg', quality=90)
        b.close()
    wav = S + f'gen/{name}.wav'; mix(sfx, T, wav)
    os.makedirs(OUT, exist_ok=True); out = OUT + f'reel-{name}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', fr + '%05d.jpg', '-i', wav,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '20', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    shutil.rmtree(fr)
    return out, T

def endcard(question, bg='#0e2b60'):
    return dict(d=2.6, bg=bg, fg='#fff', milo='welcome', anim='bounce', keep=True, sfx=[(0.2, 'outro')],
        html=f'<span class="k" style="color:#ffd84d">Tocca a te</span><div class="sm">{question}</div>'
             f'<div class="p" data-at="0.8" style="color:#dbe8ff">Salvalo · Giralo a un amico</div>'
             f'<span class="chip pop" data-at="1.1" style="background:#fff;color:#0e2b60">@ciaomilo.it</span>')
