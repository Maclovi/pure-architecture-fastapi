from fastapi import APIRouter, status

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["Healthcheck"],
    include_in_schema=True,
)


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def get_status() -> dict[str, str]:
    """Healthcheck endpoint to verify service availability.

    Returns:
        dict[str, str]: Response containing service status with keys:
            - "message": Always returns "ok"
            - "status": Always returns "success"

    Notes:
        - This endpoint is typically used by monitoring systems
        - Returns HTTP 200 OK when service is operational
        - Included in OpenAPI schema documentation
    """
    return {"message": "ok", "status": "success"}
