import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel2 import build, endcard
CSS = '''<style>
.phone{position:absolute;inset:0;display:flex;flex-direction:column;background:#efe7dd}
.ph-h{height:300px;background:#075e54;color:#fff;display:flex;align-items:flex-end;gap:26px;padding:0 50px 34px}
.ph-h .av{width:120px;height:120px;border-radius:50%;background:#dfe5e7;display:flex;align-items:center;justify-content:center;font-size:66px}
.ph-h .nm{font-family:'PJ';font-weight:800;font-size:54px;line-height:1.1}
.ph-h .st{font-size:34px;opacity:.85;height:42px}
.ph-b{flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:22px;padding:30px 44px 440px;overflow:hidden;
  background-image:radial-gradient(rgba(0,0,0,.035) 2px,transparent 2px);background-size:46px 46px}
.m{max-width:820px;flex-direction:column;border-radius:30px;padding:22px 30px 14px;font-size:50px;line-height:1.25;color:#111b21;box-shadow:0 2px 2px rgba(0,0,0,.08)}
.m.in{align-self:flex-start;background:#fff;border-top-left-radius:6px;transform-origin:left bottom}
.m.out{align-self:flex-end;background:#d9fdd3;border-top-right-radius:6px;transform-origin:right bottom}
.m small{align-self:flex-end;font-size:28px;color:#667781;margin-top:4px}
.m small b{color:#53bdeb;font-weight:700}
.m em{font-size:36px;color:#667781;font-style:italic;margin-top:6px}
.m u{text-decoration:none;font-size:32px;font-weight:700;color:#0f7a52;margin-bottom:4px}
.m.card{background:#fff;border:4px solid #ffd84d}
.typ{align-self:flex-start;background:#fff;border-radius:30px;padding:30px 36px;gap:14px}
.typ i{width:20px;height:20px;border-radius:50%;background:#8696a0;display:block}
.sep{align-self:center;background:#ffd84d;color:#0e2b60;font-weight:700;font-size:40px;border-radius:20px;padding:14px 30px;flex-direction:row}
.brand{position:absolute;top:70px;right:44px;background:#ffd84d;color:#0e2b60;font-weight:700;font-size:30px;border-radius:999px;padding:10px 22px}
</style>'''
def gaps(iv):
    out=[]; cur=-1
    for a,b in iv: out.append((cur,a)); cur=b
    out.append((cur,999)); return out
def chat(contact, avatar, msgs, d, status='online', group=False, chip='Chat dalla Francia'):
    """msgs: (t, kind, testo, sottotitolo[, mittente])"""
    body=''; sfx=[]; typing=[]; mi=0
    for m in msgs:
        t,kind,txt,sub=m[:4]; who=m[4] if len(m)>4 else ''
        if kind=='sep':
            body+=f'<div class="m sep" data-at="{t}">{txt}</div>'; sfx.append((t,'pop')); continue
        if kind in ('in','card'): typing.append((max(0,t-0.9),t)); sfx.append((t,'msg'))
        else: sfx.append((t,'pop'))
        mi+=1; tick=' <b>✓✓</b>' if kind=='out' else ''
        em=f'<em>{sub}</em>' if sub else ''; wh=f'<u>{who}</u>' if who else ''
        cls='in card' if kind=='card' else kind
        body+=f'<div class="m {cls}" data-at="{t}">{wh}{txt}{em}<small>{"21:%02d"%(14+mi)}{tick}</small></div>'
    typ=''.join(f'<div class="typ" data-from="{a}" data-to="{b}"><i></i><i></i><i></i></div>' for a,b in typing)
    st=''.join(f'<span class="stat" data-from="{a}" data-to="{b}">sta scrivendo…</span>' for a,b in typing)+''.join(f'<span class="stat" data-from="{x}" data-to="{y}">{status}</span>' for x,y in gaps(typing))
    html=CSS+f'''<div class="phone"><div class="ph-h"><div class="av">{avatar}</div><div><div class="nm">{contact}</div><div class="st">{st}</div></div></div>
<div class="ph-b">{body}{typ}</div><span class="brand">Ciao Milo · {chip}</span></div>'''
    return dict(d=d, bg='#efe7dd', fg='#111b21', nohead=True, keep=True, style='padding:0', sfx=sfx, html=html)
def punch(k, txt, sub, bg='#0e2b60', milo='welcome'):
    return dict(d=3.0, bg=bg, fg='#fff', milo=milo, anim='bounce', sfx=[(0.1,'ding')],
        html=f'<span class="k" style="color:#ffd84d">{k}</span><div class="sm">{txt}</div><div class="p" data-at="0.9" style="color:#dbe8ff">{sub}</div>')
