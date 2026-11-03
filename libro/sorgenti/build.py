import re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fixes import FIX

W = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(W, "raw.txt")).read()

# ---------------------------------------------------------------- text fixes
missing = []
for a, b in FIX:
    if a not in raw:
        missing.append(a[:60])
    raw = raw.replace(a, b)
if missing:
    print("FIX NOT FOUND:", *missing, sep="\n  ")

# ---------------------------------------------------------------- parse
blocks = []
page = 0
for line in raw.splitlines():
    m = re.match(r"<!-- p(\d+) -->", line)
    if m:
        page = int(m.group(1)); continue
    if "| " not in line:
        continue
    tag, txt = line.split("| ", 1)
    blocks.append([tag, txt.strip(), page])

# ---------------------------------------------------------------- figures
FIG = {
 "p12_1": ("p12_1.jpg", "L'evoluzione della postura: dal quadrupede all'uomo moderno sedentario."),
 "p16_1": ("p16_1.jpg", "Malattie professionali denunciate all'INAIL nel 2023: le patologie muscoloscheletriche sono la prima causa."),
 "p18_1": ("p18_1.jpg", "La colonna vertebrale: regioni, curve fisiologiche, vertebra lombare e disco intervertebrale."),
 "p20_1": ("p20_1.jpg", "La lordosi cervicale normale e la sua riduzione (rettilinizzazione)."),
 "p20_2": None,  # duplicato della figura sul sovraccarico cervicale del capitolo 3
 "p20_3": ("p20_3.jpg", "L'ipercifosi dorsale, la cosiddetta 'gobba'."),
 "p21_1": ("p21_1.jpg", "Le tre condizioni della lordosi lombare: normale, ridotta (retroversione) e aumentata (anteroversione)."),
 "p31_1": ("p31_1.jpg", "La postura tipica di chi trascorre molte ore seduto."),
 "p32_1": ("p32_1.jpg", "Gli effetti della postura da scrivania sulle diverse strutture del corpo."),
 "p33_1": ("p33_1.jpg", "Allineamento del bacino e della colonna: corretto e con compensazione."),
 "p33_2": [("p33_smartphone.jpg", "Sovraccarico cervicale: pochi gradi di flessione del capo moltiplicano il carico sulla colonna."),
           ("p33_curve.jpg", "La curva cervicale: lordosi normale e inversione della lordosi (cifosi cervicale).", "narrow")],
 "p34_1": ("p34_1.jpg", "Lo squilibrio tra psoas (flessore dell'anca) e grande gluteo (estensore dell'anca)."),
 "p36_1": ("p36_1.jpg", "I muscoli più coinvolti nello stress cronico."),
 "p39_1": ("p39_1.jpg", "Ernia discale L3-L4 massiva con sindrome della cauda equina."),
 "p40_1": ("p40_1.jpg", "La stenosi del canale vertebrale lombare e le sue cause principali."),
 "p41_1": ("p41_scoliosi.jpg", "I gradi della scoliosi, dalla colonna in asse alle deviazioni più severe."),
 "p41_2": None,
 "p42_1": ("p42_1.jpg", "Osso sano e osso osteoporotico; la MOC è l'esame per misurare la densità ossea."),
 "p52_1": "PHOTO52",
 "p54_1": "PHOTO54",
 "p55_1": "PHOTO55",
 "p55_2": ("p55_2.jpg", "Retrazione del mento (chin tuck): posizione di partenza e allungamento.", "narrow"),
 "p56_1": "PHOTO56",
 "p57_1": ("p57_1.jpg", "Il diaframma, il principale muscolo della respirazione."),
 "p58_1": ("p58_1.jpg", "Dormire sulla schiena con un cuscino sotto le ginocchia, e le posizioni da evitare."),
 "p59_1": ("p59_1.jpg", "Dormire sul fianco: la posizione corretta con l'aiuto dei cuscini."),
 "p60_1": ("p60_1.jpg", "Il materasso e il guanciale: il supporto giusto per una schiena sana."),
 "p61_1": ("p61_1.jpg", "Sollevare i pesi correttamente: il modo sbagliato e quello corretto, passo dopo passo."),
 "p66_1": ("p66_1.jpg", "Scoliosi funzionale e strutturale: il test di flessione in avanti (test di Adams)."),
 "p67_1": ("p67_1.jpg", "Il mal di schiena nei bambini e negli adolescenti: spondilolisi e spondilite anchilosante giovanile."),
 "p74_1": "PHOTO74",
 "p75_1": "PHOTO75",
 "p76_1": ("p76_1.jpg", "I test di forza funzionale per i muscoli chiave della schiena."),
 "p77_1": None,  # richiesto dall'autore: togliere le foto degli errori comuni
 "p78_1": ("p78_1.jpg", "Esercizio 2 – Ponte glutei base, con la progressione fino alla versione monopodalica."),
 "p79_1": "PHOTO79",
 "p80_1": ("p80_gatto.jpg", "Esercizio 4 – Gatto-cammello: le fasi del gatto e del cammello."),
 "p81_1": "PHOTO81",
 "p82_1": "PHOTO82",
 "p83_1": None,  # richiesto dall'autore: si usa la figura del ponte glutei del Livello 1
 "p84_1": "PHOTO84",
 "p85_1": "PHOTO85",
 "p86_1": "PHOTO86",
 "p87_1": "PHOTO87",
 "p88_1": ("p88_1.jpg", "Livello 3, esercizio 1 – Stacco da terra con varianti."),
 "p89_1": ("p89_1.jpg", "Livello 3, esercizio 2 – Squat goblet."),
 "p90_1": ("p90_1.jpg", "Livello 3, esercizio 3 – Farmer's carry."),
 "p91_1": ("p91_1.jpg", "Livello 3, esercizio 4 – Step up su rialzo."),
 "p92_1": ("p92_1.jpg", "Livello 3, esercizio 5 – Pallof press."),
 "p95_1": ("p95_1.jpg", "Il foam rolling e l'auto-rilascio miofasciale."),
}
PHOTOS = {
 "PHOTO52": [
   ("La postazione di lavoro: piedi appoggiati a terra, schiena sostenuta dallo schienale, avambracci appoggiati e schermo davanti agli occhi.",
    [("nf33.jpg", "Postazione di lavoro")]),
 ],
 "PHOTO54": [
   ("Allungamento degli estensori lombari in posizione seduta: posizione di partenza e ginocchio portato al petto.",
    [("foto02.jpg", "Partenza"), ("foto03.jpg", "Ginocchio al petto")]),
   ("Rotazione lombosacrale in decubito: posizione di partenza e ginocchia lasciate cadere da un lato e dall'altro, con le spalle a terra.",
    [("nf36.jpg", "Partenza"), ("nf35.jpg", "Rotazione"), ("nf34.jpg", "Lato opposto")]),
   ("Gatto-cammello: fase del gatto (schiena arrotondata verso il soffitto) e fase del cammello (schiena inarcata verso il pavimento).",
    [("nfo00.jpg", "Gatto"), ("nfo01.jpg", "Cammello")]),
 ],
 "PHOTO55": [
   ("Stretching dei flessori dell'anca in affondo: posizione di partenza, allungamento e variante con il braccio sollevato.",
    [("foto04.jpg", "Partenza"), ("foto05.jpg", "Allungamento"), ("foto06.jpg", "Variante")]),
 ],
 "PHOTO56": [
   ("Stretching dei muscoli posteriori della coscia: tallone sulla sedia e inclinazione in avanti a schiena dritta.",
    [("foto07.jpg", "Partenza"), ("foto08.jpg", "Allungamento")]),
 ],
 "PHOTO74": [
   ("Ricerca della posizione neutra in posizione supina: dalla massima antiversione (arco lombare accentuato) alla massima retroversione (lombare appiattita a terra); la posizione neutra è circa a metà.",
    [("nfo11.jpg", "Antiversione"), ("nf37.jpg", "Neutra"), ("nf38.jpg", "Retroversione")]),
 ],
 "PHOTO75": [
   ("Test di mobilità di base: flessione in avanti, apertura dell'anca e mobilità della caviglia.",
    [("nf40.jpg", "Flessione in avanti"), ("foto09.jpg", "Apertura dell'anca"), ("foto10.jpg", "Mobilità della caviglia")]),
   ("Test di mobilità di base: estensione lombare da prono e rotazione toracica in quadrupedia.",
    [("nf39.jpg", "Estensione"), ("nf41.jpg", "Rotazione")]),
 ],
 "PHOTO79": [
   ("Esercizio 3 – Bird dog: posizione di partenza in quadrupedia ed estensione del braccio e della gamba opposti.",
    [("nf06.jpg", "Partenza"), ("nf05.jpg", "Estensione")]),
   ("Bird dog, errori comuni: gamba sollevata troppo in alto, con estensione lombare eccessiva e rotazione del bacino.",
    [("nf03.jpg", "Errore"), ("nf07.jpg", "Errore")]),
   ("Bird dog, progressione con rowing: il gomito va verso il ginocchio senza appoggiare a terra, poi braccio e gamba si riestendono.",
    [("nf00.jpg", "Gomito al ginocchio"), ("nf01.jpg", "Riestensione")]),
 ],
 "PHOTO81": [
   ("Esercizio 5 – Rotazione toracica seduta: posizione di partenza e rotazione verso i due lati.",
    [("nf13.jpg", "Partenza"), ("nf11.jpg", "Rotazione"), ("nf12.jpg", "Lato opposto")]),
   ("Rotazione toracica, progressione: seduti a terra a gambe incrociate e poi a gambe estese.",
    [("nf09.jpg", "Gambe incrociate"), ("nf14.jpg", "Gambe estese")]),
 ],
 "PHOTO_ES6": [
   ("Esercizio 6 – Allungamento degli estensori lombari: posizione di partenza e ginocchia portate al petto.",
    [("nf42.jpg", "Partenza"), ("nf43.jpg", "Ginocchia al petto")]),
 ],
 "PHOTO82": [
   ("Livello 2, esercizio 1 – Dead bug: posizione di partenza ed estensione del braccio e della gamba opposti, alternando i lati.",
    [("nf44.jpg", "Partenza"), ("nf45.jpg", "Estensione"), ("nf47.jpg", "Lato opposto")]),
 ],
 "PHOTO84": [
   ("Livello 2, esercizio 3 – Superman: posizione di partenza e sollevamento contemporaneo di braccia e gambe.",
    [("nf20.jpg", "Partenza"), ("nf15.jpg", "Superman")]),
   ("Superman, versioni facilitate: sollevamento delle sole braccia o delle sole gambe.",
    [("nf18.jpg", "Solo braccia"), ("nf17.jpg", "Solo gambe")]),
 ],
 "PHOTO85": [
   ("Livello 2, esercizio 4 – Plank laterale: posizione di partenza e sollevamento del bacino.",
    [("nf25.jpg", "Partenza"), ("nf24.jpg", "Plank laterale")]),
   ("Plank laterale: versione facilitata sulle ginocchia e progressioni con sollevamento della gamba o del braccio.",
    [("nf23.jpg", "Sulle ginocchia"), ("nf21.jpg", "Gamba sollevata"), ("nf22.jpg", "Braccio al soffitto")]),
 ],
 "PHOTO86": [
   ("Livello 2, esercizio 5 – Wall sit: schiena appoggiata al muro, poi discesa fino a ginocchia a circa 90 gradi.",
    [("nf27.jpg", "Partenza"), ("nf26.jpg", "Wall sit")]),
 ],
 "PHOTO87": [
   ("Livello 2, esercizio 6 – Clamshell: posizione di partenza e apertura del ginocchio superiore.",
    [("nf31.jpg", "Partenza"), ("nf30.jpg", "Apertura")]),
   ("Clamshell, progressione con elastico sopra le ginocchia.",
    [("nf28.jpg", "Partenza"), ("nf32.jpg", "Apertura")]),
 ],
}

