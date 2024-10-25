from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    description=models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name="notes"
        verbose_name_plural="notes"
      
    
    

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    subject = models.CharField(max_length=50)  # Subject of the homework
    title = models.CharField(max_length=200)  # Title of the homework
    description = models.TextField()  # Detailed description of the homework
    due = models.DateTimeField()  # Due date and time
    is_finished = models.BooleanField(default=False)  # Flag for completion
    
    def __str__(self):
        return f"{self.title} - {self.subject} (Due: {self.due})"