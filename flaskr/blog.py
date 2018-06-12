from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required, must_admin
from flaskr.db import get_db
import subprocess

bp = Blueprint('blog', __name__)
@bp.route('/')
def index() :
	db = get_db()
	challenges = db.execute(
		'SELECT c.id, title, body, score'
		' FROM challenge c'
		' ORDER BY id ASC'
	).fetchall()
	return render_template('blog/index.html', challenges=challenges)

@bp.route('/ranking')
def ranking() :
    db = get_db()
    users = db.execute(
		'SELECT u.id, username, score'
		' FROM user u'
		' ORDER BY score DESC'
	).fetchall()
    return render_template('blog/ranking.html', users=users)

@bp.route('/<int:id>/chall', methods=('GET', 'POST'))
@login_required
def view_chall(id):
    challenge = get_post(id)
    return render_template('blog/chall.html', challenge=challenge)

@bp.route('/create', methods=('GET', 'POST'))
@must_admin
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        score = int(request.form['score'])
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO challenge (title, body, score)'
                ' VALUES (?, ?, ?)',
                (title, body, score)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id):
    challenge = get_db().execute(
        'SELECT c.id, title, body, score'
        ' FROM challenge c'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if challenge is None :
        abort(404, "challenge id {0} doesn't exist.".format(id))

    return challenge

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@must_admin
def update(id):
    challenge = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        score = int(request.form['score'])
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE challenge SET title = ?, body = ?, score = ?'
                ' WHERE id = ?',
                (title, body, score, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', challenge=challenge)

@bp.route('/<int:id>/submit', methods=('GET', 'POST'))
@login_required
def submit(id):
    challenge = get_post(id)

    if request.method == 'POST':
        sourcecode = request.form['body']
        username = request.form['username']
        error = None

        if not sourcecode:
            error = 'Sourcecode is required.'

        if error is not None:
            flash(error)
        else:
            filepath = "./flaskr/files/"
            filename = str(id) + "_" + username
            srcf = open(filepath + "src/" + filename + ".c", 'w')
            srcf.write(sourcecode)
            srcf.close()

            subprocess.call(filepath + "compile.sh " + filename + " " + str(id), shell=True)
            resf = open(filepath + "results/result_" + filename + ".txt", 'r')
            result = resf.readline().strip()
            if (result == "correct"):
                print(str(id) + " has been solved by " + g.user['username'])
                db = get_db();
                alreadySolved = db.execute(
                    'SELECT s.id'
                    ' FROM solved s'
                    ' WHERE s.chall_id = ? AND s.solver_id = ?',
                    (id, g.user['id'])
                ).fetchone()
                # print (alreadySolved)
                if (alreadySolved is None) :
                    # First solved!
                    flash("정답입니다!")
                    db.execute(
                        'INSERT INTO solved (solver_id, chall_id)'
                        ' VALUES (?, ?)',
                        (g.user['id'], id,)
                    )
                    chall = db.execute(
                        'SELECT score'
                        ' FROM challenge c'
                        ' WHERE c.id = ?',
                        (id,)
                    ).fetchone()
                    newScore = chall['score'] + g.user['score']

                    db.execute(
                        'UPDATE user SET score = ?'
                        ' WHERE id = ?',
                        (newScore, g.user['id'])
                    )
                    print("Gained " + str(chall['score']) + " points. (" + str(newScore) + " points now)")
                    db.commit()
                else :
                    # Already Solved!
                    # do nothing...?
                    flash("이미 푼 문제입니다.")
                    print("Already solved")
            else :
                flash("틀렸습니다. 다시 시도 해 보세요.", 'fail')
            resf.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/submit.html', challenge=challenge)

@bp.route('/<int:id>/delete', methods=('POST',))
@must_admin
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM challenge WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
