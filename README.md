# django-chainable-manager

This project aims to give your managers some chainability.

The goal here is the same of this [another project with the same name](https://github.com/maelstrom/django-chainable-manager), the only difference is the technique used. Unfortunately I didn't found a better name to describe this project.

## How it works

First you define your own manager and decorates using `@chainable_manager`

```python
from django.db import models
from chainable_manager import chainable_manager

@chainable_manager
class BookManager(models.Manager):
    def published(self):
        return self.filter(published=True)
    
    def most_popular(self):
        return self.order_by('-reads')
```

So you can use it in the common way:

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    published = models.BooleanField(default=False)
    reads = models.PositiveIntegerField()
    
    objects = BookManager()
```

```python
Book.objects.published().most_popular()
```

Or using multiple managers:

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    published = models.BooleanField(default=False)
    reads = models.PositiveIntegerField()
    
    objects = BookManager()
    chainable_objects = chainable_manager(BookManager)()
```

```python
Book.chainable_objects.published().most_popular()
```
