from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    questions = Question.objects.all()
    questions_count = questions.count()
    context = {"questions": questions}
    return render(request, "home.html", context)


def loginPage(request):
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
    return render(request, "login_register.html")


def logoutPage(request):
    logout(request)
    return redirect("home")


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


def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    # Check if the currently logged_in user has already liked the answer
    if Like.objects.filter(user=request.user, answer=answer).exists():
        view_question_url = reverse("view-question", kwargs={"pk": answer.question_id})
        return redirect(view_question_url)
    if request.method == "POST":
        like = Like.objects.create(user=request.user, answer=answer)
        answer.update_total_likes()
        like.save()
    # Redirect back to the view-question page with the fragment identifier (answer_id)
    view_question_url = (
        reverse("view-question", kwargs={"pk": answer.question_id}) + f"#{answer_id}"
    )
    return redirect(view_question_url)


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
    if(question.user==request.user):
        if request.method == "POST":
            question.delete()
            return redirect("home")
    return render(request, "base/delete.html", {"obj": question})
    