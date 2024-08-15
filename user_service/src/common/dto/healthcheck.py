from pydantic import BaseModel


class HealthCheckResponseSchema(BaseModel):
    healthy: bool
