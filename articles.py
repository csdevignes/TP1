from fctarticles import *
import csv
import redis
r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)
r.flushdb(asynchronous=False) # Supprime toutes les clés de la base.
# Besoin d'utiliser asynchronous = False sinon fausse l'incrémentation.

print("Ajout des articles :")
with open("ListeArticles.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for ligne in spamreader :
        saveArticle(ligne[0], ligne[1], ligne[2])
        print(ligne[0])

print("Timeline des articles :")
print(getSortedSet('time', desc=False))

print("Ajout des votes :")
with open("ListeVotes.csv") as csvfile2:
     spamreader2 = csv.reader(csvfile2, delimiter=';')
     for ligne in spamreader2 :
         makeVote(ligne[0], ligne[1])

print("Liste de tous les articles :")
print(listArticles())

print("Top 10 des articles :")
print(top10())
thebest = top10()[0][0].split(':')[1]
print(f"Le meilleur article est le n°{thebest}")
print(getArticle(thebest))
print(f"Les utilisateurs ayant voté pour l'article {thebest} sont:")
print(listVoters(thebest))
