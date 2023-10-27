from django.db import models
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    project_id = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('project_detail_view', args=[str(self.id)])

class PieceInputs(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    piece_name = models.CharField(max_length=200)
    keyword = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    old_content_link = models.URLField(blank=True, null=True)
    include_data = models.CharField(max_length=255, blank=True, null=True)
    csvs = models.FileField(upload_to='csvs/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('piece_inputs_detail_view', args=[str(self.id)])

class PieceBackground(models.Model):
    piece_inputs = models.ForeignKey(PieceInputs, on_delete=models.CASCADE)
    outline = models.TextField()
    research = models.TextField()

    def get_absolute_url(self):
        return reverse('piece_background_detail_view', args=[str(self.id)])

class Piece(models.Model):
    piece_inputs = models.ForeignKey(PieceInputs, on_delete=models.CASCADE)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('piece_detail_view', args=[str(self.id)])
