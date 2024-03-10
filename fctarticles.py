import redis
import time
from datetime import timedelta
import random

r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)

def saveArticle(titre, url, user):
    '''
    La méthode défini un articleId, un timestamp correspondant à l'instant actuel
    et écrit les données dans redis pour la clé "articles:articleId".
    Elle crée et alimente également le sorted set contenant la timeline des articles,
    en appelant storeIdTimestamp.
    Enfin, elle crée le set qui contiendra la liste des utilisateurs ayant voté pour un article,
    de clé "votes:articleId", et de durée de vie d'une semaine.
    Ce set, ainsi que le nombre de votes est initialisé avec le vote du créateur de l'article.
    '''
    # On crée une autre structure clé/valeur qu'on incrémente à chaque création d'article
    articleId = r.incr('nbArticle') 
    now = int(round(time.time()))
    articleKey = 'articles:' + str(articleId)
    data = {'timestamp': now, 'titre': titre, 'url': url, 'user': user, 'votes':'0'}
    r.hset(articleKey, mapping=data)
    storeIdTimestamp(articleKey, now)
    # Création du set votes:articleId, ajout du vote du créateur.
    setname = "votes:" + str(articleId)
    r.sadd(setname, user)
    r.expire(setname, timedelta(days=7))
    incrVote(articleId)

def storeIdTimestamp(articleKey, now):
    '''
    A la création d'un article, stocke son identifiant et son timestamp dans un sorted
    set de clé 'time'.
    '''
    r.zadd('time', mapping={articleKey : now})

def getArticle(articleId):
    '''
    Renvoie l'ensemble du hash stocké à la clé "articles:articleId".
    '''
    articleKey = 'articles:' + str(articleId)
    return r.hgetall(articleKey)

def getTimeline():
    '''
    Renvoie la timeline des articles stockée dans le sorted set 'time'
    Du plus ancien au plus récent
    '''
    return r.zrange('time', 0, -1, withscores=True, desc=False)

def incrVote(articleId):
    '''
    Récupère la clé de l'article et augmente le nombre de votes de 197.
    '''
    articleKey = 'articles:' + str(articleId)
    r.hincrby(articleKey, 'votes', 197)

def makeVote(userId, articleId):
    '''
    Lorsqu'on enregistre le vote d'un utilisateur pour un article :
    - augmente le nombre de votes de l'article
    - enregistre l'identifiant de l'utilisateur dans le set des votants de l'article
    Sous condition que l'utilisateur n'ai pas déjà voté pour cet article.
    '''
    if str(userId) in listVoters(articleId):
        print(f"L'utilisateur {userId} a déjà voté pour l'article {articleId}")
    else:
        incrVote(articleId)
        setname = "votes:" + str(articleId)
        r.sadd(setname, userId)


def listVoters(articleId):
    '''
    Méthode qui permet de connaitre pour un article donné, la liste des utilisateurs qui
    ont voté pour cet article.
    '''
    setname = "votes:" + str(articleId)    
    return r.smembers(setname)

def appendScoreSet(articleKey):
    '''
    Récupère le score de votes d'un article, puis le stocke avec son identifiant dans un
    sorted set de clé 'score'.
    '''
    score = r.hget(articleKey, 'votes')
    r.zadd('score', mapping={articleKey : score})

def listArticles():
    '''
    Scanne la base de données pour trouver toutes les clés qui commencent par 'articles:'.
    Renvoie la liste des clés des articles.
    La fonction SCAN de redis renvoie un curseur à chaque itération. Tant que le curseur
    renvoyé n'est pas 0, on a aucune garantie d'avoir obtenu l'ensemble des résultats.
    On stocke donc les résultats du scan dans un set d'article à chaque itération.
    La fonction SCAN peut renvoyer des doublons, d'ou l'utilisation d'un set Python.
    '''
    cursor = 0
    scan = [1]
    setArticles = set()
    while scan[0] != 0:
        scan = r.scan(cursor, match= "articles:*")
        cursor = scan[0]
        setArticles.update(scan[1])
    return setArticles

def makeScoreSet():
    '''
    Crée un sorted set contenant tous les articles de la base et leur nombre de votes
    '''
    for articleKey in listArticles():
        appendScoreSet(articleKey)
    return r.zrange('score', 0, -1, withscores=True, desc=True)

def top10():
    return makeScoreSet()[0:10]
