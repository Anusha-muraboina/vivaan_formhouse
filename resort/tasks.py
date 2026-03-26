from celery import shared_task
from .views import sync_ical

@shared_task
def sync_all_calendars():
    urls = [
        "https://ical.booking.com/v1/export/t/9208ef1c-451d-49ab-ad60-38c0710134fc.ics",
        # Add more later
    ]

    for url in urls:
        try:
            sync_ical(url)
        except Exception as e:
            print("SYNC FAILED:", url, str(e))