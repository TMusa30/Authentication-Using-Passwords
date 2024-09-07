import sys
from getpass import getpass
import subprocess
from passlib.hash import argon2


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


def hashZastita(string) :
   return argon2.hash(string)

def loginUsera(datoteka, korisnickoIme) :
  listaSpremanja = []

  with open(datoteka, "r") as file :
    for line in file :
      imeKorisnika, passwordKorisnika, forceChange = line.strip().split(":")
      if imeKorisnika == korisnickoIme :
        if forceChange == "True":
          password = getpass("Password: ")
          if argon2.verify(password, passwordKorisnika):
            novaSifra = getpass("New password: ")
            ponovljenaNovaSifra = getpass("Repeat new password: ")
            if novaSifra == ponovljenaNovaSifra and novaSifra != password :
              if passwordCheck(novaSifra):
                forceChange = "False"
                listaSpremanja.append(f"{imeKorisnika}:{hashZastita(novaSifra)}:{forceChange}\n")
                subprocess.run("wsl /bin/bash", shell=True)
              else :
                print("Passwords must contain at least 8 characters, including uppercase and lowercase letters, a number, and a special character.")
                return False
            else :
              print("Username or password incorrect.")
              return False
          else :
            print("Username or password incorrect.")
            return False
        else :
          password = getpass("Password: ")
          if argon2.verify(password, passwordKorisnika):
              if passwordCheck(password):
                listaSpremanja.append(f"{imeKorisnika}:{passwordKorisnika}:{forceChange}\n")
                subprocess.run("wsl /bin/bash", shell=True)
              else :
                print("Passwords must contain at least 8 characters, including uppercase and lowercase letters, a number, and a special character.")
                return False
          else :
            print("Username or password incorrect.")
            return False
      else :
        listaSpremanja.append(line)
  with open(datoteka, "w") as file:
    for line in listaSpremanja :
      file.write(line)
  return True



argumenti = sys.argv

korisnickoIme = argumenti[1]

ucitanaDobraSifra = False
datoteka = "datoteka.txt"
i = 0
while(True):
  i += 1
  if i > 4 :
    break
  ucitanaDobraSifra = loginUsera(datoteka,korisnickoIme)
  if ucitanaDobraSifra :
    break