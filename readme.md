# TP Big Data n°1
# Architectures Big Data
## Mars 2024 - Claire-Sophie Devignes

# Set-up
Lancer docker :
`docker run --name myredis -p 6379:6379 -it --rm redis:7.2.4`

Accéder à la base redis :
`docker exec -it myredis redis-cli --raw`

## Question n°1
Construire une base redis qui gère une fonction de vote sur les articles ou
les commentaires.
### Question 1.a: Quelle structure de Redis est la plus appropriée ?
Pour stocker les articles, une structure de hash parait être la
plus appropriée. Exemple:
* Clé: articles:72
* Valeur de type hash:
    * titre: Redis pour les nuls
    * timestamp: 1380886601
    * lien: http://www.foo.org/articles/1
    * utilisateur: utilisateurs:23
    * votes: 14

Pour gérer les identifiant d'article, on crée aussi une entrée simple:
* Clé: 'nbArticle'
* Valeur: 1 (incrémentée par la fonction saveArticle)
### Question 1.b: Quelles structures pour accéder aux articles de facon séquentielle ?
On utilisera plutôt une structure de sorted set, qui va associer à l'id de l'article:
* le timestamp pour la timeline
* ou le score

Structure:
* Clé: time
* Valeur de type sorted set:
    * article:3  394
    * article:6  985
### Question 1.c: Quelle structure pour connaître les utilisateurs ayant voté pour un article ?
Un set pour éviter qu'un utilisateur vote plusieurs fois pour un article. Structure:
* Clé: votes:3 (identifiant de l'article)
* Valeur de type set: utilisateurs:23, utilisateurs:57

## Question n°2
Il est demandé de créer une méthode permettant de gérer les structures qui stockent l'ordre de publication des articles (timeline) et les scores (score).

### Gestion de la timeline
Le sorted set 'timeline' sera alimenté à chaque création d'article, le timestamp n'étant pas censé être modifié. On crée pour cela simplement une méthode qui stocke la clé et le timestamp d'un article en cours de création dans un sorted set 'time'. On crée également la méthode qui permet de récupérer ce set de timeline.

### Système de vote
Afin de garder la trace des utilisateurs ayant voté pour un article et d'éviter les votes multiples, on crée une structure de type set par article, qui contient l'ensemble des utilisateurs ayant voté pour cet article (clé votes:articleId)

Le set est créé lors de la création de l'article, avec une durée de vie d'une semaine. Il est également initialisé avec le vote de l'auteur (qui vote pour son propre article).

Ensuite, on crée une méthode qui permet d'enregistrer les votes des utilisateurs en : 
* vérifiant qu'ils n'ont pas déjà voté pour l'article
* ajoutant leur identifiant au set votes:articleId
* incrémentant le score de votes enregistré pour l'article de 197 par vote

### Gestion des scores
Le sorted set 'score' sera généré sur demande, en effet le score de votes d'un article n'est pas stable dans le temps.

Pour cela, on crée une méthode qui récupère la liste de tous les articles de la base, en utilisant la fonction de scan de redis. On itère ensuite dans cette liste, en récupérant à chaque fois la clé de l'article et le score associé.

La structure de sorted set est ordonnée, il suffit donc d'inverser son ordre (score décroissant) et de sélectionner les 10 premiers élements pour obtenir le top10 des articles.
