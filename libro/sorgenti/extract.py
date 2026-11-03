import pymupdf as fitz, re
d=fitz.open("/home/user/maldischiena/libro completo da sistemare foto e indice-compressed.pdf")
COL={(0.918,0.957,0.984):"BLUE",(0.973,0.976,0.98):"GREY",(0.918,0.969,0.949):"GREEN"}
out=[]
for p in d:
    pn=p.number+1
    if pn<=6: continue
    bx=[(dr["rect"],COL.get(tuple(round(c,3) for c in dr["fill"]))) for dr in p.get_drawings() if dr.get("fill")]
    items=[]
    for b in p.get_text("dict")["blocks"]:
        if b["type"]==1: continue
        r=fitz.Rect(b["bbox"])
        txt="";sizes=[];fonts=[];red=False
        for l in b["lines"]:
            lt=""
            for s in l["spans"]:
                t=s["text"]
                if s["color"]==15597568: red=True
                if "Bold" in s["font"] and s["size"]==12 and t.strip(): t="**"+t+"**"
                lt+=t; sizes.append(s["size"]); fonts.append(s["font"])
            txt=(txt+" "+lt) if txt and not txt.endswith("-") else txt+lt
        txt=re.sub(r"\s+"," ",txt).strip().replace("****","")
        if not txt: continue
        sz=max(sizes,key=sizes.count); f=max(fonts,key=fonts.count)
        # box by first line center
        c=fitz.Point((r.x0+r.x1)/2, min(r.y0+14,(r.y0+r.y1)/2))
        col=None
        for bb,cc in bx:
            if bb.contains(c) and cc: col=cc
        if red: tag="RED"
        elif sz==20: tag="H1"
        elif sz==15 and "Bold" in f: tag="H2"
        elif sz==13 and "Bold" in f: tag="H3"
        elif sz==13 and "Italic" in f: tag="LEAD"
        elif col: tag=col
        elif sz==11 and "Bold" in f: tag="CASET"
        elif sz==11.5: tag="CASE"
        elif "Italic" in f: tag="ITAL"
        else: tag="P"
        items.append((tag,txt,r.y0))
    imgs=[(fitz.Rect(i["bbox"]).y0,i["bbox"]) for i in p.get_image_info()]
    allit=[(y,t,x) for t,x,y in items]+[(y,"IMG",f"{pn}:{[round(v) for v in bb]}") for y,bb in imgs]
    allit.sort(key=lambda z:z[0])
    for y,t,x in allit: out.append([t,x,pn])
m=[]
for t,x,pn in out:
    if m and m[-1][0]==t and t not in("H1","H2","H3","IMG","RED") and not re.search(r"[.!?:»”)\"'’]\**$",m[-1][1]) and (x[:1].islower() or pn==m[-1][2]):
        m[-1][1]+=" "+x; continue
    m.append([t,x,pn])
with open("raw.txt","w") as f:
    lastp=0
    for t,x,pn in m:
        if pn!=lastp: f.write(f"<!-- p{pn} -->\n"); lastp=pn
        f.write(f"{t}| {x}\n")
