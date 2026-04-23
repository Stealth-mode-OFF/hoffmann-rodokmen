# Email pro Michal Hradiš — PERO API klíč

**To:** ihradis@fit.vut.cz
**Subject:** Žádost o testovací API klíč PERO OCR — genealogický projekt Hoffmann / Silberleut

---

Vážený pane Hradiši,

píšu Vám kvůli žádosti o **testovací API klíč k PERO OCR**. Stavím online
rodokmen své rodiny **Hoffmann / Hofman ze Silberleutu (Sylvárov)** u Dvora
Králové, generace 1658 až současnost — všechny zdroje jsou primární
matriky ze SOA Zámrsk.

**Projekt:** https://hoffmann-rodokmen.vercel.app

## Co už jsem s PERO ručně udělal

- **86 stránek matriky 35-13 Dvůr Králové O 1785-1810** zpracováno přes
  Kurrent (German, Czech) OCR + German language model — 24 214 řádků textu.
- Díky OCR fulltextu jsem našel kritické fragmenty ke svatbě mého přímého
  předka Joseph Franz Hoffmann × nevěsta (1791, Silberleut), které nebyly
  čitelné v běžném prohlížeči matriky.
- Dokument testovací: `7c1a1348-c506-4000-aa04-f908bb0cfa6f`
- Účet: Josef Hofman (chatujsgpt@gmail.com), registrovaný 23.4.2026.

## Proč potřebuji API klíč

Mám **~3500 dalších stránek** ze 29 matrik (fondy 34 Dubenec, 35 Dvůr
Králové, 61 Choustníkovo, 127 Pilníkov, 188 Žireč) stažených z SOA
Zámrsk, které chci systematicky projít přes Kurrent OCR. Ruční upload
přes drag-and-drop (max ~100 stránek / batch) je časově nereálný.

API (dle Vaší Swagger specifikace https://app.swaggerhub.com/apis-docs/
LachubCz/PERO-API/1.0.4) mi umožní:

1. Skriptovat vytvoření document / upload image / trigger OCR
2. Pollovat stav a stahovat výsledky (ALTO/PAGE XML/TXT)
3. Zpracovat celý fond za jednu noc místo několika dní

## Kontext výzkumu

Matrika 35-13, folio 72, 1. zápis vpravo (8.12.1791): svatba **Joseph
Frantz Hoffmann × Anna (příjmení v rukopisu těžko čitelné, pravděpodobně
Mathes nebo Hoffmann ze Silberleut č. 16)**. Nevěsta *23.2.1774,
Silwarleut. Ženich 24 let, ze Silwarleut.

Úmrtí JF doloženo 35-19 folio 173, březen 1828, č. 12 Silwarleut, věk 62.

Web ukazuje 9 generací rodu, využití matrik jako zdroje, přiřazení
křestních listů ke konkrétním folio v matrikách, plný přepis z PERO OCR.

## Technické detaily pro OCR

- **Použitý model:** `Kurrent (German, Czech)` + language model `German`
- **Baseline:** `Handwritten`
- **Kvalita skenů:** 5500 × 4400 px JPG, originál SOA Zámrsk
- **Jazyk:** staroněmecký Kurrent + latinské šablony matrik, 1650-1860

Celkový objem: ~13 GB JPG, 3 500 stránek. Podle Vaší "API documentation"
na hlavní straně je pro takový objem API klíč doporučený způsob.

## Reciprocita

PERO už mi výrazně pomohlo. Rád se podělím o:
- GEDCOM celého rodokmenu po dokončení
- Popis OCR chyb + CER odhady na konkrétních stránkách (pomoc pro
  případné trénovací data)
- Public link na zpracovanou matriku 35-13 (Sylvárov filia) jako
  reference pro ostatní badatele, pokud by to pomohlo.

Kontakt:
- Josef Hofman
- Praha, Česká republika
- email: chatujsgpt@gmail.com
- projekt: https://hoffmann-rodokmen.vercel.app

Mockrát děkuji za PERO — bez něj by 19. století zůstalo pro amatéry
genealogy za zdí ručního čtení Kurrentu. Snad mi API klíč umožníte.

S pozdravem,
Josef Hofman
