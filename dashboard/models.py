"""Pydantic models for QBO Demo Manager."""

from pydantic import BaseModel


class Company(BaseModel):
    name: str
    cid: str
    type: str  # parent | child | consolidated | single
    priority: str  # P0 | P1


class SweepResult(BaseModel):
    date: str
    score: float | None = None
    report_file: str
    p1_findings: list[str] = []


class AltCredential(BaseModel):
    email: str
    password: str
    totp_secret: str
    label: str = ""


class Account(BaseModel):
    email: str
    label: str
    shortcode: str
    password: str
    totp_secret: str
    mfa_type: str = "totp"
    dataset: str
    retool_env: str
    companies: list[Company] = []
    alt_credentials: list[AltCredential] = []
    workspace_id: str = ""
    workspace_name: str = ""
    dataset_id: str = ""
    last_login: str | None = None
    sweep: SweepResult | None = None
    notes: str = ""

    @property
    def all_emails(self) -> list[str]:
        return [self.email] + [a.email for a in self.alt_credentials]

    @property
    def entity_count(self) -> str:
        total = len(self.companies)
        has_consolidated = any(c.type == "consolidated" for c in self.companies)
        operating = total - (1 if has_consolidated else 0)
        if has_consolidated:
            return f"{operating}+C"
        return str(total)

    @property
    def score_display(self) -> str:
        if self.sweep and self.sweep.score is not None:
            return str(self.sweep.score)
        return "\u2014"

    @property
    def score_class(self) -> str:
        if self.sweep and self.sweep.score is not None:
            return "good" if self.sweep.score >= 7 else "warn"
        return "pending"
