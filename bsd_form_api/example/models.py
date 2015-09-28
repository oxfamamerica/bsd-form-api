from django.db import models

class Example(models.Model):
    '''
    An example of a model whose data we will need to send to BSD
    '''
    email = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    saved_on_bsd = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Example"
        verbose_name_plural = "Examples"
        ordering = ("-id",)

