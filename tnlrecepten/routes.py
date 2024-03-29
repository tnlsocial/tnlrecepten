#!/usr/bin/env python3

from flask import current_app as app
from flask import render_template, abort, request, redirect, flash, url_for, send_from_directory, session
from datetime import datetime

from .models import Recepten
from .forms import ReceptForm
from . import db

import secrets, os, markdown, json, bleach


@app.route("/", methods=["GET"])
def index():
    recepten = Recepten.query.all()
    recepten_tags = Recepten.query.filter(Recepten.tags.isnot(None)).all()

    tags = []
    for recept in recepten_tags:
        recept_tag = json.loads(recept.tags)

        for tag in recept_tag:
            tags.append(tag)

    tags = list(set(tags))

    return render_template("index.html",
                            tags=tags,
                            recepten=recepten)

@app.route("/recept/<token>", methods=["GET"])
def recept(token):
    recept = Recepten.query.filter_by(token=token).first_or_404()

    allowed_tags = ['tbody', 'th', 'img', 'ins', 'mark', 'sup', 'dl', 'p', 'br', 'abbr', 'hr', 'strong', 'ul', 'li', 'ol', 'pre', 'code', 'thead', 'table', 'td', 'tr', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'em', 'blockquote', 'dt', 'dd', 'div']
    allowed_attr = { '*': ['class'],
                    'a': ['href', 'rel'],
                    'img': ['src', 'alt', 'width', 'height'],

}
    if recept:
        #recept.recept = markdown.markdown(recept.recept, extensions=['extra', 'tables', 'nl2br'])
        recept.recept = bleach.clean(markdown.markdown(recept.recept, extensions=['extra', 'tables', 'nl2br']), tags=allowed_tags, attributes=allowed_attr)
    
    recept_tags = {}
    for item in json.loads(recept.tags):
        search = Recepten.query.filter(Recepten.tags.ilike("%" + str(item) + "%")).all()

        for row in search:
            if (row.titel, row.token) in recept_tags:
                recept_tags[row.titel, row.token].append(item)
            else:
                if row.id is not recept.id:
                    recept_tags[row.titel, row.token] = [item]

    return render_template("recept.html",
                            recept=recept,
                            recept_tags=recept_tags)

@app.route("/tags/<tag>", methods=["GET"])
def tags(tag):
    recepten = Recepten.query.filter(Recepten.tags.contains(tag)).all()
    recepten_tags = Recepten.query.filter(Recepten.tags.isnot(None)).all()

    tags = []
    for recept in recepten_tags:
        recept_tag = json.loads(recept.tags)

        for tag in recept_tag:
            tags.append(tag)

    tags = list(set(tags))

    return render_template("index.html",
                            recepten=recepten,
                            tags=tags)                            


@app.route("/toevoegen", methods=["GET", "POST"])
def toevoegen():
    form = ReceptForm()
    
    if form.validate_on_submit():
        nickname = form.nickname.data
        titel = form.titel.data
        recept = form.recept.data
        tags = json.dumps(form.tags.data)
        
        token = str(secrets.token_urlsafe(8))

        try:
            new_recept = Recepten(nickname=nickname,
                        titel=titel,
                        recept=recept,
                        token=token,
                        tags=tags,
                        time_created=datetime.now()
                        )
            db.session.add(new_recept)
            db.session.commit()
            flash("Dank! je recept is toegevoegd", "success")
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            abort(400)

    return render_template("form.html",
                            form=form)


@app.route("/aanpassen/<token>", methods=["GET", "POST"])
def aanpassen(token=None):
    delete = request.args.get('delete', False)

    form = ReceptForm()

    recept = Recepten.query.filter_by(token=token).first_or_404()

    form.nickname.data = recept.nickname

    if recept.tags:
        recept_tags = ', '.join(json.loads(recept.tags))
    else:
        recept_tags = ''

    if form.validate_on_submit():
        recept.titel = form.titel.data
        recept.recept = form.recept.data
        if form.tags.data:
            recept.tags = json.dumps(form.tags.data)
        recept.last_edit = datetime.now()
        
        try:
            db.session.commit()
            flash("Het recept is aangepast!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            abort(400)

    if delete:
        try:
            Recepten.query.filter_by(token=recept.token).delete()
            db.session.commit()
            flash("Het recept is verwijderd!", "success")
            return redirect(url_for('index'))
        except:
            print(e)
            abort(400)                    


    return render_template("form.html",
                            recept=recept,
                            recept_tags=recept_tags,
                            form=form)


@app.errorhandler(404)
def page_not_found(e):
    flash(e, 'info')
    return redirect(url_for('index'))

@app.errorhandler(400)
def page_not_found(e):
    flash(e, 'info')
    return redirect(url_for('index'))    


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/recepten.db') 
def recepten_db():   
    return send_from_directory(os.path.join(app.root_path, 'db'), 'recepten.db')
