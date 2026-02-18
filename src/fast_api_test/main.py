from fastapi import FastAPI

from settings import settings

app = FastAPI()


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
