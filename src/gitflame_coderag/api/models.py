"""Wire models shared with the CodePilot Agent Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SearchFilters(ApiModel):
    repository_id: str = Field(min_length=1, max_length=200)
    commit_sha: str | None = Field(default=None, max_length=200)
    revision: str | None = Field(default=None, max_length=200)
    include: list[str] = Field(default_factory=lambda: ["**/*"], max_length=100)
    exclude: list[str] = Field(default_factory=list, max_length=100)

    @field_validator("include", "exclude")
    @classmethod
    def patterns_must_be_bounded(cls, value: list[str]) -> list[str]:
        if any(not pattern or len(pattern) > 500 for pattern in value):
            raise ValueError("path patterns must contain 1 to 500 characters")
        return value


class SearchRequest(ApiModel):
    query: str = Field(min_length=1, max_length=2_000)
    top_k: int = Field(default=10, ge=1, le=50)
    filters: SearchFilters

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("query cannot be blank")
        return value


class SearchResult(ApiModel):
    path: str = Field(min_length=1, max_length=500)
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    score: float = Field(ge=0.0, le=1.0)
    content: str = Field(max_length=50_000)

    @model_validator(mode="after")
    def line_range_must_be_ordered(self) -> SearchResult:
        if self.end_line < self.start_line:
            raise ValueError("end_line must be greater than or equal to start_line")
        return self


class SearchResponse(ApiModel):
    results: list[SearchResult]


class HealthResponse(ApiModel):
    status: str
    database: str
    version: str = "1.0.0"
