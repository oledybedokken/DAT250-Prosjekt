from django import forms
from profil import models

# classe for felt lagring av GenerellInfo
class GenerellInfoForm(forms.Modelform):
    class Metadata:
        models = models.GenerellInfo
        felt = ["fornavn", "etternavn", "email", "fodselsdato", "tlf_nummer"]

class BrukerAdresseForm(forms.ModelForm):
    class MetaData:
        models = models.BrukerAdresse
        felt = ["kommune", "fylke", "addresse", "post"]

# classe for felt lagring av Overforing
class OverforingForm(forms.ModelForm):
    class MetaData:
        models = models.Overforing
        felt = ["auth_code", "input_destinasjon_konto_nummer", "input_mengde_for_overforing"]