# assign image keys in order
cnt = {}
for b in blocks:
    if b[0] == "IMG":
        pg = int(b[1].split(":")[0]); cnt[pg] = cnt.get(pg, 0) + 1
        b[1] = f"p{pg:02d}_{cnt[pg]}"

# ---------------------------------------------------------------- structural edits
out = []
i = 0
while i < len(blocks):
    tag, txt, pg = blocks[i]
    # case clinico Giulia: body was flagged red because of one coloured word
    if tag == "RED" and txt.startswith("Giulia"):
        out[-1][1] += " " + txt; i += 1; continue
    if tag == "RED":
        i += 1; continue
    if tag == "P" and txt.startswith("**Una** **postura**"):
        out.append(["BLUE", txt.replace("**", ""), pg]); i += 1; continue
    out.append([tag, txt, pg]); i += 1
blocks = out

def find(prefix):
    for k, b in enumerate(blocks):
        if b[1].startswith(prefix):
            return k
    raise KeyError(prefix)

# Ch.3: shorten the duplicated section on central sensitisation (explained in full in ch.4)
k = find("In chi soffre di dolore lombare cronico, si sviluppa spesso")
blocks[k][1] = ("In chi soffre di dolore lombare cronico si sviluppa spesso un fenomeno chiamato "
    "sensibilizzazione centrale: il sistema nervoso diventa iperattivo nel processare i segnali di dolore "
    "e ne abbassa la soglia, così che stimoli normalmente innocui, o appena fastidiosi, vengono percepiti "
    "come dolorosi. Il dolore tende a estendersi a zone che in origine non erano coinvolte e diventa "
    "sproporzionato rispetto allo stimolo. Per questo il trattamento non può limitarsi ai tessuti periferici, "
    "ma deve includere la modulazione del sistema nervoso: ne parleremo in dettaglio nel capitolo 4.")
