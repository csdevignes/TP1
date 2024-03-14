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
### Alimentation de la base
Pour alimenter la base de données, j'ai créé 2 fichiers .csv contenant la liste des articles à insérer et la liste des votes à enregistrer (générés aléatoirement).

## Question n°2
Il est demandé de créer une méthode permettant de gérer les structures qui stockent l'ordre de publication des articles (timeline) et les scores (score). On utilise un sorted set dans les 2 cas, et on crée une méthode qui permet de récupérer les valeurs de ces deux set en spécifiant le paramètre 'time' ou 'score'.

### Création de la timeline
Le sorted set 'timeline' sera alimenté à chaque création d'article, le timestamp n'étant pas censé être modifié. On crée pour cela simplement une méthode qui stocke la clé et le timestamp d'un article en cours de création dans un sorted set 'time'.

### Système de vote
Afin de garder la trace des utilisateurs ayant voté pour un article et d'éviter les votes multiples, on crée une structure de type set par article, qui contient l'ensemble des utilisateurs ayant voté pour cet article (clé votes:articleId)

Le set est créé lors de la création de l'article, avec une durée de vie d'une semaine. Il est également initialisé avec le vote de l'auteur (qui vote pour son propre article).

### Méthode permettant d'augmenter le nombre de vote d'un article
Ensuite, on crée une méthode qui permet d'enregistrer les votes des utilisateurs en : 
* vérifiant qu'ils n'ont pas déjà voté pour l'article (présence dans le set des votants)
* ajoutant leur identifiant au set votes:articleId
* incrémentant le nombre de votes enregistré dans l'article de 1
* incrémentant le score enregistré pour l'article de 197 par vote

### Récupération de la liste de tous les articles

On crée une méthode qui récupère la liste de tous les articles de la base, en utilisant la fonction de scan de redis. On itère cette fonction jusqu'a récupérer un curseur de zero, qui garantit que la fonction scan a trouvé toutes les clés commmencant par "articles:".

### Top 10 des articles avec le meilleur score
La structure de sorted set est ordonnée, il suffit donc de récupérer les valeurs du set 'score' par ordre décroissant, et de sélectionner les 10 premiers élements pour obtenir le top10 des articles.

## Question n°3 : bonus
Ajout de la gestion des catégories. Les fonctions concernées sont décrite dans un nouveau fichier
`categorie.py`

### Gestion des catégories
Il faut ajouter une information qui permette de savoir a quelle catégorie appartient un article.
Pour cela, on propose de créer un set categorie:nomcategorie par catégorie, et d'y inclure les articles.

L'ajout d'un article à une catégorie se fera indépendemment de la création de l'article dans la
base.