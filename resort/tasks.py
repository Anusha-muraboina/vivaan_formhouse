from celery import shared_task
from .views import sync_ical

@shared_task
def sync_all_calendars():
    urls = [
        "https://ical.booking.com/v1/export/t/59a7dc20-1fb0-472c-8d56-b97073c7537c.ics",
        # Add more later
    ]

    for url in urls:
        try:
            sync_ical(url)
        except Exception as e:
            print("SYNC FAILED:", url, str(e))