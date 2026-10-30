import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reel2 import build, endcard
N='#0e2b60'; G='#ffd84d'
W=[('Bonjour','bon-giòr','BONSCIÙR','La J come in abat-jour.','#f5f9ff','#1769ef'),
   ('Merci','mèr-ci','MERSÌ','Le merci stanno al porto.','#fff6ec','#9a4a0c'),
   ("S'il vous plaît",'sil vus plait','SIL VU PLÈ','Metà delle lettere sono lì per bellezza.','#f2faf6','#0f7a52'),
   ('Je ne comprends pas','ie ne comprends pas','SCE NE COMPRÀN PA','La frase che userai di più. Fidati.','#f6f3ff','#5b3cc4'),
   ("L'addition",'l\'addizione','LADISIÒN','Non è un\'addizione. Ma i conti li fai lo stesso.','#fff5f4','#b3261c'),
   ('Au secours !','au se-cours','O SECÙR','= Aiuto! Speriamo ti serva solo qui.','#fffaeb','#8a5a00')]
sc=[dict(d=2.4, bg='#5b3cc4', fg='#fff', milo='welcome', anim='shake', sfx=[(0, 'whoosh')],
   html=f'<span class="k" style="color:{G}">Il francese fonetico di Milo</span><div class="mid">Come si legge davvero?</div><div class="p" data-at="1.0" style="color:#ece6ff">Spoiler: non come è scritto.</div>')]
for i,(fr,wrong,right,joke,bg,acc) in enumerate(W):
    sc.append(dict(d=3.1, bg=bg, fg=N, sfx=[(0.05,'pop'),(0.95,'buzz'),(1.4,'boing'),(1.45,'ding')],
      html=f'<span class="k" style="color:{acc}">Parola n. {i+1}</span><div class="mid pop" data-at="0.05" lang="fr">{fr}</div>'
           f'<div class="p" data-at="0.5">Non si legge <span class="strike" data-s="0.9">«{wrong}»</span></div>'
           f'<div class="big pop" data-at="1.4" style="color:{acc};line-height:1.18;font-size:{130 if len(right)<12 else 100}px">«{right}»</div>'
           f'<div class="p" data-at="1.9" style="opacity:.85">{joke}</div>'))
sc.append(endcard('Qual è la parola francese che pronunci peggio?'))
out,T=build('fonetico', sc, series='Milo in 15 secondi'); print(round(T,1), out)
