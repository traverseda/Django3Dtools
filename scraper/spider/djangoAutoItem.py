##Like the sandard djangoItem, but with an auto-incrementing "sid" field, and code to map sid's to pk's once the item has been saved.
import itertools
import scrapy
from scrapy.contrib.djangoitem import DjangoItem


SIDcount = itertools.count()
SIDmap = {}

class CountedItem(DjangoItem):
    def __init__(self):
        super(CountedItem, self).__init__()
        self['SID'] = next(SIDcount)
        SIDmap[self['SID']] = {}
    #scrapy ID
    SID = scrapy.Field()
    def save(self):
        project = super(CountedItem, self).save()
        SIDmap[self['SID']]['django_model']=self.django_model
        SIDmap[self['SID']]['pk']=project.pk
        #super(CountedItem, self).save()
	return project
