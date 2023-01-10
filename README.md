# Prakses darbi

## IP adreses

koda darbība:
1. Kods atver teksta failus kas pārraksta viņus, rezultātā teksta fails ir bez neviena ieraksta
2. Kods atver mājas lapu kā tekstu, kur notiek dotās funkcijas IP adrešu meklēšana
3. Funkcijā tiek izmantota regex palīdzība, lai atrastu visas IP adreses ar vienu pārbaudi, nevelkot ārā kuri nav IP adreses un tiek izmantots sintakses 
    * Unikālo IP adrešu meklēšanā notiek tas pats, izmantojot regex palīdzību, tas izlasa visas IP adreses
    * Pēc unikālo IP adrešu atrašanas, taisa jaunu, netīši sakārtotā secībā IP adreses izmantojot set()
4. Tad kad funkcijas ir pabeigušas savu darbu, tiek atvērti teksta faili kas ievada IP adreses
