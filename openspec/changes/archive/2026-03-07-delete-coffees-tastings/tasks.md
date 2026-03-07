## 1. API

- [x]1.1 Update `delete_coffee()` in `app.py`: delete all tastings for the coffee before deleting the coffee, in a single transaction
- [x]1.2 Add `DELETE /api/tastings/<id>` route: delete tasting by ID, return 200 or 404

## 2. Frontend

- [x]2.1 Add a delete button to each tasting entry in the tasting history; on click, confirm and call `DELETE /api/tastings/<id>`, then refresh the tasting list and reload coffees
- [x]2.2 Update `deleteCoffee()` confirm message to "Delete this coffee and all its tastings?"
