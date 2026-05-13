from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from .forms import NoteForm
from .models import Note


# SQL injection audit example:
# UNSAFE - never build SQL by joining user input into a raw SQL string.
# search = request.GET.get('q', '')
# notes = Note.objects.raw("SELECT * FROM notes_note WHERE title LIKE '%" + search + "%'")
#
# SAFE - Django ORM parameterizes the query instead of treating user input as SQL.
# notes = Note.objects.filter(title__icontains=search)


# Cache this list page for 5 minutes (300 seconds).
# Good candidate: the list page may be visited often and performs a database query.
# Stale-data risk: after a note is added, edited, or deleted, users may see the old
# list for up to 5 minutes. This is acceptable for a small class notes application.
@cache_page(60 * 5)
def note_list(request):
    search = request.GET.get('q', '').strip()
    notes = Note.objects.all().order_by('-created_at')
    if search:
        notes = notes.filter(title__icontains=search)
    return render(request, 'notes/note_list.html', {'notes': notes, 'search': search})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'page_title': 'Create Note'})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'page_title': 'Edit Note'})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
