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
    realism_score: int | None = None  # 0-100
    overall_status: str = ""  # PASS / FAIL / ""
    fixes_applied: int | None = None
    entities_swept: int | None = None
    deep_pass: int = 0
    deep_blocked: int = 0
    deep_total: int = 12
    surface_ok: int = 0
    surface_empty: int = 0
    surface_404: int = 0


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
    total_accesses: int = 0
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
        if self.sweep:
            if self.sweep.overall_status == "PASS":
                return "good"
            if self.sweep.overall_status == "FAIL":
                return "warn"
            if self.sweep.realism_score is not None:
                return "good" if self.sweep.realism_score >= 60 else "warn"
            if self.sweep.score is not None:
                return "good" if self.sweep.score >= 7 else "warn"
        return "pending"
