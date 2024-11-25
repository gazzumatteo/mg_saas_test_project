# Generated by Django 5.0.6 on 2024-05-20 12:55

from django.db import migrations


def create_celery_tasks(apps, schema_editor):
    from django_celery_beat.models import DAYS
    IntervalSchedule = apps.get_model("django_celery_beat", "IntervalSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    daily_schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=DAYS,
    )
    PeriodicTask.objects.create(
        name="sync-subscriptions-every-day",
        task="apps.subscriptions.tasks.sync_subscriptions_task",
        interval=daily_schedule,
        expire_seconds=60 * 60,  # cancel this task after one hour if it hasn't started
    )


def delete_celery_tasks(apps, schema_editor):
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")
    PeriodicTask.objects.filter(name="sync-subscriptions-every-day").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_celery_tasks, reverse_code=delete_celery_tasks)
    ]