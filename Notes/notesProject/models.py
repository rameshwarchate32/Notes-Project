from django.db import models

# Create your models here.
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Summary(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="summaries")
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.note.title}"
from django.db import models

# Create your models here.
