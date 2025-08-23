from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: bool = True
    message: str = Field(..., description="Error message explaining what went wrong")
    example: Optional[str] = Field(None, description="Example of correct usage")
    note: Optional[str] = Field(None, description="Additional notes or guidance")
