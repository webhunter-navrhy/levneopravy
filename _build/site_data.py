#!/usr/bin/env python3
"""Ruční obsah z levneopravy.cz (stav 5. 10. 2026) → _data/site.json. Všechno doložené z jejich webu."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = {
 "name": "Levné opravy & montážní servis",
 "brand_short": "Levné opravy",
 "domain": "https://levneopravy.cz",
 "phone": "+420 731 840 806", "phone_href": "+420731840806",
 "email": "info@levneopravy.cz",
 "hours": "PO až PÁ 8:00–18:00", "hours_weekend": "Víkend dle dohody",
 "area": "Působíme po celé České republice",
 "company": "Levné opravy – Praha", "ico": "872 94 231", "seat": "Na Proseku 35/2, Praha 9",
 "slogan": "Naše činnost směřuje k jedinému cíli, a tím je spokojený zákazník.",
 "intro": "Nabízíme pomoc při řešení oprav vašich bytů, domů, penzionů, komerčních či nebytových prostor, a dále nabízíme i ostatní související řemeslné služby, které právě potřebujete.",
 "intro2": "Zaručíme Vám kvalitní provedení všech oprav, služeb a dalších prací, jejichž cenu se však snažíme vždy přizpůsobit individuálně konkrétním požadavkům.",
 "nav": [
  {"t": "Domů", "h": "/"},
  {"t": "O nás", "h": "/o-nas/"},
  {"t": "Montáž dveří a obložek", "h": "/sluzba/montaz-dveri-a-oblozek/"},
  {"t": "Naše služby", "h": "/nase-sluzby/", "sub": "main"},
  {"t": "Další služby", "h": "/dalsi-sluzby/", "sub": "other"},
  {"t": "Ceník", "h": "/cenik/"},
  {"t": "Reference", "h": "/reference/"},
  {"t": "Kontakt", "h": "/kontakt/"}
 ],
 "can_do": ["instalatérské a elektrikářské práce, opravy elektrospotřebičů", "kuchyně na míru, montáž kuchyní, truhlářské práce",
   "pravidelná údržba bytů, domů, hotelů, SVJ", "montáž dveří a obložkových zárubní", "zednické práce, bytová jádra, čištění odpadů",
   "podlahářské, obkladačské a zahradnické práce", "vyklízecí práce, zámečnické a výškové práce", "hodinový manžel, markýzy a rolety, dřevostavby",
   "malířské práce, stěhování, doprava…"],
 "marquee": ["Instalatér", "Elektrikář", "Truhlář", "Zedník", "Obkladač", "Malíř", "Podlahář", "Zámečník", "Klempíř", "Zahradník", "Hodinový manžel", "Montáž kuchyní", "Montáž dveří", "Stěhování"],
 "perks": [
  {"k": "cr", "t": "Po celé České republice", "d": "Hlavní lokality Praha, Brno a Olomouc, montážní servis po celé republice."},
  {"k": "obi", "t": "Partner prodejen OBI", "d": "Doprovázíme Vás při realizacích i výběru vhodných materiálů."},
  {"k": "cena", "t": "Cenu znáte předem", "d": "Odhad ceny Vám sdělíme předem – jednáme fér."},
  {"k": "cert", "t": "Certifikáty a revize", "d": "Požárně bezpečnostní certifikát k protipožárním dveřím, revize elektro."}
 ],
 "offices": [
  {"t": "Levné opravy – Praha", "a": "Na Proseku 35/2, Praha 9"},
  {"t": "Pobočka Praha 9", "a": "Třtinová 523/27, Praha 9"},
  {"t": "Pobočka Praha 10", "a": "28. pluku 920/20, Praha 10"},
  {"t": "Levné opravy – Brno", "a": "Jana Babáka 2733/11, Brno"},
  {"t": "Levné opravy – Olomouc", "a": "tř. Kosmonautů 1221/2a, Olomouc"}
 ],
 "branches": [
  ["Beroun", "Plzeňská 475, 267 01 Králův Dvůr u Berouna", 14.03, 49.95],
  ["Brno", "Sokolova 622/1, 619 00 Brno-jih", 16.61, 49.18],
  ["Česká Lípa", "Borská 3218, 470 01 Česká Lípa 6", 14.54, 50.685],
  ["Cheb", "Dragounská 2563/4, 350 02 Cheb", 12.37, 50.08],
  ["Frýdek-Místek", "Příborská 2410, 738 01 Frýdek-Místek", 18.35, 49.685],
  ["Havířov", "Před tratí 4/1433, 735 64 Havířov", 18.43, 49.78],
  ["Hradec Králové", "Akademika Bedrny 532/10b, 500 02 Hradec Králové", 15.83, 50.21],
  ["Jablonec nad Nisou", "Želivského 5231/2a, 465 05 Jablonec nad Nisou", 15.17, 50.725],
  ["Jihlava", "Romana Havelky 4854/5, 586 01 Jihlava", 15.59, 49.40],
  ["Karlovy Vary", "Chebská 380/81B, 361 20 Karlovy Vary", 12.85, 50.23],
  ["Klatovy", "Domažlická 15, 339 01 Klatovy", 13.29, 49.395],
  ["Kolín", "V kasárnách 1022, 280 02 Kolín", 15.20, 50.03],
  ["Litoměřice", "Želetická 2227, 412 01 Litoměřice", 14.13, 50.535],
  ["Mladá Boleslav", "Na Radouči 1225, 293 01 Mladá Boleslav", 14.90, 50.415],
  ["Most", "Chomutovská 1316, 434 01 Most", 13.64, 50.50],
  ["Olomouc", "Horní Lán 2, 779 00 Olomouc", 17.25, 49.59],
  ["Opava", "Hlučínská 51, 747 05 Opava", 17.90, 49.94],
  ["Ostrava-Zábřeh", "Výškovická 46/3123, 700 30 Ostrava-Zábřeh", 18.25, 49.795],
  ["Písek", "U Nádraží 2607, 397 01 Písek", 14.15, 49.31],
  ["Plzeň", "Sukova 886/21, 301 00 Plzeň – Jižní předměstí", 13.37, 49.74],
  ["Praha Modřany", "Lhotecká 446, 143 00 Praha-Modřany", 14.42, 50.00],
  ["Praha Prosek", "Prosecká 78, 140 00 Praha", 14.50, 50.12],
  ["Praha Roztyly", "Tomíčkova 9, 148 00 Praha-Roztyly", 14.48, 50.04],
  ["Praha Ruzyně", "Výtvarná 3/1033, 161 00 Praha-Ruzyně", 14.30, 50.08],
  ["Praha Štěrboholy", "Nákupní 390/4, 102 00 Praha-Štěrboholy", 14.55, 50.07],
  ["Přerov", "Polní 2992/11, 750 02 Přerov", 17.45, 49.455],
  ["Příbram", "Žežická 596, 261 01 Příbram", 14.01, 49.69],
  ["Prostějov", "Konečná 4564/10, 796 07 Prostějov", 17.11, 49.47],
  ["Teplice", "Seifertova 1965, 415 01 Teplice", 13.82, 50.64],
  ["Trutnov", "Obchodní 134, 541 01 Trutnov", 15.91, 50.56],
  ["Ústí nad Labem", "Tyršova 885, 400 04 Ústí nad Labem – Trmice", 14.00, 50.645],
  ["Zlín-Malenovice", "Centro Zlín, 763 02 Zlín-Malenovice", 17.59, 49.205]
 ],
 "pricing": {
  "items": [
   {"t": "Doprava po Praze", "p": "300 Kč", "n": ""},
   {"t": "Doprava mimo Prahu", "p": "7 Kč/km", "n": ""},
   {"t": "Výjezd technika na zaměření a vypracování cenové nabídky", "p": "500 Kč", "n": ""},
   {"t": "Montáž kuchyňské linky", "p": "od 990 Kč/bm", "n": "", "link": "/sluzba/montaz-kuchyni/"},
   {"t": "Montáž nábytku všech značek", "p": "od 190 Kč/h", "n": "", "link": "/sluzba/montaz-kuchyni/"},
   {"t": "Akce: výměna vchodových či bytových dveří", "p": "10 990 Kč", "n": "celkem za dopravu, materiál i práci", "link": "/sluzba/akce/", "hl": True}
  ],
  "notes": ["ceny nezahrnují materiál", "ceny jsou závislé na individuální dohodě"]
 },
 "references": [
  ["rekonstrukce koupelen", "Praha 4"], ["montáž markýzy", "Praha 6"], ["montáž zahradního domku Biohort Highline", "Čakovice"],
  ["montáž přístřešku OBI parkoviště", "Praha 9"], ["výkopové práce", "Morava"], ["stavba opěrné stěny a revitalizace rybníku", "Morava"],
  ["montáž vchodových dveří", "Praha 9"], ["výroba mobilního domu", "Morava"], ["pokrývačské a klempířské práce, K Sídlišti", "Čakovice"],
  ["pokládka plovoucí podlahy, Terezínská", "Prosek"], ["výroba a montáž mříží, Rumburská", "Prosek"],
  ["oprava a nátěr fasády rodinného domu, Třtinová", "Čakovice"], ["oprava vstupního vchodu panelového domu, Rumburská", "Prosek"],
  ["montáž sprchového koutu, Litoměřická", "Prosek"], ["zámečnické práce, Drahobejlova", "Na Balabence"], ["údržba zahrady, Štefánikova", "Zeleneč"],
  ["malířské práce, Slavíkova", "Vinohrady"], ["sklenářské práce", "Rohanské nábřeží"], ["montáž videozvonku, Na Jahodách", "Kunratice"],
  ["elektrikářské práce", "Horní Počernice"], ["postavení betonového plotu, Štefánikova", "Zeleneč"], ["vyklizení suterénu, Bohušovická", "Prosek"],
  ["oprava vchodu, Pískovcová", "Prosek"], ["montáž bojleru, Koněvova", "Jarov"]
 ],
 "reviews": [
  {"n": "Patricie Lav", "c": "Praha", "s": "montaz-kuchyni", "q": "Firmu jsem využila už jednou na montáž kuchyně, která proběhla bez problému a podle mého očekávání. Tentokrát jsem ji oslovila na výměnu vchodových dveří, která proběhla v naprostém pořádku. Komunikace s firmou byla výborná a vyšla vstříc mým požadavkům, přičemž montáž opět proběhla bezproblémově a velice rychle. Potřebný úklid po pracovnících byl potřeba jen v minimálním rozsahu, což mě velice potěšilo. Firmu mohu jen doporučit."},
  {"n": "Radek Oto", "c": "Praha", "s": "obkladacske-prace", "q": "Firmu jsem nakontaktoval kvůli výměně dlažeb v domě. Řemeslníci nedělali zbytečný hluk a nepořádek. Vše mi připadalo velice profesionální a dlažba je krásně rovná. Doporučuji všem i pro slušné jednání i cenu."}
 ],
 "partners": [["obi_partner", "OBI"], ["rsd_partner", "ŘSD ČR"], ["letiste_partner", "Letiště Praha"], ["benzina_partner", "ORLEN Benzina"], ["prodoma_partner", "PRO-DOMA stavebniny"]],
 "groups": [["vse", "Vše"], ["byt", "Byt a koupelna"], ["dum", "Dům a zahrada"], ["kov", "Kov a dřevo"], ["udrzba", "Údržba a stěhování"]]
}
json.dump(S, open(os.path.join(ROOT, '_data', 'site.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('site.json ok')
