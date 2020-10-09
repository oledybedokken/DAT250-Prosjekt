### Ting å gjøre og fikse
  * Session problemer
  * Sikkerhet
  * CSS

```
Hjem:

- Rett hovedmeny så den står imidten
- Skap logg system for alt brukeren gjør
- Logoen linker til hovedmeny
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
"Du har ikke nok penger" er ikke tydelig nok.
"Ugyldig sum" er ikke tydelig nok.
"Kontoen må være tom før den kan slettes" ikke tydelig nok.

"Du kan maks nedbetale XXX kr" ikke tydelig, bytt til:
"Du kan ikke overstige gitte summen for nedbetaling."

*Forandring
- Mellomrom på store verdier
- Reduser tallmengde for kontonummer. (start: 10011000)
- Dato skal ikke inneholde mikrosekunder, YY-MM-DD HH-MM-SS
```

### Legg til ting du holder på med
Ole:
    
1. NA
  
Jørgen:

1. NA

Pervaz:

1. NA

Espen:

1. NA

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
