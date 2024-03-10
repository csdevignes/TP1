from fctarticles import *
import csv
import redis
r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)
r.flushdb(asynchronous=False) # Supprime toutes les clés de la base.
# Besoin d'utiliser asynchronous = False sinon fausse l'incrémentation.

print("Ajout d'un article")
with open("ListeArticles.csv") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for ligne in spamreader :
        saveArticle(ligne[0], ligne[1], ligne[2])

print("Ajout des votes")
with open("ListeVotes.csv") as csvfile2:
     spamreader2 = csv.reader(csvfile2, delimiter=';')
     for ligne in spamreader2 :
         makeVote(ligne[0], ligne[1])


# print("Recuperation d'un article")
# print(getArticle(1))
# print(listVoters(1))

print(top10())