del blocks[k + 1]

# Intro: no appendices exist in the book
k = find("Troverai nel testo diversi elementi grafici.")
blocks[k][1] = blocks[k][1].replace(
    "Le appendici alla fine raccolgono gli esercizi in formato scheda, il glossario e i riferimenti scientifici.",
    "Nel capitolo 8 gli esercizi sono presentati in forma di scheda, con serie, ripetizioni e illustrazioni passo per passo.")
k = find("Ho organizzato questo libro seguendo una logica progressiva")
blocks[k][1] = blocks[k][1].replace(
    "Gli ultimi affrontano la prevenzione a lungo termine e i casi in cui è necessario un supporto professionale.",
    "Gli ultimi propongono un programma pratico di allenamento e gli strumenti per mantenere i risultati nel tempo.")

# Ch.6 cervicalgia: avoid repeating the numbers already given in ch.3
k = find("Il dolore cervicale legato alla postura")
blocks[k][1] = blocks[k][1].replace(
    "Con la testa in posizione neutra, il peso che la colonna cervicale deve sostenere è di circa 5-6 kg. Con una flessione di 30 gradi in avanti, quel carico sale a circa 18 kg. A 60 gradi, supera i 27 kg.",
    "Come abbiamo visto nel capitolo 3, già a 30 gradi di flessione il carico sulla colonna cervicale si triplica rispetto alla posizione neutra, e a 60 gradi arriva a circa 27 kg.")

