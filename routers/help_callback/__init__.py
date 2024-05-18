from aiogram import Router

from routers.help_callback.help_contact import router as contact_help_router
from routers.help_callback.help_event import router as event_help_router
from routers.help_callback.help_general import router as general_help_router
from routers.help_callback.help_note import router as note_help_router

router = Router(name = __name__)
router.include_routers(
    contact_help_router,
    event_help_router,
    general_help_router,
    note_help_router
)
