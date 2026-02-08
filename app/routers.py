import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.database import get_db
from app.logger import logger
from app.schemas import URLCreate, URLInfo
from app.service import create_short_code, get_full_url
from app.utils import build_short_url

router = APIRouter()


@router.post(
    "/shorten",
    response_model=URLInfo,
    status_code=status.HTTP_201_CREATED,
)
def shorten_url(
        payload: URLCreate,
        request: Request,
        conn: sqlite3.Connection = Depends(get_db),
) -> URLInfo:
    """Create a short URL for the provided link."""
    logger.info("Shorten request received")

    try:
        code = create_short_code(conn, str(payload.full_url))
    except RuntimeError:
        logger.error("Failed to generate unique short code")
        raise HTTPException(
            status_code=500,
            detail="Could not generate unique short code",
        )

    short_url = build_short_url(str(request.base_url), code)

    return URLInfo(
        short_code=code,
        short_url=short_url,
        full_url=payload.full_url,
    )


@router.get("/{code}")
def redirect(code: str, conn: sqlite3.Connection = Depends(get_db)):
    """Redirect to the original URL by short code."""
    full_url = get_full_url(conn, code)

    if full_url is None:
        logger.warning("Code not found: %s", code)
        raise HTTPException(status_code=404, detail="URL not found")

    logger.info("Redirecting for code: %s", code)
    return RedirectResponse(full_url)
