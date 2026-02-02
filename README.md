# Docker Compose – Orkestracija i upravljanje multi-container aplikacijama

## Opis projekta

Ovaj projekat demonstrira kreiranje i upravljanje multi-container aplikacijom korišćenjem alata Docker Compose. Kroz praktičan primer prikazano je kako se definišu i konfigurišu različiti servisi, kako se uspostavlja njihova međusobna komunikacija, kao i kako se upravlja redosledom pokretanja i inicijalizacijom zavisnih komponenti.

Aplikacija se sastoji od backend servisa implementiranog u Python-u (Flask) i PostgreSQL baze podataka, koji predstavljaju razvojno okruženje.


## Upoznavanje sa tehnologijom

Docker Compose je alat koji je deo Docker ekosistema i služi za definisanje, pokretanje i upravljanje aplikacijama koje se sastoje od više kontejnera. Omogućava da se kompletna arhitektura aplikacije opiše deklarativno u jednom YAML fajlu (`docker-compose.yml`), uključujući servise, mreže, volumene i njihove međusobne zavisnosti.

Umesto da ručno pokrećemo svaki deo projekta, Docker Compose omogućava centralizovano upravljanje sistemom, čime se pojednostavljuje razvoj, testiranje i lokalno pokretanje kompleksnih aplikacija i na taj način ne narušavamo deljeno okruženje.

##  Zašto Docker Compose postoji i koji problem rešava

Savremene softverske aplikacije retko se sastoje od jedne izolovane komponente. Umesto toga, one su najčešće organizovane u mikroservisnu arhitekturu, kao što su backend aplikacija, baza podataka, pomoćni radni servisi (worker-i), kao i dodatne komponente za keširanje ili razmenu poruka. Svaka od ovih komponenti ima svoju ulogu u sistemu, ali istovremeno zavisi od pravilnog funkcionisanja ostalih i njihove međusobne kominikacije.

Bez odgovarajućeg alata za orkestraciju, upravljanje ovakvim sistemima postaje složeno i sklono greškama. Programeri su prinuđeni da ručno pokreću svaki servis, vode računa o redosledu njihovog podizanja, podešavaju mrežnu komunikaciju između servisa i obezbede da svi delovi sistema koriste iste konfiguracije. Ovakav pristup otežava razvoj, povećava mogućnost nekonzistentnih okruženja i usporava proces testiranja i debagovanja. Sve ovo yahteva jako puno vremena kao i dobro poznavanje svih delove sistema koji su često jako zamrseni. Alternativno rešenje je da svi programeri razvijaju na zajednickom okruženju što dovodi do otežavanja razvoja jer ne možemo sa sigurnošću da povežemo izmene koje smo napravili sa rezultatom, kao i česte kvarove jer veiki broj ljudi u isto vreme menja okruženje.


## Ključne karakteristike Docker Compose-a

Docker Compose je razvijen kako bi rešio upravo ove probleme. Njegova osnovna ideja je da omogući centralizovano i deklarativno definisanje cele aplikacije u jednom fajlu  `docker-compose.yml`. Na taj način, svi servisi, njihove zavisnosti, mreže i volumeni postaju deo jedinstvene konfiguracije koja se može jednostavno pokrenuti na svom lokalnom računaru ili zaustaviti pomoću nekoliko komandi.

Korišćenjem Docker Compose-a, redosled pokretanja servisa može se jasno definisati, a komunikacija između kontejnera postaje transparentna zahvaljujući automatskom umrežavanju. Pored toga, ovakav pristup obezbeđuje ponovljivost okruženja, što znači da se ista aplikacija može na isti način pokrenuti na različitim računarima bez dodatnih manuelnih podešavanja. Time Docker Compose značajno pojednostavljuje lokalni razvoj, testiranje i demonstraciju kompleksnih sistema koji se sastoje od više kontejnera.
---

## Tutorijal – Pokretanje projekta

### Potrebne tehnologije

Za pokretanje projekta potrebno je imati instalirano:

- Docker
- Docker Compose (dolazi uz Docker Desktop)

Instalacija se može izvršiti putem:
- https://www.docker.com/products/docker-desktop/

Provera instalacije
U terminalu izvršite sledeće komande
```bash
docker --version
docker compose version
```

