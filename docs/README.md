# GadgetFreak
Družabno omrežje za lastnike kakršnih koli naprav.

## Opis aplikacije
Vaša prijateljica Rozina ima idejo kako združiti vse ljubitelje takšnih in drugačnih elektronskih naprav, po domače gadgetov. Rada bi naredila neke sorte družbeno omrežje, kjer si bodo lahko lastniki različnih naprav izmenjali izkušnje. Rozina ima samo eno težavo... ne ve prav nič o spletnem programiranju. Pomagajte ji narediti spletno aplikacijo, ki bo omogočala vsaj naslednje:
- registracijo novega uporabnika,
- dodajanje nove naprave (npr. iPhone),
- dodajanje tehničnih lastnosti naprave,
- dodajanje slik naprave,
- dodajanje preizkusov naprave,
- forum za vsako napravo (dodajanje teme, odgovori),
- komentarji uporabnikov, kjer je to smiselno.

## Ciljna publika in naprave
Aplikacija cilja na uporabnike vseh starosti, ki si želijo sodelovati v družabnem omrežju, v katerem glavno vlogo igrajo njihove naprave. Uporabnik lahko brska po napravah in forumih naprav, če se registrira pa lahko tudi išče po napravah in sodeluje z dodajanjem novih naprav, komentarjev in ocen naprav. Aplikacija je narejena za tri velikosti naprav: mobilne telefone, tablice in velike zaslone.

## Težave v brskalnikih
Aplikacijo sem razvijal v brskalniku Google Chrome (54.0.2840.100 (64-bit)), preizkusil pa sem jo še v  Mozilli Firefox (50.0) in Operi (41.0.2353.69).

Največ težav sem imel z brskalnikom Mozilla Firefox, saj se širina vnosnih polj ni pravilno nastavila. To sem popravil tako, da sem uporabil CSS funkcijo calc(). Na srečo se izgled v Google Chromu ni pokvaril. Z brskalnikom Opera ni bilo večjih težav.

Razlike med brskalniki so opazne predvsem pri velikosti in poudarjenosti besedila.

## Najboljša gradnika
Najboljša gradnika v moji aplikaciji sta, po mojem mnenju, gradnik, ki poveča izbrano sliko (na strani device-info-li.html), ki deluje s pomočjo Javascript-a, deluje pa tudi, če ta ni prisoten. Drugi najboljši gradnik je vnosno polje za iskanje, ki je prisotno na vseh straneh prijavljenega uporabnika.

## Komentarji in pripombe

### Opomba o označevanju datotek
HTML datoteke so označene po naslednji logiki:
- datoteke oblike _*-li.html_ so strani prijavljenega uporabnika; stran neprijavljenega uporabnika se nahaja v datoteki z enakim imenom brez niza _-li_
- datoteke, ki niso podvojene na zgornji način predstavljajo strani, da katerih lahko dostopa le prijavljen uporabnik; edina izjema je stran _registracija.html_, do katere lahko dostopajo samo neprijavljeni uporabniki
- datoteke  oblike _di*.html_ so strani, ki jih uporablja stran _device-info.html_ za povečevanje slik na brskalnikih z onemogočenim Javascript-om; v končni implementaciji bo za generiranje teh strani poskrbel strežnik

### Problemi, ki jih je treba še rešiti
Aplikacijo bi bilo treba bolje optimizirati za različne brskalnike. V trenutnem stanju strani delujejo, obstajajo pa določeni elementi, ki izstopajo. Večina ostalih problemov pa se navezuje na strežniški del aplikacije.
