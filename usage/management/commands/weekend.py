#!/usr/bin/env python3.13
from django.core.management.base import BaseCommand
from ...models import WaterUsage

class Command(BaseCommand):
    """
    Calculate weekday vs. weekend water usage.
    """
    help = "Calculate weekday vs. weekend water usage."

    def handle(self, *args, **options):

        num_weekday = 0
        num_weekend = 0
        total_weekdays = 0
        total_weekends = 0

        # Get all water usage from the database.
        usage = WaterUsage.objects
        for day in usage.all():
            if day.date.strftime('%A') in ('Saturday', 'Sunday'):
                num_weekend += 1
                total_weekends += day.gallons
            else:
                num_weekday += 1
                total_weekdays += day.gallons

        # Show average gallons used on weekdays and weekends, separately.
        average_weekday = total_weekdays / num_weekday
        self.stdout.write(self.style.SUCCESS(
            f"Weekdays:\t{'{0:,.2f}'.format(total_weekdays)} total gallons /"
            f" {num_weekday} week days ="
            f" average {'{0:,.2f}'.format(average_weekday)} gallons."
        ))

        average_weekend = total_weekends / num_weekend
        self.stdout.write(self.style.SUCCESS(
            f"Weekends:\t{'{0:,.2f}'.format(total_weekends)} total gallons /"
            f" {num_weekend} weekend days ="
            f" average {'{0:,.2f}'.format(average_weekend)} gallons."
        ))

        # Show the minimum and maximum dates of water usage from the database.
        dt_fmt = "%A, %B %d, %Y"

        min_date = usage.first()
        self.stdout.write(self.style.SUCCESS(
            f'From:\t\t{min_date.date.strftime(dt_fmt)} ({min_date.date})'
        ))

        max_date = usage.last()
        self.stdout.write(self.style.SUCCESS(
            f'To:\t\t{max_date.date.strftime(dt_fmt)} ({max_date.date})'
        ))
