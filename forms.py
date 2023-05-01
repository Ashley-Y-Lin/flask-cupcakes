"""Forms for cupcakes."""

from wtforms import SelectField, StringField, TextAreaField, IntegerField
from flask_wtf import FlaskForm

from wtforms.validators import Optional, InputRequired, Length, URL


class AddNewCupcakeForm(FlaskForm):
    """Form for adding a new cupcake."""

    flavor = StringField("Flavor", validators=[InputRequired(), Length(max=50)])

    size = TextAreaField("Size", validators=[InputRequired(), Length(max=15)])

    rating = IntegerField("Rating", validators=[InputRequired()])

    image_url = StringField(
        "Image URL",
        validators=[
            InputRequired(),
            URL(require_tld=False, message="Please enter a valid URL"),
        ],
    )
