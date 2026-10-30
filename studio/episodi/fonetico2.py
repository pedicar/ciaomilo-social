import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reel2 import build, endcard
N='#0e2b60'; G='#ffd84d'
PAL=[('#f5f9ff','#1769ef'),('#fff6ec','#9a4a0c'),('#f2faf6','#0f7a52'),('#f6f3ff','#5b3cc4'),('#fff5f4','#b3261c'),('#fffaeb','#8a5a00')]
def episode(name, n, tema, hook_bg, words, question):
    sc=[dict(d=2.4, bg=hook_bg, fg='#fff', milo='welcome', anim='shake', sfx=[(0,'whoosh')],
       html=f'<span class="k" style="color:{G}">Il francese fonetico · puntata {n}</span><div class="mid">{tema}</div><div class="p" data-at="1.0" style="color:#eef">Pronuncia approssimativa garantita.</div>')]
    for i,(fr,wrong,right,joke) in enumerate(words):
        bg,acc=PAL[i%6]
        sc.append(dict(d=3.1, bg=bg, fg=N, sfx=[(0.05,'pop'),(0.95,'buzz'),(1.4,'boing'),(1.45,'ding')],
          html=f'<span class="k" style="color:{acc}">Parola n. {i+1}</span><div class="mid pop" data-at="0.05" lang="fr">{fr}</div>'
               f'<div class="p" data-at="0.5">Non si legge <span class="strike" data-s="0.9">«{wrong}»</span></div>'
               f'<div class="big pop" data-at="1.4" style="color:{acc};line-height:1.18;font-size:{130 if len(right)<12 else 100}px">«{right}»</div>'
               f'<div class="p" data-at="1.9" style="opacity:.85">{joke}</div>'))
    sc.append(endcard(question))
    return build(name, sc, series='Milo in 15 secondi')
EP={
 'fonetico-bar': (2,'Al bar e in boulangerie','#9a4a0c',[
   ('Croissant','croissànt','CRUASSÀN','La T finale? Solo decorativa.'),
   ('Pain au chocolat','pain au cioccolat','PEN O SCIOCOLÀ','Pen, non pain. E a Tolosa nemmeno quello.'),
   ('Café au lait','cafè au lait','CAFÈ O LÈ','«Au» si legge O. Sempre. Rassegnati.'),
   ("L'eau",'l-e-a-u','LO','Quattro lettere, un suono solo. Magia.'),
   ('Oui','u-i','UÌ','Tre lettere per dire sì. A noi ne bastano due.'),
   ('Fromage','fromàge','FROMÀSC','La parola più importante di tutta la Francia.')],
   'Qual è la parola che al bar sbagli sempre?'),
 'fonetico-citta': (3,'Le città francesi','#1769ef',[
   ('Bordeaux','bor-de-àux','BORDÒ','8 lettere, 2 sillabe. Benvenuto in Francia.'),
   ('Toulouse','tu-lù-se','TULÙZ','La capitale della chocolatine.'),
   ('Marseille','mar-sèil-le','MARSÈI','Le due L? Partite in barca.'),
   ('Montpellier','mont-pel-lièr','MONPELIÈ','La R finale è in vacanza.'),
   ('Strasbourg','stra-sbùrg','STRASBÙR','La G finale è muta. Come al solito.'),
   ('Aix-en-Provence','aix in provènce','ÈX AN PROVÀNS','E gli abitanti? Aixois: «èxuà».')],
   'Qual è la città francese che pronunci peggio?'),
 'fonetico-burocrazia': (4,'La burocrazia','#5b3cc4',[
   ('Rendez-vous','ren-dez-vous','RANDEVÙ','Senza, in Francia non fai niente.'),
   ('Impôts','im-pòts','ENPÒ','6 lettere, se ne leggono 3. Si pagano tutte.'),
   ('Mutuelle','mutuèlle','MUTUÈL','Non è il mutuo. Te l\'abbiamo già detto.'),
   ('Quittance','quit-tànce','CHITÀNS','La ricevuta dell\'affitto. Chiedila sempre.'),
   ('Justificatif','iu-sti-fi-ca-tìf','SCIUSTIFICATÌF','Te lo chiederanno ogni settimana.'),
   ('Sécurité sociale','sècurite sociàle','SECURITÈ SOSIÀL','Quella della Carte Vitale.')],
   'Qual è la parola della burocrazia che ti fa più paura?'),
}
for k in (sys.argv[1:] or EP):
    n,tema,bg,w,q=EP[k]; out,T=episode(k,n,tema,bg,w,q); print(k,round(T,1),out)
