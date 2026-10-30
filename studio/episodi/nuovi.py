import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reel2 import build, endcard
from chat import chat, punch
N='#0e2b60'; G='#ffd84d'; L='#f5f9ff'
def numero(n, fr, calc, d=3.0, bg=L, acc='#1769ef'):
    return dict(d=d, bg=bg, fg=N, sfx=[(0.05,'pop'),(0.8,'tick'),(1.0,'tick'),(1.2,'tick'),(1.5,'boing')],
      html=f'<div class="num pop" data-at="0.05" style="color:{acc};font-size:300px">{n}</div>'
           f'<div class="sm" data-at="0.6" lang="fr">{fr}</div>'
           f'<div class="mid" data-at="1.5" style="color:{acc}">= {calc}</div>')
R={
 'matematica': ('Milo in 15 secondi', [
   dict(d=2.4, bg='#5b3cc4', fg='#fff', milo='laptop', anim='shake', sfx=[(0,'whoosh')],
        html=f'<span class="k" style="color:{G}">La matematica francese</span><div class="mid">Contare fino a 100 in Francia</div><div class="p" data-at="1.0" style="color:#ece6ff">Serve la calcolatrice.</div>'),
   numero('70','soixante-dix','60 + 10'),
   numero('80','quatre-vingts','4 × 20', bg='#fff6ec', acc='#9a4a0c'),
   numero('90','quatre-vingt-dix','4 × 20 + 10', bg='#f2faf6', acc='#0f7a52'),
   numero('97','quatre-vingt-dix-sept','4 × 20 + 10 + 7', d=3.4, bg='#fff5f4', acc='#b3261c'),
   dict(d=3.0, bg=N, fg='#fff', milo='welcome', anim='bounce', sfx=[(0.2,'ding')],
        html=f'<span class="k" style="color:{G}">Plot twist</span><div class="sm">In Belgio e in Svizzera dicono «septante» e «nonante».</div><div class="p" data-at="1.0" style="color:#dbe8ff">Molto più semplice. Troppo semplice.</div>'),
   endcard('Quale numero francese ti manda in tilt?')]),
 'chat-scuola': ('Chat dalla Francia', [
   chat('Genitori CE2 🏫','👪',[
     (0.8,'in','Rappel : demain grève, pas de cantine 🙃','(Promemoria: domani sciopero, niente mensa)','Maman de Léo'),
     (3.2,'out','Di nuovo?',''),
     (4.4,'in','Et jeudi sortie piscine, prévoir bonnet de bain','(Giovedì piscina, portare la cuffia)','Maman de Léo'),
     (6.6,'out','E domani a pranzo cosa gli do?',''),
     (8.0,'in','Un sandwich 😊','(Un panino)','Papa de Jade'),
     (9.4,'out','Un panino… come pranzo?!',''),
     (10.8,'sep','Intanto, in Italia…',''),
     (11.8,'card','UN PANINO?! Mando io la pasta al forno.','','Nonna 👵')],13.6, status='Maman de Léo, Papa de Jade, Tu'),
   endcard('Anche il tuo gruppo genitori è così?')]),
 'chat-medico': ('Chat dalla Francia', [
   chat('Studio medico 🩺','🩺',[
     (0.8,'out','Bonjour! Vorrei un appuntamento con il medico',''),
     (2.4,'in','Prochain rendez-vous disponible : le 14 mars.','(Primo appuntamento libero: il 14 marzo)'),
     (4.6,'out','Ma siamo a novembre',''),
     (5.8,'in','Oui.',''),
     (7.0,'out','E se sto male prima?',''),
     (8.4,'in','Vous pouvez appeler le 116 117.','(Può chiamare il 116 117)'),
     (10.4,'out','Il 116 117 è il medico?? 😳','')],12.0),
   punch('Il consiglio di Milo','116 117: il medico di guardia, la sera e nel weekend.','Emergenza vera? Il 15, sempre.', milo='documents'),
   endcard('Qual è il tuo record di attesa dal medico?')]),
}
for k in (sys.argv[1:] or R):
    ser,sc=R[k]; out,T=build(k,sc,series=ser); print(k,round(T,1),out)
