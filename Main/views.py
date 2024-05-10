from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .tasks import trigger_async_task
from .utils import aptitude_required, personality_required, cv_required, is_cv_complete, signup, validate_year
from .models import *

# Redirect to view_jobs upon index page access.


def index(request):
    return HttpResponseRedirect(reverse("view_jobs"))

# View all jobs; requires authentication.


@login_required
def view_jobs(request: HttpRequest):
    all_jobs = Job.objects.all()
    is_admin = request.user.is_superuser
    return render(request, "jobs.html", {"jobs": all_jobs, "is_admin": is_admin})

# Log In to User Account


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("view_jobs"))
        else:
            # Add an error message for incorrect credentials
            return render(request, "login.html", {"error": True})
    return render(request, "login.html")

# Create a User Account


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        try:
            user = signup(request, username, password1, password2)
            assert user is not None
            return HttpResponseRedirect(reverse("index"))
        except AssertionError:
            return render(request, "signup.html", {"error": True})
    return render(request, "signup.html")

# Log out User


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Redirect to CV page for job application


@login_required
def apply_view(request, pk):
    return HttpResponseRedirect(reverse("cv", {"job": pk}))

# View job details; requires authentication.


@login_required
def job_details(request, pk):
    try:
        job = Job.objects.get(pk=pk)
        if AptitudeAttempt.objects.filter(job=job, user=request.user).exists():
            return render(request, "details.html", {"job": job, "progress": True})
        return render(request, "details.html", {"job": job})
    except Job.DoesNotExist:
        messages.error(request, "Job does not exist.")
        return HttpResponseRedirect(reverse("view_jobs"))

# Takes the User CV Information.


@login_required
def cv_view(request, pk):
    if is_cv_complete(request.user):
        return HttpResponseRedirect(reverse("aptitude_test", args=[pk]))
    if request.method == "GET":
        return render(request, "cv.html", {"valid_date": validate_year(), "job_id": pk, "range": (1, 2, 3)})
    elif request.method == "POST":
        # Processing CV form data
        data = request.POST
        jobs = {data["job1"]: data["exp1"], data["job2"]                : data["exp2"], data["job3"]: data["exp3"]}
        jobs = {key: value for key, value in jobs.items() if key != ''}
        CV.objects.update_or_create(
            user=request.user,
            name=data["name"],
            email=data["email"],
            date_of_birth=data["DOB"],
            previous_jobs=jobs,
            qualification=data["qualification"],
            hobbies=data["hobbies"],
            defaults={"email": data["email"]}
        )
        return HttpResponseRedirect(reverse("aptitude_test", args=[pk]))

# Take aptitude test; requires authentication.


@login_required
@cv_required
def aptitude_test(request, pk):
    if request.method == "GET":
        aptitude_questions = AptitudeQuestion.objects.all()
        job = Job.objects.get(pk=pk)
        completed_attempts = AptitudeAttempt.objects.filter(
            user=request.user, job=job)
        completed_attempts_dict = {}
        for attempt in completed_attempts:
            completed_attempts_dict[attempt.question_id] = attempt.answer
        return render(request, "aptitude.html", {
            "questions": aptitude_questions,
            "job_id": pk,
            "completed_attempts": completed_attempts_dict
        })
    elif request.method == "POST":
        # Handling form submission
        completed = request.POST.get("completed") == "True"
        # Extracting the POST data
        response = request.POST.copy()  # Create a copy of the QueryDict
        fields_to_remove = ["completed", "csrfmiddlewaretoken"]

        # Remove the specified fields from the copied QueryDict
        for field in fields_to_remove:
            if field in response:
                del response[field]
        try:
            # Fetch the job instance only once outside the loop
            job_instance = Job.objects.get(pk=pk)
            batch = []
            # Fetch all questions in one go
            questions = AptitudeQuestion.objects.in_bulk(response.keys())
            _all_attempted = AptitudeAttempt.objects.filter(
                user=request.user,
                job=job_instance
            ).exists()
            for Q, A in response.items():
                question = questions.get(int(Q))
                if question:
                    if _all_attempted:
                        obj = AptitudeAttempt.objects.get(
                            user=request.user,
                            question=question,
                            job=job_instance,
                        )
                        obj.answer = A
                        obj.completed = completed
                    else:
                        obj = AptitudeAttempt(
                            user=request.user,
                            question=question,
                            job=job_instance,
                            answer=A,
                            completed=completed
                        )
                    batch.append(obj)

                else:
                    messages.error(
                        request, f"Question with ID {Q} does not exist.")
            else:
                AptitudeAttempt.objects.bulk_update(
                    batch, fields=["answer", "completed"]) if _all_attempted else AptitudeAttempt.objects.bulk_create(batch)

        except Job.DoesNotExist:
            messages.error(request, f"Job with ID {pk} does not exist.")
    return HttpResponseRedirect(reverse("personality_test", args=[pk]))

