from flask import Response
import json

from models.model import News, Articles

class NewsResult:
    def __init__(self):
        pass

    def execute(self):
        articles = Articles.query.all()
        articles_response = []
        for article in articles:
            articles_response.append({
                'title':article.title,
                'date':article.date.strftime('%d/%m/%Y'),
                'link':article.link
            })
        news = News.query.all()
        news_response = []
        for new in news:
            news_response.append({
                'title':new.title,
                'date':new.date.strftime('%d/%m/%Y'),
                'description':new.description
            })
        return Response(response=json.dumps({'articles':articles_response, 'news': news_response}), status=200, mimetype='application/json')