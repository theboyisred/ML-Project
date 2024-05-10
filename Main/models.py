from io import BytesIO
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

# Model representing a job


class Job(models.Model):
    name = models.CharField(max_length=1024, null=False, blank=False)
    description = models.TextField()
    wages = models.DecimalField(decimal_places=2, max_digits=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

# Function to generate a unique image name based on UUID and timestamp


def generate_unique_image_name(ext):
    unique_id = uuid.uuid4()
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_name = f"{timestamp}_{unique_id}.{ext}"
    return unique_name

# Model representing an aptitude question


class AptitudeQuestion(models.Model):
    question = models.CharField(max_length=1024, null=False, blank=False)
    option_a = models.CharField(max_length=1024, null=False, blank=False)
    option_b = models.CharField(max_length=1024, null=False, blank=False)
    option_c = models.CharField(max_length=1024, null=False, blank=False)
    option_d = models.CharField(max_length=1024, null=False, blank=False)
    CHOICES = enumerate(("A", "B", "C", "D"))
    correct_option = models.IntegerField(choices=CHOICES)

    def __str__(self) -> str:
        return f"Aptitude Question {self.pk}"

    def get_options(self) -> tuple:
        return (self.option_a, self.option_b, self.option_c, self.option_d)

    class Meta:
        verbose_name = "Aptitude Test Question"
        verbose_name_plural = "Aptitude Test Questions"

# Model representing a personality question


class PersonalityQuestion(models.Model):
    TAGS = {
        "EXT": "EXT",
        "EST": "EST",
        "AGR": "AGR",
        "CSN": "CSN",
        "OPN": "OPN"
    }

    def validate_tag_count(value):
        tag_instances = PersonalityQuestion.objects.filter(tag=value)
        if tag_instances.count() > 10:
            raise ValidationError(f"Too many instances with tag '{value}'.")

    tag = models.CharField(max_length=50, validators=[
                           validate_tag_count], choices=TAGS)
    question = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.tag}{self.pk}"

    class Meta:
        verbose_name = "Personality Test Question"
        verbose_name_plural = "Personality Test Questions"

# Model representing an attempt of an aptitude question


class AptitudeAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="aq_attempts")
    job = models.ForeignKey(
        Job, on_delete=models.PROTECT
    )
    question = models.ForeignKey(
        AptitudeQuestion, on_delete=models.CASCADE, related_name="aq_attempts")
    answer = models.IntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["user", "question", "job"], name="unique_user_job_aptitude_question")]

# Model representing an attempt of a personality question


class PersonalityAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pq_attempts")
    job = models.ForeignKey(
        Job, on_delete=models.PROTECT
    )
    question = models.ForeignKey(
        PersonalityQuestion, on_delete=models.CASCADE, related_name="pq_attempts")
    TOTALLY_DISAGREE = 1
    SLIGHTLY_DISAGREE = 2
    NEUTRAL = 3
    SLIGHTLY_AGREE = 4
    TOTALLY_AGREE = 5
    PQ_CHOICES = [
        (TOTALLY_DISAGREE, "Totally Disagree"),
        (SLIGHTLY_DISAGREE, "Slightly Disagree"),
        (NEUTRAL, "Neutral"),
        (SLIGHTLY_AGREE, "Slightly Agree"),
        (TOTALLY_AGREE, "Totally Agree")
    ]
    answer = models.IntegerField(choices=PQ_CHOICES)
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["user", "question", "job"], name="unique_user_job_personality_question")]

# Model representing the result of tests for a user


class Result(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Candidate Name")
    role = models.ForeignKey(
        Job, on_delete=models.CASCADE, verbose_name="Role Applied")
    experience = models.JSONField(max_length=1024)
    aptitude_test_result = models.PositiveSmallIntegerField()
    personality_type = models.ImageField(
        upload_to='images/', null=True, blank=True)
    rank_score = models.DecimalField(decimal_places=2, max_digits=16)

    # Function to save a plot image for the personality type
    def save_plot_image(self, plot):
        buffer = BytesIO()
        plot.savefig(buffer, format='png')
        buffer.seek(0)
        image = InMemoryUploadedFile(buffer, 'ImageField', generate_unique_image_name("png"),
                                     'image/png', buffer.getbuffer().nbytes, None)
        self.personality_type = image

    # Function to calculate and display the total years of experience
    def years_of_experience(self):
        # Load the JSON-formatted experience data from the model
        exp_dict: dict = self.experience
        # Sum the years of experience
        exp = sum(map(lambda _: int(_), exp_dict.values()))
        return exp

    def rank_score_func(self, score):
        personality_weight = 0.5
        aptitude_weight = 0.35
        experience_weight = 0.15
        total_weight = personality_weight + aptitude_weight + experience_weight

        # Normalize weights
        personality_weight /= total_weight
        aptitude_weight /= total_weight
        experience_weight /= total_weight
        exp = self.years_of_experience()

        value = (score * personality_weight) + (self.aptitude_test_result *
                                                            personality_weight) + (exp * personality_weight)
        self.rank_score = value

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["username", "role"], name="unique_user_role_result")]
        ordering = ("rank_score",)

    def __str__(self) -> str:
        return f"{self.username.username}—{self.role.name}"

# Model representing the CV of a user


class CV(models.Model):
    qualification_choices = {
        "SSCE": "Senior Secondary Certificate",
        "HND": "Higher National Diploma",
        "DEG": "University Degree",
        "MAS": "Masters Degree",
        "PHD": "Doctorate of Philosophy (PhD.)"
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    email = models.EmailField()
    date_of_birth = models.DateField()
    previous_jobs = models.JSONField(
        verbose_name="Years of Experience", max_length=1024)
    qualification = models.CharField(
        max_length=1024, choices=qualification_choices)
    hobbies = models.CharField(max_length=1024)