# Take personality test; requires authentication and completed aptitude test.
# This decorator ensures that only authenticated users can access this view.


@login_required
# This decorator ensures that only users with the required aptitude can access this view.
@aptitude_required
def personality_test(request: HttpRequest, pk):
    # Handling GET request
    if request.method == "GET":
        # Fetching all personality questions from the database
        personality_questions = PersonalityQuestion.objects.all()
        # Fetching the job object based on the primary key passed in the URL
        job = Job.objects.get(pk=pk)
        # Fetching completed attempts for the current user and job
        completed_attempts = PersonalityAttempt.objects.filter(
            user=request.user, job=job)
        # Creating a dictionary to store completed attempts for easier access
        completed_attempts_dict = {}
        for attempt in completed_attempts:
            completed_attempts_dict[attempt.question_id] = attempt.answer
        # Rendering the personality test template along with necessary data
        return render(request, "personality.html", {
            "questions": personality_questions,
            "job_id": pk,
            "completed_attempts": completed_attempts_dict
        })
    # Handling POST request
    elif request.method == "POST":
        # Extracting the POST data
        response = request.POST.copy()
        completed = response.get("completed") == "True"
        fields_to_remove = ["completed", "csrfmiddlewaretoken"]

        # Remove the specified fields from the copied QueryDict
        for field in fields_to_remove:
            if field in response:
                del response[field]

        # Fetching the job object based on the primary key passed in the URL
        try:
            job_instance = Job.objects.get(pk=pk)
            batch = []
            # Fetch all questions in one go
            questions = PersonalityQuestion.objects.in_bulk(response.keys())
            _all_attempted = PersonalityAttempt.objects.filter(
                user=request.user,
                job=job_instance
            ).exists()
            # Getting or creating an attempt object for each question
            for Q, A in response.items():
                question = questions.get(int(Q))
                if question:
                    if _all_attempted:
                        obj = PersonalityAttempt.objects.get(
                            user=request.user,
                            question=question,
                            job=job_instance,
                        )
                        obj.answer = A
                        obj.completed = completed
                    else:
                        obj = PersonalityAttempt(
                            user=request.user,
                            question=question,
                            job=job_instance,
                            answer=A,
                            completed=completed
                        )
                    batch.append(obj)

                else:
                    messages.error(
                        request, f"Question with ID {Q} does not exist.")
            else:
                PersonalityAttempt.objects.bulk_update(
                    batch, fields=["answer", "completed"]) if _all_attempted else PersonalityAttempt.objects.bulk_create(batch)

        except Job.DoesNotExist:
            messages.error(request, f"Job with ID {pk} does not exist.")
        # Triggering an asynchronous task if the test is completed, otherwise redirecting to job details page
        return trigger_async_task(request, request.user, pk) if completed else HttpResponseRedirect(reverse("job_details", args=[pk]))

# Success page after completing both tests; requires authentication and completed personality test.


@login_required
@personality_required
def success_page(request: HttpRequest):
    return render(request, "success.html")

# View function for the loading page.


def loading_view(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'loading.html')
    else:
        return HttpResponseRedirect('/')

# View function for the error page.


def error_page(request: HttpRequest):
    if request.method == 'GET':
        message = request.session.get("error_message")
        return render(request, 'error.html', context={"message": message})
    else:
        return HttpResponseRedirect('/')
