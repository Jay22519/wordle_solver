from django.db import models

# Create your models here.


class English_corpus(models.Model) :
    word = models.CharField(max_length  = 200) 

    def __str__(self):
        return self.words
