from auth_service_backend.settings import auth_service_settings
from fastapi import Depends, FastAPI

from settings import settings

from auth_service_backend.fastapi_backend import FastAPIUser
from one_more_test.deps import current_user_dep

app = FastAPI()

# Configure auth service (required for token validation)
auth_service_settings.configure(
    SERVICE_BASE_URL=settings.AUTH_SERVICE_BASE_URL,
    CLIENT_ID=settings.AUTH_CLIENT_ID,
    CLIENT_SECRET=settings.AUTH_CLIENT_SECRET,
)


@app.get("/status")
async def status():
    return {"status": "ok", "environment": settings.env}


# Include your routers here:
# from my_resource import router as my_resource_router
# app.include_router(
#     my_resource_router.router,
#     prefix="/v1",
#     tags=["my-resource"],
# )

# Example protected route (requires Bearer token and scope):
# @app.get("/protected")
# def protected(user: FastAPIUser = Depends(current_user_dep(["example.read"]))):
#     return {"user_id": user.user_id, "email": user.email}