# Ch.8 test di mobilità: add the two tests illustrated by the author's photos
k = find("Rotazione: in quadrupedia, porta una mano")
blocks.insert(k + 1, ["P", "Apertura dell'anca: in affondo, con il ginocchio posteriore appoggiato a terra e le mani sui fianchi, porta il bacino in avanti mantenendo il busto eretto. Senti un allungamento nella parte anteriore dell'anca? È simile tra i due lati?", 75])
blocks.insert(k + 2, ["P", "Mobilità della caviglia: nella stessa posizione di affondo, porta il ginocchio anteriore in avanti, oltre la punta del piede, mantenendo il tallone ben appoggiato a terra. Il tallone si solleva presto? Il movimento è uguale a destra e a sinistra?", 75])

# move test-photo figure after the test descriptions
ki = [n for n, b in enumerate(blocks) if b[0] == "IMG" and b[1] == "p75_1"][0]
img = blocks.pop(ki)
k = find("Mobilità della caviglia:")
blocks.insert(k + 1, img)

k = find("Variante: esegui l'allungamento con una sola gamba")
blocks.insert(k + 1, ["IMG", "es6", 81])
FIG["es6"] = "PHOTO_ES6"

# Ch.8 Esercizio 4: variant with rotation removed at the author's request
k = find("Variante: aggiungi una rotazione toracica.")
del blocks[k]
# Monopodal bridge: refer to figure of level 1
k = find("Errori comuni: cedimento laterale del bacino")
blocks[k][1] += " La progressione fino al ponte monopodalico è illustrata nella figura dell'esercizio 2 del Livello 1."

