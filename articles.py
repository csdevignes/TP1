from fctarticles import *
from categorie import *
import csv
import redis
from pprint import *

r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)
r.flushdb(asynchronous=False) # Supprime toutes les clés de la base.
# Besoin d'utiliser asynchronous = False sinon fausse l'incrémentation.

print("Ajout des articles :")
with open("ListeArticles.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for ligne in spamreader :
        saveArticle(ligne[0], ligne[1], ligne[2])
        print(ligne[0])

print("\nTimeline des articles :")
pprint(getSortedSet('time', desc=False))

print("\nAjout des votes :")
with open("ListeVotes.csv") as csvfile2:
     spamreader2 = csv.reader(csvfile2, delimiter=';')
     for ligne in spamreader2 :
         makeVote(ligne[0], ligne[1])

print("\nListe de tous les articles :")
pprint(listArticles())

print("\nTop 10 des articles :")
pprint(top10())
thebest = top10()[0][0].split(':')[1]
print(f"Le meilleur article est le n°{thebest}")
print(getArticle(thebest))
print(f"Les utilisateurs ayant voté pour l'article {thebest} sont:")
print(listVoters(thebest))

print("\nAjout des catégories.")
with open("ListeCategories.csv") as csvfile3:
     spamreader3 = csv.reader(csvfile3, delimiter=';')
     for ligne in spamreader3 :
         addtoCat(ligne[0], ligne[1])
print("\nArticles dans la catégorie programmation :")
pprint(getCategorie('programmation'))
print("Retrait de l'article 5 de la catégorie programmation :")
removefromCat('programmation', 5)
pprint(getCategorie('programmation'))
print('\nScores des articles de la catégorie Alimentation :')
pprint(scoreCategorie('alimentation'))