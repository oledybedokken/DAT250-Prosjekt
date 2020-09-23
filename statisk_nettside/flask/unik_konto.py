from functools import wraps

# Sjekker databasen for å se etter email og konto_nummer. 
# Om bruker ikke har konto_nummer/email registrert, skriv nede hva som forehender.


def unik_konto_nummer(a):
    @wraps(a)
    def wrapper(*args):
        for i in range(5):
            konto_nummer = a(*args)
            resultat = bruker.find_one({"bruker.konto_nummer": konto_nummer})
            if not resultat:
                return konto_nummer
        raise Exception("Ingen konto nummer er funnet")
    return wrapper

# Skap unik konto_nummer