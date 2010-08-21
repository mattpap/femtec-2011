import os

from django.db import models
from django.contrib.auth.models import User

from femtec.settings import ABSTRACTS_PATH

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    affiliation = models.CharField(max_length=100)

    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    speaker = models.BooleanField()
    student = models.BooleanField()

    accompanying = models.IntegerField()
    vegeterian = models.BooleanField()

    arrival = models.DateField()
    departure = models.DateField()

    postconf = models.BooleanField()
    tshirt = models.CharField(max_length=1)

    def __unicode__(self):
        return u"Profile for %s" % self.user.get_full_name()

class UserAbstract(models.Model):
    user = models.ForeignKey(User)

    title = models.CharField(max_length=200)

    digest_tex = models.CharField(max_length=40)
    digest_pdf = models.CharField(max_length=40)

    size_tex = models.IntegerField()
    size_pdf = models.IntegerField()

    submit_date = models.DateTimeField()
    modify_date = models.DateTimeField()

    accepted = models.NullBooleanField()

    def __unicode__(self):
        return u"Abstract for %s" % self.user.get_full_name()

    def delete(self):
        try:
            os.remove(os.path.join(ABSTRACTS_PATH, self.digest_tex+'.tex'))
            os.remove(os.path.join(ABSTRACTS_PATH, self.digest_tex+'.pdf'))
        except OSError:
            pass # don't care about missing files

        super(UserAbstract, self).delete()

