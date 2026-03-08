## 1. Fix scan endpoint

- [x] 1.1 In the `/api/scan` route in `app.py`, capture `details.get("other")` before calling `CoffeeBean.from_scan(details)`, then inject it into the result dict after `coffee.to_dict()` alongside `matched_roaster` and `qr_url`
