from datetime import date
from dateutil.relativedelta import relativedelta
from .models import AptitudeAttempt, CV, Job, PersonalityAttempt, PersonalityQuestion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

# Decorator to check if the user has completed the aptitude test
def aptitude_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_aptitude_complete(request.user):
            return redirect(reverse('aptitude_test', args=args, kwargs=kwargs))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to check if the user has completed the personality test
def personality_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_PT_complete(request.user):
            request.session["error_message"] = "It Seems Like You Have Not Completed The Personality Test."
            return redirect(reverse('error'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to check if the user has completed their CV
def cv_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_cv_complete(request.user):
            messages.error(request, "Please complete your CV first.")
            return redirect(reverse('cv', args=args, kwargs=kwargs))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Function to check if the user has completed the aptitude test
def is_aptitude_complete(user):
    total_attempts = AptitudeAttempt.objects.filter(user=user.pk).count()
    completed_attempts = AptitudeAttempt.objects.filter(
        user=user.pk, completed=True).count()
    return total_attempts > 0 and total_attempts == completed_attempts

# Function to check if the user has completed the personality test
def is_PT_complete(user):
    total_attempts = PersonalityAttempt.objects.filter(user=user.pk).count()
    completed_attempts = PersonalityAttempt.objects.filter(
        user=user.pk, completed=True).count()
    return total_attempts > 0 and total_attempts == completed_attempts

# Function to check if the user has completed their CV
def is_cv_complete(user):
    return CV.objects.filter(user=user).exists()

# Function to compute the aptitude test score for a user and a given job
def compute_aptitude_test_score(user: User, job_pk) -> int:
    assert is_aptitude_complete(user)
    job = Job.objects.get(pk=job_pk)
    attempts = AptitudeAttempt.objects.filter(
        user=user, job=job)
    score = 0
    for attempt in attempts:
        if attempt.answer == attempt.question.correct_option:
            score += 1
    return score

# Function to convert personality test attempts to a dictionary
def convert_personality_test_to_dict(user: User) -> dict:
    assert is_PT_complete(user)
    questions = PersonalityQuestion.objects.all()
    attempts = tuple(PersonalityAttempt.objects.filter(user=user).values())
    org_data = map(lambda attempt: (
        str(questions.get(id=attempt["question_id"])), attempt["answer"]), attempts)
    org_data = dict(org_data)
    return org_data

# Function to handle user signup
def signup(request, username, password, confirm_password):
    # Check if a user with the given username already exists
    if User.objects.filter(username=username).exists():
        return None  # User already exists, return None indicating failure

    # Proceed with user creation if the username is unique
    form = UserCreationForm(
        {"username": username, "password1": password, "password2": confirm_password})
    if form.is_valid():
        user = form.save()
        if user is not None:
            login(request, user)
            return user
    return None  # User creation failed, return None

# Function to validate the minimum year for users (18 years old)
def validate_year():
    _ = date.today() - relativedelta(years=18)
    return _.strftime("%Y-%m-%d")
