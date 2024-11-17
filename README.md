Ovaj projekt se sastoji od dva alata :
  1. usermgmt - Alat za upravljanje korisničkim imenima i lozinkama (dodavanje, izmjena, brisanje, forcepass)
  2. login - Alat za prijavu korisnika u sustav


#Instalacija
  1. Preuzmite datoteke "usermgmt.py" i "login.py"

#Pokretanje

  #USER MANAGEMENT
    1. Pokrenite "usermgmt.py" s komandom: "python usermgmt.py add <korisnicko_ime>"
    2. Promjena lozinke s komandom: "python usermgmt.py passwrd <korisnicko_ime>
    3. Forsiranje promjene lozinke prilikom sljedece prijave korisnika: "python usermgmt.py forcepass <korisnicko_ime>
    4. Brisanje korisnika: "python usermgmt.py del <korisnicko_ime>

  #Login
    1. Prijavite se naredbom: "python login.py <korisnicko_ime>



=> Sve lozinke su spremljene u datoteci i šifrirani. Svaka lozinka mora biti određene kompleksnosti i pri promjeni lozinke ne smije biti jednaka staroj.
