# Rust Code Review Rules

Verify Rust code safety and performance guidelines:
- Check for unnecessary `.unwrap()` or `.expect()` calls that can cause panics in production.
- Ensure proper error propagation using the `?` operator.
- Verify borrowing and lifetime efficiency (avoid unnecessary `.clone()`).
- Check thread safety and concurrency primitives (`Arc<Mutex<T>>`, `tokio` tasks).
