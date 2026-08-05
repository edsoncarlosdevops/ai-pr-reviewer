# Go Code Review Rules

Verify Go code against standard Go proverbs and performance guidelines:
- Check for unhandled error returns (`if err != nil`).
- Ensure goroutine leaks are prevented (context cancellation, channel closing).
- Check for race conditions on shared memory structures.
- Verify proper slice allocations (`make([]T, 0, capacity)`).
- Ensure mutex locks/unlocks use `defer mu.Unlock()`.
