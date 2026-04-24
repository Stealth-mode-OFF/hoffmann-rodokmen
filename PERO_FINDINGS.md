# PERO OCR Findings — autopilot 2026-04-23/24

## Summary
- 7+ matrik přepsáno přes Kurrent (German, Czech) model
- 24 339+ řádků textu
- 70× Hoffmann/Hofmann, 57× Mathes, 40× Helena, 6× Eleonora

## Klíčové nálezy

### 1. Marginální anotace 1868 (35-13 line 17)
```
Hoffmann, Franz Hufschmied und Feldgärtner in
Belaun [č.]80 geboren in Silberleut
```
**Význam:** Anotace 1868 u svatebního zápisu rodičů (JF × ??). Franz = Franz Xaveri Johann
Hoffmann *1799 (syn JF), kovář v Bělouni č.80. Potvrzuje pravost svatby 1791
+ generační návaznost JF → Franz Xaveri.

### 2. Helena Mathesin v indexu 188-2 (Žireč N 1782-1795)
Multiple výskyty v indexu/seznamu kmotrů:
- Line 5594-5596: `Hutmacher / Helena / Mathese`
- Line 7434-7436: `1. / Helena / Matessin sein`
- Line 8944-8946: `Marian / Mathesin / Als Rath`

**Mathesin/Matessin = Mathes ž.r. (Mathesová)**. Helena Mathes byla žijící
osoba aktivní v Žireč farnosti 1782-1795. Pravděpodobně **manželka JF**
(narozena 23.2.1774 Silberleit, zápis křtu v 35-6 page 92).

### 3. Selena (= Helena) v 35-13 — multiple entries
- Line 521-526: `Sylberli / Selena / Tochter des / Josep Matsumd Poin` →
  Helena dcera Josepha Math[es] (Bauer) ze Silberleitu
- Line 1832: `Selena Tochter ... dorph Mat... Posina`
- Line 2302-2306: `Hofmann. / Selena / Tochter des / er / Ab / Hofsmann` →
  Helena dcera Hoffmanna (cousin marriage hypothesis)
- Line 5462: `Copul Selena Daolaw kowa Acra dana Wailawita`

### 4. Cross-link Hoffmann ↔ Hutmacher / Hufschmied / Feldgärtner
- Hutmacher (klobouk) — line 5594 (Helena Mathese context)
- Hufschmied (kovář) — line 17 (Franz Xaveri JF syn)
- Feldgärtner (polní zahradník) — line 17

Hoffmann rodina = řemeslníci v regionu (kovář, klobouk, zahradník).

## Negativní výsledky
- **Möckler 0×** v žádné matrice — definitivně NE bride name (byl OCR omyl mé
  původní transkripce)
- **Tschenek 0×** v matrikách 1782-1814 (bude až 34-20 Dubenec OZ + 181A Zaloňov O)
- **Libotov 0×** ve fulltextu! Hypotéza "Helena z Libotova" v MyHeritage = chyba

## Statistika OCR
| Slovo | Výskyty |
|---|---|
| Richter | 189 |
| Hoffmann + Hofmann | 70 |
| Mathes (incl. Mathesin) | 57 |
| Helena (incl. Selena) | 40 |
| Silberleut | 9 |
| Eleonora | 6 |
| Hass | 4 |
| Vestec | 1 |
| **Möckler / Mödler** | **0** |
| **Tschenek / Cenek** | **0** |
| **Libotov / Liebthal** | **0** |

## Stav PERO pipeline (running, 2026-04-24 @ 00:30)
- 12+ docs uploadnuto (matriky 188-x, 34-x, 35-x, 61-x)
- Orchestrator polluje + auto-trigger OCR + extrahuje text + grep
- Findings uloženy do `~/matriky/pero_findings.md` + tato MD synchronizována na repo
