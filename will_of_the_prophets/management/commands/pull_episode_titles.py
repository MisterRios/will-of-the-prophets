import datetime

from django.core.management.base import BaseCommand

import feedparser

from will_of_the_prophets.models import Episode


class Command(BaseCommand):
    help = "Downloads episode titles and saves them to the database"

    def handle(self, *args, **options):
        feed = feedparser.parse("http://feeds.feedburner.com/TheGreatestGeneration")
        for item in feed.entries:
            date = item.published_parsed
            episode_date = datetime.datetime(
                year=date.tm_year,
                month=date.tm_mon,
                day=date.tm_mday,
                hour=date.tm_hour,
            )
            Episode.objects.get_or_create(
                itunes_id=item.itunes_episode, title=item.title, date=episode_date
            )
