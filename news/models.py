from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from utils.markupfield import MarkupTextField
# Create your models here.

class News(models.Model):
	def __init__(self, *args, **kwargs):
		super(News, self).__init__(*args, **kwargs)
		self.content_markup_choices = 'markdown'
    
	author = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	content = MarkupTextField()
	pub_date = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	is_public = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.title
	class Meta:
	    verbose_name_plural = "news"

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'is_public')
