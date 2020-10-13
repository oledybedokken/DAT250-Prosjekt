### Ting å gjøre og fikse
  * ADMIN BRUKER
  * Session problemer
  * Sikkerhet (https://pythonhosted.org/Flask-Security/) og sjekke owasp top 10
  * CSS

```
ADMIN
* Se over alle brukere
* Se over alle konto
* Se over konto til hver bruker
* Redigere alle bruker
* Slette bruker/konto
* Rediger admin info
* Legge til admin bruker
* Global liste med kontonummer for å hinder duplikater?
```
```
Hjem:

- Rett hovedmeny så den står imidten (done)
- Skap logg system for alt brukeren gjør
- Logoen linker til hovedmeny (done)
```
```
Profil:

- Noen av boksene er for kort. Gjør at boksene er under emnet, eks.
Kjønn:
[--------------]

- Ikke inenholde tall: fornavn, etternavn, kjønn, fylke
- Ikke inneholde bokstaver: Postkode
- Ikke inneholde ASCII: alt, (utenom email)

- 'Kontoer' viser bare Brukskonto, ikke sparekonto. Flere brukskonto har den plass til.
- Reduser antall konto som skal vises. Maks 4 brukskonto, maks 4 sparekonto.
```
```
Oversikt:
- Kan skape maks 8 kontoer (bruks- og sparekonto) (ellers problem for profil.html)

*Tenke gjennom
- Logg / Alle kontoer vist under, som i Profil
```
```
Betaling:
- Mellomrom på store verdier
Har tenkt å formatere til string med '.toLocaleString()' eller ''.join - men skapte error.

```

### Legg til ting du holder på med.-
Ole:
    
1. Sortere Admin bruker
  
Jørgen:

1. Sortere transaksjoner riktig (nyeste øverst)           GJORT
2. Mellomrom på store verdier                             GJORT
3. maks en av hver lånetype                               GJORT
4. Fjerne kontonummer for nedbetaling av lån??
5. maksgrense for lån?

Pervaz:

1. Går gjennom sikkerhet og quality control (alt funker)

Espen:

1. CSS
2. Admin bruker(FUNKER)

## For å kjøre flask run

```
export FLASK_APP=project
```
```
set FLASK_APP=project
```
```
set FLASK_DEBUG=1
```
```
flask run
```

### Sikkerhet!!!
  * https://sucuri.net/guides/owasp-top-10-security-vulnerabilities-2020/

Top 10 vulnerabilities som må fikses

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access control
6. Security misconfigurations
7. Cross Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with known vulnerabilities
10. Insufficient logging and monitoring
