# authlog_api/schemas/events.py
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, IPvAnyAddress, Field, field_validator

Outcome = Literal["success", "failure"]
LogLevel = Literal["INFO", "WARN", "ERROR"]
ActorType = Literal["user", "admin", "service"]

class AuthLogBase(BaseModel):
    actor_id: int = Field(ge=1)                              # positive
    actor_type: ActorType                                    # enum
    event_type: str = Field(min_length=2, max_length=64)     # length
    outcome: Outcome                                         # enum
    ip_address: Optional[IPvAnyAddress] = None               # validated IP
    user_agent: Optional[str] = Field(default=None, max_length=512)
    auth_method: Optional[str] = Field(default=None, max_length=64)
    provider: Optional[str] = Field(default=None, max_length=64)
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = Field(default=None, max_length=256)
    log_level: LogLevel

    @field_validator("failure_reason")
    @classmethod
    def failure_reason_required_on_failure(cls, v, info):
        data = info.data
        if data.get("outcome") == "failure" and not v:
            raise ValueError("failure_reason is required when outcome='failure'")
        return v

class AuthLogCreate(AuthLogBase):
    pass

class AuthLogUpdate(BaseModel):
    actor_type: Optional[ActorType] = None
    event_type: Optional[str] = Field(default=None, min_length=2, max_length=64)
    outcome: Optional[Outcome] = None
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = Field(default=None, max_length=512)
    auth_method: Optional[str] = Field(default=None, max_length=64)
    provider: Optional[str] = Field(default=None, max_length=64)
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = Field(default=None, max_length=256)
    log_level: Optional[LogLevel] = None

class AuthLogOut(AuthLogBase):
    event_id: int
    occurred_at: datetime
    model_config = {"from_attributes": True}
