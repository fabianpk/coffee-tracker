"""CoffeeBean model for the Coffee Tracker application."""

from dataclasses import dataclass, field, fields
from datetime import datetime, timezone


@dataclass
class CoffeeBean:
    id: int | None = None
    roaster: str | None = None
    name: str | None = None
    country_grown: str | None = None
    country_roasted: str | None = None
    origin: str | None = None
    process: str | None = None
    roast_level: str | None = None
    tasting_notes: str | None = None
    weight: str | None = None
    price: str | None = None
    brew_score: int | None = None
    espresso_score: int | None = None
    other: str | None = None
    notes: str | None = None
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_row(self) -> dict:
        """Return a dict of column names to values for SQL INSERT (excludes id)."""
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name != "id"}

    def to_dict(self) -> dict:
        """Return a JSON-serializable dict (includes id)."""
        return {f.name: getattr(self, f.name) for f in fields(self)}

    @classmethod
    def from_row(cls, row) -> "CoffeeBean":
        """Create a CoffeeBean from a sqlite3.Row."""
        return cls(**{k: row[k] for k in row.keys()})

    @classmethod
    def from_scan(cls, data: dict) -> "CoffeeBean":
        """Create a CoffeeBean from Claude scan output. Maps 'roastery' to 'roaster'."""
        mapped = dict(data)
        if "roastery" in mapped:
            mapped["roaster"] = mapped.pop("roastery")
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in mapped.items() if k in known})
