"""Reel «Milo risponde»: una domanda arriva in chat, Milo risponde in 2-3 passi, chiusura «Tocca a te».

Uso:  python3 milo_risponde.py spec.json
spec.json = {
  "name": "risponde-2026-11-08",
  "domanda": "Come faccio ad avere la carte Vitale?",       # come la scriverebbe un follower
  "passi": [["1. Il numero", "Prima ti serve il numero di sicurezza sociale.", "Lo chiedi alla CPAM con il modulo S1106."],
            ["2. ...", "...", "..."]],                       # 2 o 3 passi: titolo breve, frase, dettaglio
  "consiglio": ["Il consiglio di Milo", "La guida completa è su ciaomilo.it", "Link nella storia di oggi"],
  "chiusura": "E tu quanto ci hai messo?"
}
Solo fatti verificati su fonti ufficiali. Niente marchi, niente alcol, niente volti.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reel2 import build, endcard
from chat import chat, punch

COLORI = ['#0e2b60', '#1769ef', '#0f7a52', '#5b3cc4']
MILO = ['documents', 'laptop', 'budget', 'welcome']

def episodio(s):
    scene = [chat('Domande per Milo 💬', '💬', [
        (0.8, 'in', s['domanda'], '', 'Un follower'),
        (2.8, 'out', 'Te lo spiego in 20 secondi 👇', '')], 4.4, chip='Milo risponde')]
    for i, (k, txt, sub) in enumerate(s['passi'][:3]):
        scene.append(punch(k, txt, sub, bg=COLORI[i % 4], milo=MILO[i % 4]))
    k, txt, sub = s['consiglio']
    scene.append(punch(k, txt, sub, bg='#0e2b60', milo='welcome'))
    scene.append(endcard(s['chiusura']))
    return build(s['name'], scene, series='Milo risponde')

if __name__ == '__main__':
    out, T = episodio(json.load(open(sys.argv[1])))
    print(out, round(T, 1))
