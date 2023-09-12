from abc import ABCMeta, abstractmethod
from typing import Optional

from baserow.core.exceptions import (
    InstanceTypeAlreadyRegistered,
    InstanceTypeDoesNotExist,
)
from baserow.core.registry import (
    CustomFieldsRegistryMixin,
    Instance,
    MapAPIExceptionsInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

from .models import Notification


class NotificationType(MapAPIExceptionsInstanceMixin, Instance):
    model_class = Notification
    include_in_notifications_email = False


class EmailNotificationTypeMixin(metaclass=ABCMeta):
    """
    A mixin for notification types that can be sent by email, which provides the
    methods needed to render a title and an optional description in the email message.
    """

    include_in_notifications_email = True

    @classmethod
    @abstractmethod
    def get_notification_title_for_email(cls, notification, context) -> str:
        """
        Returns the translatable string title for the given notification and context.
        """

    @classmethod
    @abstractmethod
    def get_notification_description_for_email(
        cls, notification, context
    ) -> Optional[str]:
        """
        Returns the translatable string description for the given notification
        and context.
        """


class CliNotificationTypeMixin(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def prompt_for_args_in_cli_and_create_notification(cls):
        """
        Prompts the user for any additional arguments needed to create the
        notification from the CLI, and then creates the notification.
        """


class NotificationTypeDoesNotExist(InstanceTypeDoesNotExist):
    """Raised when a notification type with a given identifier does not exist."""


class NotificationTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    """Raised when a notification type is already registered."""


class NotificationTypeRegistry(
    CustomFieldsRegistryMixin,
    ModelRegistryMixin[Notification, NotificationType],
    Registry[NotificationType],
):
    """
    The registry that holds all the available job types.
    """

    name = "notification_type"

    does_not_exist_exception_class = NotificationTypeDoesNotExist
    already_registered_exception_class = NotificationTypeAlreadyRegistered


notification_type_registry: NotificationTypeRegistry = NotificationTypeRegistry()
