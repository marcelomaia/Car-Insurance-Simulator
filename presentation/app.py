"""FastAPI application factory."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import DomainError, InvalidDeductiblePercentageError, NegativeAppliedRateError
from presentation.api.router import router


def create_app() -> FastAPI:
    """Wire router and map ``DomainError`` subclasses to HTTP **422** (readme §5 / execution plan Phase 4)."""

    def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
        if isinstance(exc, InvalidDeductiblePercentageError):
            code = "invalid_deductible_percentage"
        elif isinstance(exc, NegativeAppliedRateError):
            code = "negative_applied_rate"
        else:
            code = "domain_error"
        detail = {"code": code, "message": str(exc)}
        return JSONResponse(status_code=422, content={"detail": detail})

    application = FastAPI(title="Car Insurance Premium Simulator", version="0.1.0")
    application.add_exception_handler(DomainError, domain_error_handler)

    @application.get("/health")
    def health_check() -> dict[str, str]:
        """Liveness probe for Docker / orchestrators (`docker-compose` healthcheck)."""
        return {"status": "ok"}

    application.include_router(router)
    return application
