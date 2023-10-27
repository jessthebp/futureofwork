from django import forms
from .models import Project, PieceBackground, Piece, PieceInputs

class ProjectCreateForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = ("project_id", "brand", "location")


class PieceInputsForm(forms.ModelForm):
    csv_file = forms.FileField(required=False, label='Upload CSV')  # Existing CSV upload field

    class Meta:
        model = PieceInputs
        fields = ("project", "piece_name", "keyword", "location", "old_content_link", "include_data", "csv_file")


class PieceCreateForm(forms.ModelForm):
    class Meta:
        model = PieceBackground
        fields = ("piece_inputs", "outline", "research")

class PieceUpdateForm(forms.ModelForm):
    class Meta:
        model = PieceBackground
        fields = ("piece_inputs", "outline", "research")

