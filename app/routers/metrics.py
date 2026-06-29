"""
metrics.py
----------
Refactored API router.  All endpoints accept structured Pydantic bodies
(POST) instead of loose query parameters.

Routes
------
POST /metrics/calculate  – validate TransactionRequest, return AnalyticsResponse
"""

from fastapi import APIRouter
from app.schemas.data_models import (
    AnalyticsResponse,
    FormattedMetadata,
    TransactionRequest,
)

router = APIRouter(prefix="/metrics", tags=["Metrics"])


# Currency symbol lookup – extend as needed
_CURRENCY_SYMBOLS: dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "INR": "₹",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
}


def _build_display(currency: str, total: float) -> str:
    """Return a human-readable total string with the correct symbol."""
    symbol = _CURRENCY_SYMBOLS.get(currency, currency + " ")
    return f"Total amount is {symbol}{total:,.2f}"


@router.post(
    "/calculate",
    response_model=AnalyticsResponse,
    summary="Calculate transaction analytics",
    description=(
        "Accepts a validated `TransactionRequest` body and returns a structured "
        "`AnalyticsResponse` containing the raw total, bulk-order flag, and "
        "formatted currency metadata."
    ),
    responses={
        200: {"description": "Analytics computed successfully."},
        422: {"description": "Validation error – one or more fields failed constraints."},
    },
)
def calculate_metrics(payload: TransactionRequest) -> AnalyticsResponse:
    """
    Business logic
    --------------
    1. Compute raw_total  = unit_price × quantity
    2. Set is_bulk_order  = quantity >= 10
    3. Build formatted_metadata with currency code and display string
    """

    raw_total: float = round(payload.unit_price * payload.quantity, 2)
    is_bulk_order: bool = payload.quantity >= 10

    metadata = FormattedMetadata(
        currency=payload.currency,
        display=_build_display(payload.currency, raw_total),
    )

    return AnalyticsResponse(
        raw_total=raw_total,
        is_bulk_order=is_bulk_order,
        formatted_metadata=metadata,
    )
