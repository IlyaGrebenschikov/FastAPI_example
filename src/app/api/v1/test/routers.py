from fastapi import APIRouter


test_router = APIRouter()


@test_router.get("/test_endpoint")
async def test_endpoint():
    return {"message": "This is a test endpoint"}

