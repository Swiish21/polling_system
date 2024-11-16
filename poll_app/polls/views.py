"""
Importing necessary modules from Django.

* `db.models`: Django's database modeling module, providing classes for defining database tables.
    + `F`: A class for creating database functions, used for database queries.
* `http`: Django's HTTP module, providing classes for working with HTTP requests and responses.
    + `HttpResponseRedirect`: A class for creating HTTP redirects.
* `shortcuts`: Django's shortcuts module, providing convenience functions for common tasks.
    + `get_object_or_404`: A function for retrieving an object from the database, or raising a 404 error if it doesn't exist.
    + `render`: A function for rendering a template with a given context.
* `urls`: Django's URL routing module, providing functions for working with URLs.
    + `reverse`: A function for reversing URLs, i.e. generating a URL from a view name and arguments.
* `views`: Django's views module, providing classes for defining views.
    + `generic`: A module providing generic views, i.e. views that can be used for common tasks.
"""
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    A view for displaying the index page of the polls app.

    Attributes:
        template_name (str): The name of the template to render for the index page.
        context_object_name (str): The name of the variable in the template context that will hold the list of questions.

    Methods:
        get_queryset: Returns the queryset of questions to be displayed on the index page.

    Description:
        This view displays the index page of the polls app, showing the last five published questions.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions.

        Returns:
            QuerySet: A queryset of Question objects, ordered by publication date in descending order, limited to the last five questions.
        """
        return Question.objects.order_by("-pub_date")[:5]
    
    
class DetailView(generic.DetailView):
    """
    A view for displaying the details of a question.

    Attributes:
        model (Question): The model for the question.
        template_name (str): The name of the template to render for the details page.

    Description:
        This view displays the details of a question, including the question text and the choices.
    """
    model = Question
    template_name = "polls/detail.html"
    
class ResultView(generic.DetailView):
    """
    A view for displaying the results of a poll.

    Attributes:
        model (Question): The model for the poll question.
        template_name (str): The name of the template to render for the results page.

    Description:
        This view displays the results of a poll, including the question and the choices with their respective vote counts.
    """
    model = Question
    template_name = "polls/results.html"
    

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