import redis

r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)

def addtoCat(categorie, articleId):
    '''
    Ajoute un article d'identifiant numérique spécifié à une catégorie.
    '''
    articleKey = 'articles:' + str(articleId)
    catKey = 'categorie:' + str(categorie)
    r.sadd(catKey, articleKey)

def removefromCat(categorie, articleId):
    '''
    Enlève un article d'identifiant numérique spécifié d'une catégorie.
    '''
    articleKey = 'articles:' + str(articleId)
    catKey = 'categorie:' + str(categorie)
    r.srem(catKey, articleKey)

def getCategorie(categorieName):
    '''
    Retourne tous les membres d'une catégorie d'articles.
    '''
    catKey = 'categorie:' + str(categorieName)
    return r.smembers(catKey)

def scoreCategorie(categorieName):
    '''
    Crée un ensemble qui contient tous les articles d'une catégories
    ainsi que leurs scores.
    '''
    for articleKey in getCategorie(categorieName):
        # Chercher le score dans le sorted set 'score' pour l'article correspondant
        articleScore = r.zscore('score', articleKey)
        # Copier le couple score + clé dans le sous ensemble catégorie
        r.zadd(f"score:{categorieName}", mapping={articleKey : articleScore})
    return r.zrange(f'score:{categorieName}', 0, -1, withscores=True, desc=True)

