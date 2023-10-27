from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count
import csv

from .models import Project, PieceBackground, Piece, PieceInputs
from .forms import ProjectCreateForm, PieceInputsForm

def home(request):
    return redirect('project_list')

class ProjectList(ListView):
    model = Project
    template_name = 'spinner/home.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.annotate(
            num_pieces_prepared=Count('pieceinputs'),
            num_pieces_outlined=Count('pieceinputs__piecebackground'),
            num_pieces_generated=Count('pieceinputs__piece')
        )

class ProjectCreate(CreateView):
    model = Project
    template_name = 'spinner/project_create_form.html'
    form_class = ProjectCreateForm

    def get_success_url(self):
        return reverse_lazy('project_list')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'spinner/project_detail.html'

class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'spinner/project_update_form.html'
    form_class = ProjectCreateForm

    def get_success_url(self):
        return reverse_lazy('project_detail_view', args=[self.object.id])

class ProjectDelete(DeleteView):
    model = Project
    template_name = 'spinner/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

def handle_csv_upload(csv):
    csv_reader = csv.reader(csv)
    for row in csv_reader:
        print(row)
        if row[0] == 'keyword':
            continue
        else:
            keyword = row[0]
            location = row[1]
            old_content_link = row[2]
            include_data = row[3]
            # csvs should be the name of hte csv file
            csvs = csv
            piece_inputs = PieceInputs.objects.create(keyword=keyword, location=location, old_content_link=old_content_link, include_data=include_data, csvs=csvs)
            piece_inputs.save()




from django.forms import formset_factory

def piece_inputs(request, pk):
    project = Project.objects.get(id=pk)
    PieceFormSet = formset_factory(PieceInputsForm, extra=1)  # This allows you to create multiple pieces. `extra=1` will display 1 empty form by default.

    if request.method == 'POST':
        formset = PieceFormSet(request.POST, prefix='piece')
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    piece = form.save(commit=False)
                    piece.project = project
                    piece.save()

                    # If there's a CSV upload field in each form
                    if 'csv_file' in form.cleaned_data:
                        handle_csv_upload(form.cleaned_data['csv_file'])

            return redirect('project_detail_view', pk=pk)
    else:
        formset = PieceFormSet(queryset=PieceInputs.objects.none(), prefix='piece', initial=[{'project': project}])
    return render(request, 'spinner/piece_inputs_form.html', {'formset': formset})

def piece_backgrounds(pk):
    project = Project.objects.get(id=pk)
    piece_inputs = PieceInputs.objects.filter(project=project)
    for piece_input in piece_inputs:
        piece_background = PieceBackground.objects.create(piece_input=piece_input)
        piece_background.save()
    return redirect('project_detail_view', pk=pk)

def piece_inputs_for_project(request, project_id):
    # Your view logic here
    pass
