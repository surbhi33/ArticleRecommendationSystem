# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    ls_path=[]
    for art in articles:
        title=art[1]
        ls_path.append(('/article/'+art[0],title))
        
    template_fill=render_template('articles.html', tup_list=ls_path)
    
    return template_fill


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    for art in articles:
        if art[0]==topic+'/'+filename:
            top_articles=recommended(art, articles, 5)
            title= art[1]
            body= art[2]
            break
    

    ls_path=[]
    for art_new in top_articles:
        t= art_new[1]
        ls_path.append(('/article/'+ art_new[0],t))
    
    return render_template('article.html', title=title, cond=body.split("\n\n"), tup_list=ls_path)

# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)
