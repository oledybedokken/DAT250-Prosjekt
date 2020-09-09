# DAT250-Prosjekt

*WORK IN PROGRESS*

Registrering:
- Fornavn, etternavn, fødselsdato, addresse, telefon-nr (frivillig)
- Passord, e-mail

*Passord krav:
- Minimum 8 
- Stor bokstav
- Liten bokstav
- Minimum 1 ASCII-symbol

*Etter registrering:
- Sendes e-mail at man har registrert hos [nettbank] osv..
- Sendes e-mail om authentication-code (random gen 5 tall)

*Authentication-Code
- Bare tall | 5 tall

Innlogging:
- Fler-fase;
- E-mail & Passord -> Authentication-Code

*Sikkerhet:
@ Passord:
- Skriv feil kode/passord 5 ganger, da blir kontoen sperret, man får e-mail for ny kode.
- Kan gjøres bare en gang - om kontoen blir sperret for andre gang før brukeren har fått tilgang, 
	da blir den permanent sperret. Kontoen kan bli åpnet, men bare av Admin (Admin login/SQL).
- Får melding på nettsiden "Du har {antall_gjentagelser} igjen".

@ Nettisde:
- Automatisk avlogging etter x minutt av inaktivitet
- Fjerner potensiell 'sikkerhetsshull' for å minske tilgang.
- Legge til reCaptcha for at roboter ikke skal kunne logge inn på siden

@ Admin loggin:
- Spesiell kode for Admin, eks. Admin authentication-code eller ha en 'whitelisted' MAC-addresse.

Admin: (om det trengs)
- Login for Admin
- Glemt passord for Admin
- Edit profil for Admin
- Logg-out funksjon
- Dashbord for Admin

Brukere:
- Legg til ny konto
- Rediger eksisterende konto (navn, slett...)
- Detaljer om transaksjon (hovedmeny - under eksisterende-konto)
- Bytt valuta 

Transaksjon administrasjon:
- Avsende transaksjon (Error om den ikke finnes i databasen)
- Send over eFaktura
- Logg over alt transaksjon

Bruker:
- HTML: Sideoppsett
- CSS: Design
- Python: Valideringsoppgaver
- MySQL: Database
- Server? - Trengs nett, trengs server.

TEST test test
