# Example: Python FastAPI Endpoint Review

## Input (`target_code`)

```diff
--- a/app/routes/users.py
+++ b/app/routes/users.py
@@ -14,6 +14,15 @@ def get_db():
+@router.get("/users/search")
+def search_users(q: str, db: Session = Depends(get_db)):
+    sql = f"SELECT id, email, role FROM users WHERE email LIKE '%{q}%'"
+    rows = db.execute(text(sql)).fetchall()
+    return {"results": [dict(r._mapping) for r in rows]}
+
+@router.delete("/users/{user_id}")
+def delete_user(user_id: int, db: Session = Depends(get_db)):
+    db.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
+    db.commit()
+    return {"deleted": user_id}
```

## Expected Output (`review_report`)

# Code Review Report

## Summary
- **Scope Reviewed**: `app/routes/users.py` (+11 lines)
- **Verdict**: `Request changes`
- **Overview**: Two critical security vulnerabilities were identified: an unparameterized SQL query allowing SQL injection and an unauthenticated destructive endpoint lacking authorization checks.

## Findings

### Critical (Must Fix Before Merge)
- **`app/routes/users.py:16` — SQL Injection in `search_users`**
  - **Issue**: User input `q` is interpolated directly into `text(sql)` via an f-string, enabling arbitrary SQL injection.
  - **Fix**:
    ```python
    stmt = text("SELECT id, email, role FROM users WHERE email LIKE :pattern LIMIT 50")
    rows = db.execute(stmt, {"pattern": f"%{q}%"}).fetchall()
    ```

- **`app/routes/users.py:21` — Missing Authentication and Authorization on `delete_user`**
  - **Issue**: Any unauthenticated caller can delete arbitrary users by ID (Broken Object Level Authorization / missing auth dependency).
  - **Fix**: Require an authenticated principal dependency (e.g., `current_user: User = Depends(require_admin)`) and verify ownership/admin role before deleting.

### Major (Should Fix)
- **`app/routes/users.py:16` — Unbounded Result Set**
  - **Issue**: `search_users` has no `LIMIT` or pagination, allowing a broad query like `q=""` to dump the entire `users` table.
  - **Fix**: Add `LIMIT :limit` with a validated `limit: int = Query(default=25, ge=1, le=100)` parameter.

### Minor / Nit
- **`app/routes/users.py:24` — Idempotency / 404 Handling**: `delete_user` returns HTTP 200 even if `user_id` does not exist; check `result.rowcount` and return `404` if appropriate for your API contract.

## Test & Verification Gaps
- No unit or integration tests included for `search_users` (injection payloads, pagination bounds) or `delete_user` (unauthorized caller returning `401`/`403`).
