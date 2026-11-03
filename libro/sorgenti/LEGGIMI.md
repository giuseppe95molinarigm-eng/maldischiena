# Sorgenti dell'impaginazione

- `raw.txt`: testo estratto dal PDF originale, con un tag di struttura per ogni blocco (titoli, paragrafi, box).
- `fixes.py`: elenco delle correzioni testuali (prima → dopo).
- `build.py`: applica le correzioni, inserisce le figure e genera `libro.html`.
- `template.html`: grafica del libro (formato 17×24 cm, font, intestazioni, indice automatico).
- `fig/`: tutte le immagini usate (le foto dell'autore sono `foto00.jpg` … `foto11.jpg`).

Per rigenerare il PDF:

    pip install weasyprint
    python3 build.py
    python3 -c "import weasyprint; weasyprint.HTML('libro.html', base_url='.').write_pdf('libro.pdf')"
