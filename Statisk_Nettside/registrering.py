class BrukerStyring(BaseBrukerStyring):
    # Fødselsdato skal være DD/MM/ÅR.
    def lag_bruker(self, navn, mail, passord, addresse, kjonn, fodseldato): 
        pass

# Etter lag_bruker er ferdig, drar den til ei ny side der den gir 
# "Du er registrert, din authentication kode er {kode}"-noe lignende. 
# Det sendes over mail i tillegg om registrerings prosessen og authentication kode.
