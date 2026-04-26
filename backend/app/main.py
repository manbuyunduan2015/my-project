from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import NotFoundException, DuplicateException, ForbiddenException
from app.utils.response import success_response, error_response
from app.api.router import include_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="整车零部件管理系统",
        description="Vehicle Parts Management System API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    include_routers(app)

    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(status_code=exc.status_code, content=error_response(message=exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(status_code=422, content=error_response(message=str(exc.errors())))

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request, exc):
        return JSONResponse(status_code=404, content=error_response(message=exc.detail))

    @app.exception_handler(DuplicateException)
    async def duplicate_handler(request, exc):
        return JSONResponse(status_code=409, content=error_response(message=exc.detail))

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(request, exc):
        return JSONResponse(status_code=403, content=error_response(message=exc.detail))

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