<img width="1000" height="119" alt="image" src="https://github.com/user-attachments/assets/f8557431-4582-4c08-bcec-f829523bab8b" />



### Arhitektura projekta

 ```
project-root/
├── backend/
│   ├── app.py
│   ├── wait_for_db.py
│   └── Dockerfile
├── db/
│   └── init/
│       └── 01_init.sql
├── docker-compose.yml
└── README.md
```

Projekat se sastoji od sledećih servisa:

### db
PostgreSQL baza podataka
Automatski se inicijalizuje SQL skriptom pri prvom pokretanju (01_init.sql)

### backend
Backend servis (Python + Flask)
Servis sa izloženim REST API endpointi koji se konektuje na PG bazu i prikayuje informacije odatle 

Servisi su povezani putem interne Docker mreže i upravljaju se docker-compose.yml fajlom.

### Pokretanje projekta
1. Otvoriti terminal u folderu gde se nalazi projekat 
2. Pokrenite komandu:

```
docker compose up --build
```
Kao rezultat dobijate :
<img width="1919" height="552" alt="image" src="https://github.com/user-attachments/assets/52984f70-2980-4d27-9a20-afd822114726" />

Pozovite neki od sledecih endpointa:
  http://localhost:5000, 
  http://localhost:5000/db,
  http://localhost:5000/users

<img width="775" height="433" alt="image" src="https://github.com/user-attachments/assets/8d4498e5-e576-4000-a18c-6487962fcdf2" />

Kontejnere stopiramo komandom
```
 ctrl + C
```
Brisane kontejnera radimo komandom
```
docker compose down -v
```
Ovo raimo kada pravimo izmene u kodu koje želimo da vidimo kada kontejenere

<img width="1090" height="407" alt="image" src="https://github.com/user-attachments/assets/c435bbf7-8441-47f7-bc27-1a6900c8e1cb" />


### Redosled podizanja kontejnera
U mikroservisnoj arhitekturi bitno je da znamo koji servisi imaju međusobne zavisnosti kao i kakvog su tipa, zbog toga dešavaju se situacije gde nam je bitno da odredimo redosled kojim se servisi podižu.
Zavisnost između servisa se diktira sa `depends on:` u servisu koji zavisi od toga da je neki drugi podignut pre njega
```
  backend:
  ...
    depends_on:
      db:
        condition: service_healthy

```
Preporuka je da probate da obrisete taj deo i pokrenete build kontejnera tada ce servis wait_for_db prvo da ispisuje pouke kako pokusava da se konektuje na bazu ali bez uspeha dok se demo_db kontejner ne podigne.
Međutim, važno je razumeti ograničenje ove opcije `depends_on` ne čeka da servis postane spreman za rad – on samo osigurava da će Docker pokušati da pokrene kontejnere u određenom redosledu. To znači da backend kontejner može biti podignut čak i ako PostgreSQL baza još nije spremna za konekcije. Zato je potrebna dodatna provera pre konektovanja koju radimo u `wait_for_db`.

To može da se isproba tako što promenite sifru ili username za konekciju na bazu dok je depends_on opcija ukjucena i u nekom trenutku demo_backend će ispisvati poruku `demo_backend  | Waiting for PostgreSQL...` dok demo_db salje gresku `FATAL:  password authentication failed for user "demo_user"` 

### Korisne docker komande
| Komanda                              | Šta radi                                |
| ------------------------------------ | --------------------------------------- |
| `docker compose up --build`          | Build i start servisa, prikazuje logove |
| `docker compose down -v`             | Zaustavlja servise i briše volumene     |
| `docker compose stop`                | Zaustavlja servise, volumeni ostaju     |
| `docker compose start`               | Pokreće prethodno zaustavljene servise  |
| `docker compose restart`             | Restartuje servise                      |
| `docker compose ps`                  | Prikazuje status svih servisa           |
| `docker compose logs -f`             | Real-time logovi servisa                |
| `docker compose exec <service> bash` | Ulazak u kontejner za debug ili komande |
| `docker compose build`               | Build Docker image servisa              |
| `docker compose run <service> <cmd>` | Privremeno pokretanje komande u servisu |
| `docker compose top`                 | Prikazuje procese unutar kontejnera     |
| `docker compose version`             | Prikazuje verziju Docker Compose alata  |





