from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    questions = Question.objects.all()
    questions_count = questions.count()
    context = {"questions": questions}
    return render(request, "home.html", context)


def loginPage(request):
    # if the user is already logged in they cannot access the login page
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not Exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username/Password Does not exist")

    page = "login"
    context = {"page": page}
    return render(request, "login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    context = {"form": form, "page": "resgiter"}
    return render(request, "login_register.html", context)


def view_question(request, pk):
    answers = Answer.objects.filter(question_id=pk)
    question = Question.objects.get(id=pk)
    context = {"answers": answers, "question": question}
    return render(request, "question_page.html", context)


@login_required(login_url="login")
def add_question(request):
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        return redirect("home")
    context = {"form": form}
    return render(request, "question_form.html", context)


@login_required(login_url="login")
def add_answer(request, pk):
    form = AnswerForm()
    question = Question.objects.get(id=pk)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            view_question_url = reverse("view-question", kwargs={"pk": question.id})
            return redirect(view_question_url)

    context = {"form": form, "question": question}
    return render(request, "answer_form.html", context)

@login_required(login_url="login")
def like_answer(request, answer_id):
    # Get the Answer instance for the given answer_id
    answer = get_object_or_404(Answer, pk=request.POST.get('answer_id'))
    like= Like()
    if request.method == 'POST':
        # Check if the user has already liked the answer
        existing_like = Like.objects.filter(user=request.user, answer_id=answer.id)

        if not existing_like:
            # Create a new Like instance for the answer
            like = Like.objects.create(user=request.user, answer=answer)
            like.save()

        else:
            # If the user has already liked the answer, delete the existing like
            existing_like.delete()

        # Update and Save the total_likes for the answer
        answer.update_total_likes()
        answer.save()

        # Redirect to the view-question page for the associated question
    return HttpResponseRedirect(reverse("view-question", kwargs={"pk": answer.question_id}))
    

@login_required(login_url="login")
def update_question(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            view_question_url = reverse("view-question", kwargs={"pk": question.id})
            return redirect(view_question_url)
    return render(request, "question_form.html", {"form": form})

@login_required(login_url="login")
def update_answer(request, ans_id):
    answer = Answer.objects.get(id=ans_id)
    form = AnswerForm(instance=answer)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            view_question_url = reverse(
                "view-question", kwargs={"pk": answer.question_id}
            )
            return redirect(view_question_url)
    return render(request, "answer_form.html", {"form": form})


@login_required(login_url="login")
def delete_question(request, pk):
    question = Question.objects.get(id=pk)
    if question.user == request.user:
        if request.method == "POST":
            question.delete()
            return redirect("home")
    return render(request, "delete.html", {"obj": question})
