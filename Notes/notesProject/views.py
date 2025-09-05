from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Student, Note


# Home page
def index(request):
    return render(request, "index.html")


# Register student
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # Basic validation
        if not name or not email or not password or not address:
            messages.error(request, 'All fields are required.')
        elif Student.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
        else:
            # Hash password
            hashed_password = make_password(password)
            student = Student(
                name=name,
                email=email,
                password=hashed_password,
                address=address
            )
            student.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

    return render(request, 'registration.html')


# Login student
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                # Create session
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                messages.success(request, f'Welcome, {student.name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


# Dashboard page
def dashboard(request):
    if 'student_id' not in request.session:
        messages.error(request, 'You must be logged in to view the dashboard.')
        return redirect('login')

    student_id = request.session['student_id']
    try:
        student = Student.objects.get(id=student_id)
        return render(request, 'dashboard.html', {'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Student does not exist.')
        return redirect('login')


# Logout
def logout(request):
    request.session.flush()  # clears all session data
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# List all notes for logged-in student
def notes_list(request):
    if "student_id" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    student_id = request.session["student_id"]
    student = Student.objects.get(id=student_id)
    notes = Note.objects.filter(student=student).order_by("-created_at")

    return render(request, "notes/notes_list.html", {
        "student": student,
        "notes": notes
    })


# Add a new note
def add_note(request):
    if "student_id" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    student_id = request.session["student_id"]
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.error(request, "Both title and content are required.")
        else:
            Note.objects.create(student=student, title=title, content=content)
            messages.success(request, "Note added successfully!")
            return redirect("notes_list")

    return render(request, "notes/add_note.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

def summarize_note(request):
    if request.method == "POST":
        note_id = request.POST.get("note_id")
        note = get_object_or_404(Note, id=note_id)

        # Simple predefined summary: take first 20 words
        content_words = note.content.split()
        summary = " ".join(content_words[:20])
        if len(content_words) > 20:
            summary += "..."

        # Store summary in session
        request.session[f"summary_{note.id}"] = summary

        return render(request, "notes/summary.html", {"note": note, "summary": summary})

    return redirect("notes_list")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note, Student

# Edit a note
def edit_note(request):
    if "student_id" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    student_id = request.session["student_id"]
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        note_id = request.POST.get("note_id")
        note = get_object_or_404(Note, id=note_id, student=student)

        # If form is submitted with new data
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            note.title = title
            note.content = content
            note.save()
            messages.success(request, "Note updated successfully!")
            return redirect("notes_list")
        else:
            messages.error(request, "Both title and content are required.")

        return render(request, "notes/edit_note.html", {"note": note})

    # If GET request, show edit form
    note_id = request.GET.get("note_id")
    note = get_object_or_404(Note, id=note_id, student=student)
    return render(request, "notes/edit_note.html", {"note": note})


# Delete a note
def delete_note(request):
    if "student_id" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    student_id = request.session["student_id"]
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        note_id = request.POST.get("note_id")
        note = get_object_or_404(Note, id=note_id, student=student)
        note.delete()
        messages.success(request, "Note deleted successfully!")
        return redirect("notes_list")

    return redirect("notes_list")

