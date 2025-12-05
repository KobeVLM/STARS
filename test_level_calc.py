import math

# Test the level calculation formula
# Level = sqrt(total_xp / 100) + 1

test_cases = [
    (0, 1),      # 0 XP → Level 1
    (100, 2),    # 100 XP → Level 2
    (400, 3),    # 400 XP → Level 3
    (900, 4),    # 900 XP → Level 4
    (10000, 11), # 10000 XP → Level 11
]

print("Testing Level Calculation Formula:")
print("=" * 60)

for xp, expected_level in test_cases:
    calculated = max(1, int(math.sqrt(xp / 100)) + 1)
    status = "✓" if calculated == expected_level else "✗"
    print(f"XP: {xp:5d} | Expected: {expected_level:2d} | Calculated: {calculated:2d} | {status}")

print("\nTesting XP Requirements for Next Level:")
print("=" * 60)

# Test XP needed for each level
for level in range(1, 6):
    xp_needed = (level - 1) ** 2 * 100
    xp_next = level ** 2 * 100
    xp_required = xp_next - xp_needed
    print(f"Level {level} → Level {level + 1}: Need {xp_required:4d} XP (from {xp_needed:5d} to {xp_next:5d})")
