"""Views."""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import condition
from django.views.generic.edit import CreateView

from will_of_the_prophets import board, forms, models


def get_last_modified(request):
    """Get board's last modified datetime."""
    try:
        return (
            models.Roll.objects.filter(embargo__lte=timezone.now())
            .latest("embargo")
            .embargo
        )
    except models.Roll.DoesNotExist:
        return None


@xframe_options_exempt
@condition(last_modified_func=get_last_modified)
@cache_control(max_age=3600)
def public_board(request):
    """
    Board for the public.

    Does not take embargoed rolls into account.
    """
    now = timezone.now()
    special_squares = board.get_special_squares(now)
    special_square_types = set(special_squares.values())
    episodes = None
    error_messages = []
    board_public = board.Board(now)

    episode_id = request.GET.get("episode", None)
    if episode_id:
        try:
            episode = models.Episode.objects.get(itunes_id=episode_id)
        except models.Episode.DoesNotExist:
            error_messages.append("Not a valid episode number")
        else:
            board_public = board.Board(now=episode.date)

    if models.Roll.objects.exists():
        first_roll_date = models.Roll.objects.first().embargo.date()
        last_roll_date = models.Roll.objects.last().embargo.date()
        latest_published_episode_date = min(last_roll_date, timezone.now().date())
        episodes = models.Episode.objects.filter(
            date__range=(first_roll_date, latest_published_episode_date)
        )
        episodes = episodes.values("itunes_id", "title")

    response = render(
        request,
        "will_of_the_prophets/public_board.html",
        {
            "board": board_public,
            "special_square_types": special_square_types,
            "episodes": episodes,
            "selected": episode_id,
            "error_messages": error_messages,
        },
    )

    canonical_url = settings.PUBLIC_BOARD_CANONICAL_URL
    if canonical_url:
        response["Link"] = f'<{canonical_url}>; rel="canonical"'

    return response


@xframe_options_exempt
@condition(last_modified_func=get_last_modified)
@cache_control(max_age=3600)
def roll_frequency(request):
    """
    Show roll frequency.
    """
    roll_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for roll in models.Roll.objects.filter(embargo__lte=timezone.now()):
        roll_count[roll.number] += 1

    max_count = max(roll_count.values())

    return render(
        request,
        "will_of_the_prophets/roll_frequency.html",
        {"roll_frequency": roll_count, "max_count": max_count},
    )


class RollView(LoginRequiredMixin, CreateView):
    """View for rolling the die."""

    form_class = forms.RollForm
    template_name = "will_of_the_prophets/roll.html"

    def get_context_data(self, **kwargs):
        last_roll = models.Roll.objects.order_by("-embargo").first()
        last_roll_embargo = None
        if last_roll:
            last_roll_embargo = last_roll.embargo

        return super().get_context_data(
            **kwargs,
            last_roll=last_roll,
            board=board.Board(now=last_roll_embargo),
            special_square_types=models.SpecialSquareType.objects.all(),
        )

    def get_success_url(self):
        return reverse("roll") + "#chula"
