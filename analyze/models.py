from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class File(models.Model):
    name        = models.CharField(max_length=1000)
    efile       = models.FileField()
    user        = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    slug        = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while File.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

class ReviewList(models.Model):
    title = models.CharField(max_length=100, default='Review List')
    fileInstance = models.ManyToManyField(File)
    date         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
