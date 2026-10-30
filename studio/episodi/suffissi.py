import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reel2 import build, endcard
N='#0e2b60'; G='#ffd84d'
PAL=[('#f5f9ff','#1769ef'),('#fff6ec','#9a4a0c'),('#f2faf6','#0f7a52'),('#f6f3ff','#5b3cc4'),('#fff5f4','#b3261c'),('#fffaeb','#8a5a00')]
W=[('informa','zione','information','-zione → -tion'),('famo','so','fameux','-oso → -eux'),('universi','tà','université','-tà → -té'),
   ('professo','re','professeur','-ore → -eur'),('fantasti','co','fantastique','-ico → -ique'),('rapida','mente','rapidement','-mente → -ment')]
sc=[dict(d=2.4, bg='#0f6e66', fg='#fff', milo='welcome', anim='shake', sfx=[(0,'whoosh')],
   html=f'<span class="k" style="color:{G}">Il trucco dei suffissi</span><div class="mid">Parli già francese. Solo che non lo sai.</div>')]
for i,(root,suf,fr,rule) in enumerate(W):
    bg,acc=PAL[i]
    sc.append(dict(d=2.7, bg=bg, fg=N, sfx=[(0.05,'pop'),(0.65,'buzz'),(1.2,'boing'),(1.25,'ding')],
      html=f'<span class="chip" style="background:{acc};color:#fff">{rule}</span>'
           f'<div class="mid pop" data-at="0.05">{root}<span class="strike" data-s="0.6" style="color:{acc}">{suf}</span></div>'
           f'<div class="big pop" data-at="1.2" lang="fr" style="color:{acc};line-height:1.15;font-size:{120 if len(fr)<11 else 100}px">{fr}</div>'))
sc.append(dict(d=3.2, bg='#fff5f4', fg=N, milo='laptop', anim='float', sfx=[(0.1,'buzz'),(1.0,'pop')],
   html='<span class="k" style="color:#b3261c">Attenzione però</span><div class="sm">città ≠ <s>cité</s></div><div class="mid" data-at="1.0" style="color:#b3261c" lang="fr">= ville</div><div class="p" data-at="1.6">Non funziona sempre. Ma quasi.</div>'))
sc.append(endcard('Come si dice: nazione, curioso, attore?'))
out,T=build('suffissi', sc); print(round(T,1), out)
