from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)  # auto_now_add adds time as when the data was inserted
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)   
    # related_name = 'topics' is the method name from entity Board
    # on_delete=models.CASCADE deletes the row associated to the board id in this model when that board is deleted.
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)  
    # related_name = 'topics' is the method name from the entity User. Look at the Class Diagram for guide
    
    def __str__(self):
        return self.subject
    
class Post(models.Model):
    message = models.CharField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    # automatically added date when created
    updated_at = models.DateTimeField(null=True)    # has to be added manually by user
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)    

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)