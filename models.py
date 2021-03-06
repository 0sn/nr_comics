from django.db import models, connection, transaction
from django.template.defaultfilters import slugify
import datetime, os

Contribution = models.get_model('nr_contributions', 'contribution')

import datetime, os

class ComicsManager(models.Manager):
    def public(self):
        return self.filter(**{'date__lte': datetime.datetime.now()})
    
    def future(self):
        return self.filter(**{'date__gt': datetime.datetime.now()})
    
    def by_year(self):
        years = self.public().dates('date','year')
        comics = []
        for year in years:
            y = {"year": year, "months": []}
            for month in self.public().filter(date__year=year.year).dates('date','month'):
                y["months"].append({"month": month, "comics": self.public().filter(date__year=year.year, date__month=month.month)})
            comics.append(y)
        return comics

def upload_to(instance, filename):
    return "comics/%s-%s%s" % (str(instance.date), slugify(instance.title), os.path.splitext(filename)[1])

class Comic(models.Model):
    comics = ComicsManager()
    date = models.DateField(unique=True)
    sequence = models.IntegerField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=100)
    transcript = models.TextField()
    newstitle = models.CharField(max_length=100, verbose_name="news title")
    news = models.TextField()
    comic = models.ImageField(upload_to=upload_to, height_field="height", width_field="width")
    height = models.IntegerField(blank=True, null=True, editable=False)
    width = models.IntegerField(blank=True, null=True, editable=False)
    origin = models.ManyToManyField(Contribution, limit_choices_to={'flagged': True}, null=True, blank=True)

    class Meta:
        ordering = ('sequence',)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.date)
    
    @models.permalink
    def get_absolute_url(self):
        return ("nr_comics.views.comic", [self.sequence])

    def is_public(self):
        """
        True if the date on the comic is in the past, or today.
        """
        return self.date <= datetime.date.today()
    is_public.boolean = True
    
    @classmethod
    def first(self):
        return 1
    
    def previous(self):
        return self.sequence - 1
    
    @classmethod
    def last(self):
        return Comic.comics.public().count()
    
    def next(self):
        return self.sequence + 1

def update_comic_sequence(sender, instance, **kwargs):
    """
    After a save, or a delete, updates the sequence of all comics by date.
    Not in save() in the Comics model because it affects all Comics.
    """
    query = "UPDATE nr_comics_comic SET sequence=(select count(*) from nr_comics_comic where nr_comics_comic.date <= %s) WHERE id=%s"
    cursor = connection.cursor()
    for comic in Comic.comics.all():
        cursor.execute(query,[comic.date, comic.id])
    transaction.commit()

models.signals.post_save.connect(update_comic_sequence,sender=Comic)
models.signals.post_delete.connect(update_comic_sequence,sender=Comic)
