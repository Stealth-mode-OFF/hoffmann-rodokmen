# Prompt pro Claude Code — Rodokmen Hoffmann/Hofman

Zkopíruj a vlož do nové Claude Code session:

---

## Pokračuj v práci na rodokmenu Hoffmann/Hofman

### Stav po swarm session 2026-04-22 (viz SWARM_RESEARCH_2026-04-22.md)

**Nejstarší doložený předek stále:** Joseph Franz Hoffmann (\*~1766, †3. 3. 1828 Silberleut č. 12) + Helena Haße (Libotov, ~1770).

**Klíčové korekce z posledního výzkumu:**
1. ⚠️ **Silberleut patřil nejspíš Šporkům (panství Choustníkovo Hradiště)**, NE jezuitům Žireč. Proto matriky mohou být v **jiném fondu** než jsme dosud otevřeli.
2. ⚠️ **Po 1773 parochiálně pod Dvůr Králové**, ne Žireč. Úmrtní zápis Joseph Franze (3. 3. 1828) hledat ve **fondu Dvůr Králové**, ne 188-4 Žireč.
3. ✅ **Hoffmann NENÍ mezi tradičními rody Silberleutu** (Patzak, Radda, Erbert, Honal, Turnwald, Schiller, Fiedler) — Joseph Franz se tam přiženil ~1793. Křest hledat jinde.
4. ✅ **Nikdo jiný linku online nedokumentuje** — jsme první. Pull-forward přes veřejné stromy nevyšel.

### Priority akcí (v pořadí hodnoty)

#### P0 — SVATBA 1793 = rodiče obou párů v 1 zápisu
- Matrika **188-3 O Žireč 1782-1814, strany 10-11** (rok 1793)
- Direct JPG URL nefunguje (matriky.online vrací HTML redirect bez browser session)
- **Řešení:** otevřít ručně v prohlížeči přes matriky.online nebo ARON (aron.vychodoceskearchivy.cz, UUID pro 188-3 je nutné dohledat ve finding aid fondu 188)
- **Očekávaný výstup:** jména otce + matky Joseph Franze + otce + matky Heleny Haße + jejich místa původu

#### P1 — PŘIHLÁŠENÝ FamilySearch
- Otevři [PZ5T-1QY (Helena Haße)](https://www.familysearch.org/en/tree/person/details/PZ5T-1QY) v přihlášeném browseru
- Sources tab může obsahovat matriční reference nebo rodičovský profil
- Family view ukáže, jestli je Joseph Franz jako manžel propojen a zda má rodiče

#### P2 — INDEX 34-21 NOZ 1653-1760
- 106 stran abecedního indexu pro celou farnost Dubenec (9 vesnic)
- **Písmeno H = odhadem strany 25-40**
- Vyhledá všechny Hoffmann + Haße záznamy 1653-1760 v 1 projití

#### P3 — MATRIKY CHOUSTNÍKOVO HRADIŠTĚ (dosud nezkoumané)
- Šporkovské panství, potenciální matriky pro Silberleut před 1773
- V SOA Zámrsk / ARON najít fond fary Choustníkovo Hradiště
- Pokud Silberleut tam měl matriční záznamy, rodiče Joseph Franze budou tam, ne ve fondu 34

#### P4 — EMAIL W. HONAL
- Draft připravený v `EMAIL_HONAL_DRAFT.md` (němčina)
- Honal má matriční výpisy Žireč 1760-1830 pro sousední rody
- Nejpravděpodobnější regionální pull forward

#### P5 — TRANSKRIBUS AI TRANSKRIPCE
- 10 dokumentů uploaded, 470 str. matrik
- Potřeba dokoupit ~430 kreditů (~20 €)
- Po transkripci fulltext search "Hoffmann", "Haße", "Silberleut", "Libotov"

#### P6 — TEREZIÁNSKÝ KATASTR 1748 (ověření panství Silberleut)
- Národní archiv Praha-Dejvice, fond TK
- Určí definitivně: Šporkové vs. jezuité vs. Dvůr Králové pro Silberleut
- Odpoví na otázku: kam patří matriky pro Silberleut před 1773?

### Infrastruktura (nezměněno)
- **Gramps Web** localhost:5050 (josef / hoffmann2026) — 44 osob, 9 rodin
- **Gramps MCP** — 16 nástrojů
- **FamilySearch MCP** — vyžaduje API klíč (registrace na familysearch.org/developers/)
- **Vercel** — https://hoffmann-rodokmen.vercel.app
- **GitHub** — https://github.com/Stealth-mode-OFF/hoffmann-rodokmen
- **GEDCOM** — `/Users/josefhofman/hoffmann-rodokmen/hoffmann-rodokmen-complete-2026-04-04.ged`
- **Matriky už stažené** (6 JPGů) v `matriky/` — ale jen 1400x1106 grayscale, nedostatečné pro OCR Kurrent

### Matriční inventář — kompletní
Viz `SESSION_2026-04-17_MATRIKY.md` — nezměněno.

### Klíčové lokace (připomenutí)
⚠️ **POZOR:** Rtyně v rodokmenu = **Rtyně u Zaloňova** (u Jaroměře, farnost Zaloňov od 1785), NE Rtyně v Podkrkonoší. Silberleut = **Sylvárov**, dnes k.ú. Dvora Králové n. L.

### Technické pravidlo
- Matriky.online přímý curl NEFUNGUJE — vrací HTML. Nutný Playwright + browser session nebo stažené JPGy přes "Save as".
- Claude multimodal OCR na 1400×1106 grayscale Kurrent = nespolehlivé. Pro OCR je nutné full-res 3000×2000+ nebo Transkribus AI.
