from django.shortcuts import render
from django.http import HttpResponse
from .models import Question


def index(request): #this function is to display the latest five questions for the voter.
    """
    Display the latest five questions in the system.

    Retrieves the latest questions from the database, ordered by the
    publication date in descending order, and renders them to the 
    'polls/index.html' template. If there are no questions available,
    an appropriate message is displayed.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'polls/index.html' template with 
        the latest five questions.
    """
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id): #this one is to display a specific question
    """
    Display a specific question.

    Retrieve the question with the provided ID from the database and 
    renders it to the 'polls/detail.html' template. If the question does 
    not exist, an appropriate message is displayed.

    Args:
        request: The HTTP request object.
        question_id: The ID of the question to be displayed.

    Returns:
        HttpResponse: The rendered 'polls/detail.html' template with the 
        requested question.
    """
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id): # to display the results to the results html
    """
    Display the results of a specific question.

    Retrieve the question with the provided ID from the database and 
    renders its results to the 'polls/results.html' template. If the 
    question does not exist, an appropriate message is displayed.

    Args:
        request: The HTTP request object.
        question_id: The ID of the question to be displayed.

    Returns:
        HttpResponse: The rendered 'polls/results.html' template with the 
        requested question results.
    """
    
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id): #to handle the voting process, with error handling for when the user does not select a choice
    """
    Handle voting for a specific question.

    Retrieve the question with the provided ID from the database and 
    process the vote for the selected choice. If the choice is not 
    selected or does not exist, redisplay the voting form with an 
    error message. Otherwise, increment the vote count for the selected 
    choice and redirect to the results page for the question.

    Args:
        request: The HTTP request object containing POST data.
        question_id: The ID of the question for which voting is being processed.

    Returns:
        HttpResponse: If an error occurs, render the 'polls/detail.html' 
        template with an error message. Otherwise, redirect to the 
        'polls/results.html' page for the question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("Votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))