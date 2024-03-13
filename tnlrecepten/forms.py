from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from .utils.tag_list_field import TagListField

class ReceptForm(FlaskForm):
    nickname = StringField('Nickname', render_kw={'readonly': True})
    titel = StringField('Titel', validators=[DataRequired()])
    recept = TextAreaField('Recept', validators=[DataRequired()], render_kw={'rows': 20, "placeholder": """Je kunt markdown gebruiken in dit veld, een snelle opfriscursus:
# h1 Heading
## h2 Heading

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~
+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit"""})
    tags = TagListField('Tags', separator=",", render_kw={"placeholder": "Voer hier de hoofdingrediënten toe, gescheiden door een komma"})
    submit = SubmitField('Versturen')