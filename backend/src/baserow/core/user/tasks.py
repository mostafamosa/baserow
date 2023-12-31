from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

from baserow.config.celery import app

User = get_user_model()


@app.task(bind=True, queue="export")
def check_pending_account_deletion(self):
    """
    Periodic tasks that delete pending deletion user account that has overcome the
    grace delay.
    """

    from .handler import UserHandler

    UserHandler().delete_expired_users_and_related_workspaces_if_last_admin()


@app.task(bind=True, queue="export")
def flush_expired_tokens(self):
    """
    Flushes the expired blacklisted refresh tokens.
    """

    from django.utils import timezone

    from baserow.core.models import BlacklistedToken

    BlacklistedToken.objects.filter(expires_at__lte=timezone.now()).delete()


# noinspection PyUnusedLocal
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        getattr(settings, "CHECK_PENDING_ACCOUNT_DELETION_INTERVAL", timedelta(days=1)),
        check_pending_account_deletion.s(),
    )
    sender.add_periodic_task(
        timedelta(days=1),
        flush_expired_tokens.s(),
    )
