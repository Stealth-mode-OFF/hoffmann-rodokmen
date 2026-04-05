# Prompt pro Claude Code — Rodokmen Hoffmann/Hofman

Zkopíruj a vlož do nové Claude Code session:

---

## Pokračuj v práci na rodokmenu Hoffmann/Hofman

Máš nastavené 2 MCP servery (Gramps + FamilySearch) a kompletní infrastrukturu. Tady je co potřebuješ vědět:

### Co běží
- **Gramps Web** na `localhost:5050` (Docker, user: josef / hoffmann2026) — 44 osob, 9 rodin importováno z GEDCOM
- **Gramps MCP** — 16 nástrojů (find_type, find_anything, create_person, get_ancestors, get_descendants...). Zkus: `find_anything` s query "Hoffmann"
- **FamilySearch MCP** — 9 nástrojů (search-records, search-persons, get-ancestors...). **POTŘEBUJE API KLÍČ** — registruj se na https://www.familysearch.org/developers/ a pak `configure` s Client ID
- **Vercel** — https://hoffmann-rodokmen.vercel.app (live HTML rodokmen)
- **GitHub** — https://github.com/Stealth-mode-OFF/hoffmann-rodokmen

### Soubory
- `/Users/josefhofman/hoffmann-rodokmen/` — git repo se vším
- `/Users/josefhofman/hoffmann-rodokmen.html` — zdrojový HTML rodokmen (44 osob, 9 generací, horoskopy)
- `/Users/josefhofman/hoffmann-rodokmen/hoffmann-rodokmen-complete-2026-04-04.ged` — GEDCOM 5.5.1
- `/Users/josefhofman/hoffmann-rodokmen/HOFFMANN_RESEARCH_REPORT.md` — archivní výzkum
- `/Users/josefhofman/hoffmann-rodokmen/FAMILYSEARCH_RESEARCH.md` — FamilySearch guide

### Co dělat dál (priority)

1. **Gramps MCP test** — zkus `find_anything` query "Hoffmann" a ověř že MCP funguje. Pak `tree_stats` pro statistiky.

2. **FamilySearch API klíč** — zeptej se Josefa jestli má Client ID z https://www.familysearch.org/developers/. Pak `configure` + `authenticate`. Potom:
   - `search-records` surname="Hoffmann" birthPlace="Rtyne" — české matriky!
   - `search-records` surname="Hoffmann" birthPlace="Dvur Kralove" — Sylvárov
   - `search-persons` name="Josef Hoffmann" birthDate="1894" — hledej ve Family Tree

3. **Hledej chybějící manželky** — 4 zbývají:
   - Manželka Josepha Franze (~1766) — matka 12 dětí
   - Manželka Franze Xaveri (1799) — sňatek ~1818
   - Manželka Franze podkováře (1825)
   - Manželka Josefa (1857)
   → Hledej v matrikách oddaných (Trauungsbücher) farnosti Zaloňov a Dvůr Králové

4. **WWI — Josef (1894)** — `search-records` surname="Hoffmann" birthDate="1894" collection="WWI" nebo hledej na Verlustlisten (des.genealogy.net)

5. **MyHeritage** — Josef má premium účet (jsfhofman@gmail.com). Nemá API — jen manuální Record Matching. Připomeň mu ať uploadne GEDCOM a spustí matching.

6. **FamilySearch census** — sčítání Trutnov 1869-1921 (catalog/2101223) — hledej Rtyně č. 27 podle čísla domu. Najdeš tam všechny obyvatele za 50 let!

### Klíčové lokace
⚠️ **POZOR:** Rtyně v rodokmenu = **Rtyně u Velichovek / Rtyně u Zaloňova** (obec Zaloňov, u Jaroměře), NE Rtyně v Podkrkonoší (u Trutnova)! Stejné německé jméno "Hertin" pro obě obce.

| Matrika | Moderní název | Okres | Farnost |
|---------|--------------|-------|---------|
| Silberleut/Silwerleut | **Sylvárov** (Dvůr Králové) | Trutnov | Dvůr Králové n. L. |
| Bělouň/Bielaun | **Běluň** (Heřmanice) | Náchod | Jaroměř |
| Rtyně/Hertin č. 27 | **Rtyně u Zaloňova** (obec Zaloňov) | Náchod | **Zaloňov** (od 1785) |
| Vesce/Vestec | **Vesce** (obec Zaloňov) | Náchod | Zaloňov |
| Lišice/Lischitz | **Lišice** | Hradec Králové | — |

### Nalezené matriční knihy (digitalizované, SOA Zámrsk)
| Signatura | Farnost | Typ | Roky | Pokrývá |
|-----------|---------|-----|------|---------|
| 66-9 | Jaroměř | Narození | 1822-1834 | Děti F. Xaveri v Běluně |
| 66-10 | Jaroměř | Narození | 1835-1841 | Děti F. Xaveri v Běluně |
| 66-29 | Jaroměř | Oddací | 1810-1834 | Sňatek F. Xaveri ~1824 |
| 181A-4224 | Zaloňov | Oddací | 1839-1895 | Sňatek Franze ~1851 + Josefa ~1891 |
| 181A-4213 | Zaloňov | Narození | 1839-1895 | Děti v Rtyni č. 27 |

### Pravidla
- Všechno česky (rodokmen, noty, komentáře)
- Po každé změně: `cp hoffmann-rodokmen.html hoffmann-rodokmen/index.html && vercel --yes --prod --scope josefs-projects-e1e25112`
- Git: `git add -A && git commit && git push origin main`
- HTML je na `/Users/josefhofman/hoffmann-rodokmen.html`
- GEDCOM je v `/Users/josefhofman/hoffmann-rodokmen/hoffmann-rodokmen-complete-2026-04-04.ged`
- Gramps Web Docker musí běžet: `cd ~/projects/gramps-web && docker compose up -d`