# Farmer's carry: correct naming of the variants
k = find("Variante bilaterale (suitcase carry)")
blocks[k][1] = ("Variante bilaterale: porta un peso in ciascuna mano e cammina (è il farmer's carry nella sua forma classica; "
                "la versione con un solo peso è detta anche suitcase carry). È più semplice e meno impegnativa per i muscoli "
                "laterali del tronco, ma anche meno allenante in termini di stabilità.")

# Paragraph splits for run-on blocks
SPLITS = [
 " I segnali tipici della cervicalgia", " In molti casi questi sintomi", " La buona notizia è che la cervicalgia",
 " La gestione passa attraverso", " Il primo passo è l'osservazione.", " Il secondo passo è identificare",
 " Il terzo passo è lavorare", " Il quarto passo, quello che",
 " Sei arrivato alla fine di questo libro.", " Forse hai scoperto che", " Se è così, questo libro",
 " Hai capito che la colonna", " Hai scoperto che la diagnostica", " Hai avuto in mano un programma",
 " La seconda cosa è la pazienza.", " La terza cosa è non isolarti.",
 " In tutti questi anni di lavoro clinico", " Sei una di quelle persone.", " La tua schiena è più forte",
]
nb = []
for b in blocks:
    if b[0] == "P":
        t = b[1]
        for s in SPLITS:
            t = t.replace(s, "¶" + s.strip())
        for part in t.split("¶"):
            nb.append(["P", part.strip(), b[2]])
    else:
        nb.append(b)
blocks = nb

# ---------------------------------------------------------------- HTML rendering
def esc(s):
    s = html.escape(s, quote=False)
    s = s.replace("'", "’")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # typographic quotes: ’word’ used as quotation marks -> ‘word’
    s = re.sub(r"(^|[\s(“])’", r"\1‘", s)
    s = s.replace(" - ", " – ")
    return s

LEADINS = ["Serie e ripetizioni", "Perché", "Come (stacco rumeno)", "Come", "Errori comuni", "Progressione",
           "Variante bilaterale", "Variante", "Versione facilitata", "Versione senza pesi", "Versione ‘swimming’",
           "Il punto chiave", "Applicazione pratica", "Flessione in avanti", "Estensione", "Rotazione",
           "Apertura dell’anca", "Mobilità della caviglia", "Ponte glutei", "Quadrupedia bilanciata",
           "Squat su una gamba", "Ricerca chiave", "Dato chiave", "Test semplice per i glutei"]

def leadin(s):
    for l in LEADINS:
        if s.startswith(l + ":"):
            return f'<span class="lead-in">{l}:</span>' + s[len(l) + 1:]
    return s

