from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CV, Job, Result
from .utils import convert_personality_test_to_dict, compute_aptitude_test_score
from .preprocessing import preprocessor
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import threading

# Function to run machine learning tasks asynchronously
def run_ML(user: User, job_id):
    # Convert personality test data to dictionary format
    data = convert_personality_test_to_dict(user)
    # Preprocess data and generate a graph
    graph, score = preprocessor(data)

    # Create a Result object with user data and test results
    _res = Result(
        username=user,
        role=Job.objects.get(id=job_id),
        experience=CV.objects.get(user=user).previous_jobs,
        aptitude_test_result=compute_aptitude_test_score(user, job_id))
    
    # Save the plot image to the Result object
    _res.save_plot_image(graph)
    _res.rank_score_func(score)
    try:
        # Save the Result object to the database
        _res.save()
    except IntegrityError:
        print(f"The User '{user.username}' already has an entry for the Job with ID - {job_id}")

# Function to trigger asynchronous machine learning task
def trigger_async_task(request, username, job_id):
    # Start the long-running task in a separate thread
    thread = threading.Thread(target=run_ML, args=(username, job_id))
    thread.start()

    # Check if the thread is still alive
    if thread.is_alive():
        # If the thread is still running, return the loading page
        return HttpResponseRedirect(reverse("loading"))
    else:
        # If the thread has finished, redirect the user to the success page
        return HttpResponseRedirect(reverse("success"))
