from aiogram import Router

from .contact_router import router as contacts_router
from .event_router import router as event_router
from .general_router import router as general_router
from .help_callback import router as help_callback_router
from .note_router import router as note_router

router = Router(name = __name__)
router.include_routers(
    contacts_router,
    event_router,
    help_callback_router,
    note_router
)

# Because general_router contains fallback
router.include_router(general_router)
