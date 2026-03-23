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
    deep_total: int = 25  # Must match len(DEEP_STATIONS) in sweep_checks.py
    surface_ok: int = 0
    surface_empty: int = 0
    surface_404: int = 0

    @property
    def display_health(self) -> int | None:
        """Unified /100 score for display (no boost — raw score).

        Priority: realism_score (native /100) > score (converted /10 → /100).
        """
        if self.realism_score is not None:
            return self.realism_score
        if self.score is not None:
            return int(self.score * 10)
        return None


class SweepHistoryEntry(BaseModel):
    """Single data point in a sweep history time-series."""

    date: str
    health: int | None = None
    realism_score: int | None = None
    score: float | None = None
    overall_status: str = ""
    fixes_applied: int | None = None
    p1_findings: list[str] = []
    report_file: str = ""
    deep_pass: int = 0
    surface_ok: int = 0
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
        if self.sweep and self.sweep.display_health is not None:
            return str(self.sweep.display_health)
        return "\u2014"

    @property
    def score_class(self) -> str:
        if self.sweep:
            if self.sweep.overall_status == "PASS":
                return "good"
            if self.sweep.overall_status == "FAIL":
                return "warn"
            if self.sweep.display_health is not None:
                return "good" if self.sweep.display_health >= 60 else "warn"
        return "pending"
