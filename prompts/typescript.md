# JavaScript / TypeScript Code Review Rules

Verify JavaScript and TypeScript web and node.js applications:
- Check for unhandled Promise rejections and async/await try-catch blocks.
- Ensure strict type safety (avoid implicit or explicit `any` types).
- Verify state mutations and race conditions in frontend hooks or backend handlers.
- Check for memory leaks in event listeners or intervals without cleanup.
- Verify OWASP web security (XSS prevention, input sanitization).
