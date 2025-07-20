from .start import router as start_router
from .upload import router as upload_router
from .inline import router as inline_router
from .admin import router as admin_router

routers = [
    start_router,
    upload_router,
    inline_router,
    admin_router
]