from django.db import models

# Create your models here.
class NGram(models.Model):
	n = models.IntegerField()
	pickled_ngram = models.FileField(upload_to='ngrams/')

	def __unicode__(self):
		return str(self.n) + "gram"
