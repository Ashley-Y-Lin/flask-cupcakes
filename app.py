from flask import Flask, jsonify, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

# from forms import NewSongForPlaylistForm, AddSongForm, AddPlaylistForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

"""Flask app for Cupcakes"""


@app.get("/api/cupcakes")
def show_all_cupcakes():
    """Return data about all the cupcakes.

    Returns JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_one_cupcake(cupcake_id):
    """Return data about a single cupcake.

    Returns JSON Return JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize())


# add validation to cupcakes in WTForms
# until then, be explicit about precise keys to extract from data


@app.post("/api/cupcakes")
def create_one_cupcake():
    """Adds a new cupcake to the database, and returns data about a single cupcake.

    Returns JSON Return JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image_url=image_url)

    # data = {k: v or None for k, v in request.json.items()}
    # new_cupcake = Cupcake(**data)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


# FIXME: FIX
@app.post("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """updates the tag with the given id
    and redirects to the tag list page"""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["tag_name"]

    db.session.add(tag)
    db.session.commit()

    flash("Tag updated!")

    return redirect(f"/tags")
