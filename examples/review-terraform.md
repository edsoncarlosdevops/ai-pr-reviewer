# Terraform PR Review Example

## Code Changes
```diff
-  instance_type = "t2.micro"
+  instance_type = "t3.large"
```

## AI Review
**Performance & Cost:** The instance type upgrade from `t2.micro` to `t3.large` increases compute capacity but will impact AWS costs significantly. Ensure this change is intended for the target environment.
**Maintainability:** Consider parameterizing `instance_type` using a variable to allow environment-specific overrides rather than hardcoding it.
