## Why

Grind level is a key variable in coffee brewing that directly affects extraction. Tracking it alongside dosage and brew type lets users reproduce good results and dial in their grinder over time.

## What Changes

- Add a `grind_level` field (float) to the Tasting model and database schema
- Add a grind-level selector in the tasting modal UI, using the same spinning-wheel `<select>` pattern as dosage
- Grind level adjustable in steps of 0.2
- Smart defaults: pre-populate with the last grind level used for that coffee, or fall back to brew-type defaults (espresso: 4.0, brew: 14.0, metal_brew: 18.0)
- Include grind level in tasting API endpoints (POST/PUT) and display it in tasting history

## Capabilities

### New Capabilities
- `tasting-grind-level`: Grind level field on tastings with smart defaults and spinning-wheel UI selector

### Modified Capabilities
- `tasting-model`: Add `grind_level` float field to Tasting dataclass and DB schema
- `tasting-api`: Accept and return `grind_level` in POST/PUT tasting endpoints
- `tasting-ui`: Add grind-level selector to tasting modal, display in tasting history

## Impact

- **Models**: `Tasting` dataclass gains `grind_level: float | None` field
- **Database**: `tastings` table needs `grind_level REAL` column (migration via `init_db`)
- **API**: `/api/tastings` POST and PUT accept/return `grind_level`
- **Frontend**: Tasting modal gets a new grind-level dropdown; tasting history rows show grind level
- **No new dependencies**
