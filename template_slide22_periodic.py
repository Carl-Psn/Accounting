# Slide 22 - Midterm Review Study Guide 2026
# Rameau Co. | Accounting equation | PERIODIC method
# Affichage seul (pas de saisie). NumWorks: ... > Executer le script
#
# Prochain cas: copier ce fichier et modifier TABLE + END.

print("Rameau solution: accounting equation, periodic method")
print("Assets = Liabilities + Shareholders' equity")
print("")

# En-tete (meme ordre que la slide 22)
print("N  Eq  Adv Inv Rec Cash Debt Pay Sal Soc Div Cap  RE   NI   Detail IS")
print("-" * 72)

# Ecritures: une ligne = une ligne du tableau du guide
TABLE = (
    "1   +240           +160                      +400",
    "2                  +200  +200",
    "3   N/A: no entry",
    "4        +60      -60",
    "5        -60            +90                      -150  Purchase of merchandise",
    "6             +120 +100                           +220  Sales revenue",
    "7                  -15                             -15   Rent expense",
    "8                  -50       -50",
    "9             -80  +80",
    "10                           +40                 -40   Salaries expense",
    "10                                +20              -20   Social charges expense",
    "11                 -8                              -8    Interest expense",
    "12  -30                                             -30   Depreciation expense",
    "13                                     +10    -10",
    "14        +60                                       +60   Change in inventory",
)

for line in TABLE:
    print(line)

print("-" * 72)
print("End 210   0  60  40  407  200  40  40  20  10  400  -10  17")
print("")
print("Assets 717 = Liabilities 310 + Equity 407")
print("")
print("Part I: six mistakes that cost points")
print("(slide 23)")
print("")
print("X Recording a promise")
print("  Order/contract, nothing exchanged: no entry.")
print("  Write the number and N/A.")
print("")
print("X Expensing an advance")
print("  Cash paid before delivery = asset")
print("  (Advances to suppliers) until goods arrive.")
print("")
print("X Miscounting sale entries")
print("  Perpetual: revenue + cost of goods sold.")
print("  Periodic: revenue only.")
print("")
print("X Crediting the asset for depreciation")
print("  Use Accumulated depreciation; keep")
print("  original cost on the books.")
print("")
print("X Calling dividends an expense")
print("  Dividends reduce retained earnings.")
print("  Never on the income statement.")
print("")
print("X Leaving the grader guessing")
print("  Tick your method, number every transaction,")
print("  do not switch method halfway.")
