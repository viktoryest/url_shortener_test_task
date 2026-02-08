from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class URLCreate(BaseModel):
    full_url: HttpUrl = Field(..., description="Original URL to be shortened")


class URLInfo(BaseModel):
    short_code: str = Field(
        ...,
        min_length=4,
        max_length=16,
        description="Unique generated code identifying the URL"
    )
    short_url: str
    full_url: HttpUrl

    model_config = ConfigDict(from_attributes=True)
