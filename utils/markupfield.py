from django.db.models import CharField, TextField
from django.utils.html import linebreaks

MARKUP_CHOICES = (
	('html', 'Plain HMTL'),
	('plain', 'Plain Text'),
)

try:
	from markdown import markdown
	MARKUP_CHOICES += (('markdown', 'Markdown'),)
except ImportError:
	pass

try:
	from textile import textile
	MAKRUP_CHOICES += (('textile', 'Textile'),)
except ImportError:
	pass

class MarkupTextField(TextField):
	"""
	A TextField taht automatically implements DB-cached makup translation.
	
	Supports: Markdown, Plain HTML, Plain Text, and Textile.
	"""
	def __init__(self, *args, **kwargs):
		super(MarkupTextField, self).__init__(*args, **kwargs)
	
	def contribute_to_class(self, cls, name):
		self._html_field = "%s_html" % name
		self._markup_choices = "%s_markup_choices" % name
		TextField(editable=False, blank=True, null=True).contribute_to_class(cls, self._html_field)
		CharField(choices=MARKUP_CHOICES, max_length=10, blank=True, null=True).contribute_to_class(cls, self._markup_choices)
		super(MarkupTextField, self).contribute_to_class(cls, name)
	
	def pre_save(self, model_instance, add):
		value = getattr(model_instance, self.attname)
		markup = getattr(model_instance, self._markup_choices)
		if markup == 'markdown':
			html = markdown(value)
		elif markup == 'plain':
			html = linebreaks(value, autoescape=True)
		elif markup == 'textile':
			html = textile(value)
		else:
			html = value
		setattr(model_instance, self._html_field, html)
		return value
	
	def __unicode__(self):
		return self.attname