chap = 0
figno = 0
secno = 0
toc = []
body = []
sec_id = 0
in_chapter = False
need_dropcap = False

def fig_html(src, cap, cls=""):
    global figno
    figno += 1
    lab = f"Figura {chap}.{figno}" if chap else f"Figura {figno}"
    return (f'<figure class="{cls}"><img src="fig/{src}" alt=""><figcaption>'
            f'<span class="fignum">{lab}</span>{esc(cap)}</figcaption></figure>')

def photo_html(cap, items):
    global figno
    figno += 1
    lab = f"Figura {chap}.{figno}"
    n = len(items)
    from PIL import Image as _I
    w, h = _I.open(os.path.join(W, "fig", items[0][0])).size
    land = " land" if w > h else ""
    cells = "".join(f'<div class="ph"><img src="fig/{s}" alt=""><span>{esc(t)}</span></div>' for s, t in items)
    return (f'<figure class="photos n{n}{land}"><div class="grid">{cells}</div><figcaption>'
            f'<span class="fignum">{lab}</span>{esc(cap)}</figcaption></figure>')

KEYLABELS = {"Dato chiave": "Dato chiave", "Ricerca chiave": "Ricerca chiave", "Test semplice per i glutei": "Prova anche tu"}

header_open = False
for tag, txt, pg in blocks:
    if header_open and tag != "LEAD":
        body.append("</header>"); header_open = False
    if tag == "H1":
        if in_chapter:
            body.append("</section>")
        m = re.match(r"Capitolo (\d+) — (.+)", txt)
        sec_id += 1
        sid = f"s{sec_id}"
        secno = 0
        if m:
            chap = int(m.group(1)); figno = 0
            title = m.group(2)
            body.append(f'<section class="chapter"><header class="opener"><div class="bignum">{chap:02d}</div>'
                        f'<div class="kicker">Capitolo {chap}</div><h1 id="{sid}">{esc(title)}</h1>')
            toc.append(("ch", f"{chap:02d}", title, sid))
        else:
            chap = 0 if txt == "Introduzione" else chap
            body.append(f'<section class="chapter unnumbered"><header class="opener"><div class="bignum"></div>'
                        f'<div class="kicker">{"Prima di iniziare" if txt == "Introduzione" else "Per concludere"}</div>'
                        f'<h1 id="{sid}">{esc(txt)}</h1>')
            toc.append(("ch", "", txt, sid))
        in_chapter = True
        need_dropcap = True
        header_open = True
        continue
    if tag == "LEAD":
        if txt.startswith("Una schiena sana non è assenza"):
            body.append(f'<div class="closing"><p>{esc(txt)}</p></div>')
        else:
            body.append(f'<p class="chapter-lead">{esc(txt)}</p>')
            if header_open:
                body.append("</header>"); header_open = False
        continue
    if tag == "H2":
        sec_id += 1; sid = f"s{sec_id}"
        numbered = chap > 0 and not (txt.startswith("Quello che hai") or txt.startswith("Cosa fare") or txt.startswith("Una parola finale"))
        lm = re.match(r"Livello (\d): (.+)", txt)
        if lm:
            secno += 1
            body.append(f'<h2 id="{sid}" class="level"><span class="lvl">Livello {lm.group(1)}</span>'
                        f'<span class="lvl-title">{esc(lm.group(2))}</span></h2>')
            toc.append(("h2", f"{chap}.{secno}", txt, sid))
            continue
        if numbered:
            secno += 1
            num = f"{chap}.{secno}"
            body.append(f'<h2 id="{sid}"><span class="secnum">{num}</span>{esc(txt)}</h2>')
            toc.append(("h2", num, txt, sid))
        else:
            body.append(f'<h2 id="{sid}">{esc(txt)}</h2>')
            toc.append(("h2", "", txt, sid))
        continue
    m = re.match(r"Esercizio (\d+): (.+?) Serie e ripetizioni: (.*)$", txt)
    if m:
        t = m.group(2).rstrip(". ")
        body.append(f'<div class="exercise"><div class="ex-head"><span class="ex-num">Esercizio {m.group(1)}</span>'
                    f'<span class="ex-title">{esc(t)}</span></div>'
                    f'<div class="ex-rx"><span class="rx-label">Serie e ripetizioni</span>{esc(m.group(3))}</div></div>')
        continue
    if tag == "H3":
        body.append(f"<h3>{esc(txt)}</h3>")
        continue
    if tag == "P":
        if txt.startswith("Durata consigliata"):
            d = txt.split(":", 1)
            body.append(f'<p class="duration"><span>{esc(d[0])}</span>{esc(d[1])}</p>'); continue
        if txt == "Dott. Gianluca Santambrogio":
            body.append(f'<p class="signature">{esc(txt)}</p>'); continue
        h = leadin(esc(txt))
        if 'class="lead-in"' in h:
            cls = ' class="li"'
        else:
            cls = ""
            if need_dropcap:
                cls = ' class="dropcap"'
                m2 = re.match(r"([A-ZÈÀ])(’)?(\S*)(.*)$", h, re.S)
                if m2:
                    h = f'<span class="dc">{m2.group(1)}</span>{m2.group(2) or ""}{m2.group(3)}{m2.group(4)}'
                need_dropcap = False
        body.append(f"<p{cls}>{h}</p>")
        continue
    if tag in ("BLUE", "ITAL"):
        body.append(f'<blockquote class="pull"><p>{esc(txt)}</p></blockquote>')
        continue
    if tag == "GREEN":
        label = "Da ricordare"
        for k, v in KEYLABELS.items():
            if txt.startswith(k + ":"):
                label = v; txt = txt[len(k) + 1:].strip(); txt = txt[0].upper() + txt[1:]
        body.append(f'<aside class="keybox"><div class="box-label">{label}</div><p>{esc(txt)}</p></aside>')
        continue
    if tag == "GREY":
        m = re.match(r"CASO CLINICO — (.+?\d+ anni, [^A-Z]+?)(?: ([A-Z].*))?$", txt)
        who, story = m.group(1).strip(), (m.group(2) or "")
        name, rest = who.split(",", 1)
        body.append(f'<aside class="case"><div class="box-label">Caso clinico</div>'
                    f'<div class="case-who"><strong>{esc(name)}</strong>,{esc(rest)}</div><p>{esc(story)}</p></aside>')
        continue
    if tag == "IMG":
        f = FIG[txt]
        if f is None:
            continue
        if isinstance(f, str):
            for cap, items in PHOTOS[f]:
                body.append(photo_html(cap, items))
            continue
        if isinstance(f, list):
            for x in f:
                body.append(fig_html(x[0], x[1], x[2] if len(x) > 2 else ""))
            continue
        body.append(fig_html(f[0], f[1], f[2] if len(f) > 2 else ""))
        continue
    print("UNHANDLED", tag, txt[:60])
body.append("</section>")

toc_html = []
for kind, num, title, sid in toc:
    if kind == "ch":
        lab = f'<span class="tnum">{num}</span>' if num else '<span class="tnum"></span>'
        toc_html.append(f'<li class="toc-ch"><a href="#{sid}">{lab}<span class="tt">{esc(title)}</span></a></li>')
    else:
        lab = f'<span class="snum">{num}</span>' if num else '<span class="snum"></span>'
        toc_html.append(f'<li class="toc-h2"><a href="#{sid}">{lab}<span class="tt">{esc(title)}</span></a></li>')

tpl = open(os.path.join(W, "template.html")).read()
doc = tpl.replace("{{TOC}}", "\n".join(toc_html)).replace("{{BODY}}", "\n".join(body))
open(os.path.join(W, "libro.html"), "w").write(doc)
print("chapters/sections:", len(toc), "figures written")
