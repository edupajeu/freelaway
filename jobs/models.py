from django.db import models
from django.contrib.auth.models import User


class References(models.Model):  # CREATE A TABLE FOR FILES UPLOADED
    file = models.FileField(upload_to='references')

    def __str__(self) -> str:  # STR APPLY A TIDY URL
        return self.file.url


class Jobs(models.Model):  # CREATE A JOBS TABLE WITH YOURS OWN ALL COLUMNS
    # THESE VARIABLES ARE TABLES COLUMNS
    category_choices = (('D', 'Design'),
                        ('VE', 'Video Editing'))

    status_choices = (('C', 'Creating'),
                      ('WA', 'Waiting Approval'),
                      ('F', 'Finished'))
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=category_choices, default="D")
    delivery_time = models.DateTimeField()
    price = models.FloatField()
    references = models.ManyToManyField(References)
    professional = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    private = models.BooleanField(default=False)
    status = models.CharField(max_length=2, default='WA')

    def __str__(self) -> str:
        return self.title
