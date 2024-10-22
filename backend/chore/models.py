from io import BytesIO
from PIL import Image

from datetime import timedelta
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(default='')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Chore(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chores')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    score = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    FREQUENCY_OPTIONS = [
        (timedelta(weeks=1), 'once in a week'),
        (timedelta(weeks=2), 'once in 2 weeks'),
        (timedelta(weeks=3), 'once in 3 weeks'),
        (timedelta(weeks=4), 'once in a month'),
        (timedelta(weeks=8), 'once in 2 months'),
        (timedelta(weeks=26), 'once in 6 months'),
    ]
    frequency = models.DurationField(choices=FREQUENCY_OPTIONS, default=timedelta(weeks=1))
    slug = models.SlugField(default='')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.room.slug}/{self.slug}"

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail



class History(models.Model):
    chore = models.OneToOneField(Chore, on_delete=models.CASCADE, related_name='history')

    def __str__(self):
        return f'History for {self.chore.name}'

    def add_entry(self, done_at, assignee, difficulty_score):
        HistoryEntry.objects.create(
            history=self,
            done_at=done_at,
            assignee=assignee,
            difficulty_score=difficulty_score
        )


class HistoryEntry(models.Model):
    done_at = models.DateTimeField()
    difficulty_score = models.PositiveSmallIntegerField(default=1,
                                                        validators=[MinValueValidator(1), MaxValueValidator(10)])

    history = models.ForeignKey('History', on_delete=models.CASCADE, related_name='entries')
    assignee = models.ForeignKey('assignee.Assignee', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.assignee} did {self.history.chore.name} at {self.done_at}'
