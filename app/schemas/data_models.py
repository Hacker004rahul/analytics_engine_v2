"""
data_models.py
--------------
Pydantic v2 request/response validation schemas for the Analytics Engine.

TransactionRequest  – enforces strict field-level constraints on incoming POST body.
AnalyticsResponse   – defines a structured, nested JSON output contract.
"""

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Schema 1 – Request Payload Contract
# ---------------------------------------------------------------------------

class TransactionRequest(BaseModel):
    """
    Validates the incoming transaction body for POST /metrics/calculate.

    Constraints
    -----------
    unit_price : float  – must be strictly greater than 0.0
    quantity   : int    – must be strictly greater than 0
    currency   : str    – max 3 characters; auto-uppercased before validation
    """

    unit_price: float = Field(
        ...,
        gt=0.0,
        description="Price per unit. Must be a positive non-zero value.",
        examples=[29.99],
    )

    quantity: int = Field(
        ...,
        gt=0,
        description="Number of units purchased. Must be a positive non-zero integer.",
        examples=[5],
    )

    currency: str = Field(
        ...,
        max_length=3,
        description="ISO 4217 currency code (e.g. USD, INR, EUR). Auto-uppercased.",
        examples=["INR"],
    )

    # Auto-uppercase the currency string before the max_length check runs
    @field_validator("currency", mode="before")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value


# ---------------------------------------------------------------------------
# Schema 2 – Nested Response Payload Matrix
# ---------------------------------------------------------------------------

class FormattedMetadata(BaseModel):
    """
    Child model embedded inside AnalyticsResponse.

    currency : str  – the ISO currency code echoed back to the client
    display  : str  – human-readable formatted total string
    """

    currency: str = Field(
        ...,
        description="ISO currency code used in this transaction.",
        examples=["INR"],
    )

    display: str = Field(
        ...,
        description="Localised display string showing the final total.",
        examples=["Total amount is ₹450.00"],
    )


class AnalyticsResponse(BaseModel):
    """
    Structured JSON response returned by POST /metrics/calculate.

    raw_total          : float            – unit_price × quantity
    is_bulk_order      : bool             – True when quantity >= 10
    formatted_metadata : FormattedMetadata – nested currency + display fields
    """

    raw_total: float = Field(
        ...,
        description="Computed total value: unit_price × quantity.",
        examples=[449.85],
    )

    is_bulk_order: bool = Field(
        ...,
        description="True when quantity is 10 or greater; False otherwise.",
        examples=[False],
    )

    formatted_metadata: FormattedMetadata = Field(
        ...,
        description="Nested object containing currency code and localised display string.",
    )
