#!/usr/bin/env python3
"""
test_field_router.py - Test suite for Field Router
"""
import pbi_inspect as pbi

print("=" * 60)
print("FIELD ROUTER - FUNCTIONAL TEST")
print("=" * 60)

# Test 1: Normalize key
print("\n1. Test: Normalize key (remove spaces, underscores, case)")
print("-" * 60)
test_names = ["Customer_Name", "CustomerName", "customer name", "CUSTOMER-ID"]
for name in test_names:
    normalized = pbi.normalize_key(name)
    print(f"  '{name}' -> '{normalized}'")

# Test 2: Similarity scoring
print("\n2. Test: Similarity scoring")
print("-" * 60)
print("(0.0 = completely different, 1.0 = identical)")
pairs = [
    ("CustomerID", "CustomerID"),
    ("CustomerID", "Customer_ID"),
    ("OrderDate", "OrderDates"),
    ("Name", "DisplayName"),
    ("Sales", "Sells"),
]
for old, new in pairs:
    score = pbi.similarity(old, new)
    confidence_pct = f"{score*100:.0f}%"
    print(f"  '{old}' vs '{new}' = {confidence_pct:>4}")

# Test 3: Detect naming style
print("\n3. Test: Detect naming style conventions")
print("-" * 60)
names = ["customer_id", "customerId", "CustomerId", "Customer ID", "CUSTOMER"]
for name in names:
    style = pbi.detect_style(name)
    print(f"  '{name:20}' -> {style}")

# Test 4: Match field (example)
print("\n4. Test: Field matching with confidence scoring")
print("-" * 60)
old_field = {"entity": "Sales", "property": "OrderDate", "kind": "Column"}
inventory = [
    {"entity": "Orders", "property": "Date", "kind": "Column"},
    {"entity": "Orders", "property": "OrderDate", "kind": "Column"},
    {"entity": "Sales", "property": "OrderDate", "kind": "Column"},
]

print(f"  Old field: {old_field['entity']}.{old_field['property']}")
print(f"  Inventory to search:")
for item in inventory:
    print(f"    - {item['entity']}.{item['property']}")

match = pbi.match_field(old_field, inventory)
print(f"\n  Match Result:")
print(f"    Status: {match['status']}")
print(f"    Confidence: {match['confidence']*100:.0f}%")
if match['match']:
    print(f"    Matched to: {match['match']['entity']}.{match['match']['property']}")
print(f"    Note: {match['note']}")

# Test 5: Majority style detection
print("\n5. Test: Majority naming style in dataset")
print("-" * 60)
fields = [
    {"property": "customer_id", "entity": "Customers", "kind": "Column"},
    {"property": "order_date", "entity": "Orders", "kind": "Column"},
    {"property": "product_name", "entity": "Products", "kind": "Column"},
]
style = pbi.majority_style(fields)
print(f"  Fields: {[f['property'] for f in fields]}")
print(f"  Majority style: {style}")

# Test 6: Levenshtein distance
print("\n6. Test: Levenshtein distance (edit distance)")
print("-" * 60)
word_pairs = [
    ("kitten", "sitting"),
    ("Saturday", "Sunday"),
    ("hello", "hello"),
]
for w1, w2 in word_pairs:
    distance = pbi.levenshtein(w1, w2)
    print(f"  '{w1}' -> '{w2}' = {distance} edits")

print("\n" + "=" * 60)
print("✓ All functional tests completed successfully!")
print("=" * 60)
print("\nTo test with actual .pbix files, use:")
print("  python pbi_inspect.py report.pbix --list-pages")
print("  python pbi_inspect.py report.pbix --page 0")
print("  python pbi_inspect.py old.pbix --page 0 --scope new.pbix --out mapping")
