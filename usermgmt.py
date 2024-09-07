import sys
from passlib.hash import argon2
from getpass import getpass


def hashZastita(string) :
   return argon2.hash(string)

def passwordCheck(lozinka) :
    if len(lozinka) <= 7:
      return False
    
    imaMaloSlovo = False
    imaVelikoSlovo = False
    imaSpecijalniZnak = False
    imaBroj = False

    skupSpecijalnihZnakova = "!?=,._-#$%&"

    for znak in lozinka :
      if znak.islower():
        imaMaloSlovo = True
      if znak.isupper():
        imaVelikoSlovo = True
      if znak.isdigit():
        imaBroj = True
      if znak in skupSpecijalnihZnakova:
        imaSpecijalniZnak = True
    return imaVelikoSlovo and imaMaloSlovo and imaSpecijalniZnak and imaBroj

def addUser(korisnickoIme, password, datoteka):
    hashedPassword = hashZastita(password)
    forceChange = False
    try :
      with open(datoteka, "r") as file :
        for line in file :
          uzmiIme, uzmiHashedPassword, citajForce = line.strip().split(":")

          if uzmiIme == korisnickoIme :
            return False, None, None, False
    except FileNotFoundError :
      pass
    return True, korisnickoIme, hashedPassword, forceChange

argumenti = sys.argv


for argument in argumenti :
  if argument == "add":
    korisnickoIme = sys.argv[2]
    datoteka = "datoteka.txt"
    password = getpass("Lozinka: ")
    repeatPassword = getpass("Ponovite lozinku: ")

    if  not password != repeatPassword:
      if passwordCheck(password) :
        jeliProslo, korisnickoImeAdd, hashedPassword, forceChange = addUser(korisnickoIme, password, datoteka)
        if not jeliProslo:
          print("User add failed. User may already exist.")
        else :
          with open(datoteka, "a") as file :
            file.write(f"{korisnickoImeAdd}:{hashedPassword}:{forceChange}\n")
          print(f"User {korisnickoIme} successfuly added.")

      else :
        print("Passwords must contain at least 8 characters, including uppercase and lowercase letters, a number, and a special character.")

    else :
      print("User add failed. Password mismatch.")

  if argument == "passwrd":
      korisnickoIme = sys.argv[2]
      datoteka = "datoteka.txt"
      password = getpass("Lozinka: ")
      repeatPassword = getpass("Ponovite lozinku: ")

      if not password != repeatPassword:
        if passwordCheck(password):
          with open(datoteka, "r") as file :
            procitaj = file.readlines()
          sacuvajListu = []
          pronadjen = False
          for line in procitaj :
             uzmiIme, uzmiHashedPassword,citajForce = line.split(":")
             if uzmiIme == korisnickoIme:
                pronadjen = True
                hashedNoviPassword = hashZastita(password)
                sacuvajListu.append(f"{korisnickoIme}:{hashedNoviPassword}:{citajForce}")
             else :
                sacuvajListu.append(line)
          if not pronadjen :
             with open(datoteka, "w") as file :
                for line in sacuvajListu :
                   file.write(line)
             print("Password change failed. Password mismatch.")
          else :
              with open(datoteka, "w") as file :
                for line in sacuvajListu :
                   file.write(line)
              print("Password change successful.")

        else :
          print("Passwords must contain at least 8 characters, including uppercase and lowercase letters, a number, and a special character.") 
      else :
        print("User add failed. Password mismatch.")
  if argument == "del" :
      korisnickoIme = sys.argv[2]
      datoteka = "datoteka.txt"
      sacuvajListu = []
      pronadjen = False
      with open(datoteka, "r") as file :
        procitaj = file.readlines()
      for line in procitaj :
         uzmiIme, uzmiHashedPassword, citajForce = line.split(":")
         if uzmiIme == korisnickoIme :
            pronadjen = True
         else :
            sacuvajListu.append(line)
      if not pronadjen :
        with open(datoteka, "w") as file :
          for line in sacuvajListu :
            file.write(line)
        print("User not in database.")
      else :
        with open(datoteka, "w") as file :
          for line in sacuvajListu :
              file.write(line)
        print("User successfuly removed.")
  if argument == "forcepass" :
      korisnickoIme = sys.argv[2]
      datoteka = "datoteka.txt"
      pronadjen = False
      listaSpremanja = []
      with open(datoteka, "r") as file :
         procitaj = file.readlines()
      for line in procitaj :
         uzmiIme, uzmiHashedPassword, uzmiForce = line.strip().split(":")
         if uzmiIme == korisnickoIme :
            pronadjen = True
            uzmiForce = True
            listaSpremanja.append(f"{uzmiIme}:{uzmiHashedPassword}:{uzmiForce}\n")
         else :
            listaSpremanja.append(line)
      if not pronadjen :
        with open(datoteka, "w") as file :
          for line in listaSpremanja :
              file.write(line)
        print("User not in database.")
      else :
        with open(datoteka, "w") as file :
          for line in listaSpremanja :
            file.write(line)
        print("User will be requested to change password on next login.")
      