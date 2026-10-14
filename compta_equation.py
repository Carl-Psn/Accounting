# Comptabilite — equation comptable, methode periodique
# Copier ce fichier sur NumWorks (Python app) pour l'examen.
# Montants en milliers de CU, comme le cas Rameau.

METHOD = "periodic"

# Colonnes (ordre slide 22 du study guide)
COL_KEYS = (
    "eq", "adv", "inv", "rec", "cash",
    "debt", "pay", "sal", "soc", "divp",
    "cap", "re", "ni",
)
COL_SHORT = (
    "Eq", "Adv", "Inv", "Rec", "Ca",
    "Det", "Fourn", "Sal", "Soc", "Div",
    "Cap", "Res", "RN",
)
COL_LABEL = {
    "eq": "Equip(net)",
    "adv": "Avances",
    "inv": "Stock",
    "rec": "Clients",
    "cash": "Caisse",
    "debt": "Emprunt",
    "pay": "Fourn.",
    "sal": "Sal. a payer",
    "soc": "Soc. a payer",
    "divp": "Div. a payer",
    "cap": "Capital",
    "re": "Reserves",
    "ni": "RN",
}

ASSET_KEYS = ("eq", "adv", "inv", "rec", "cash")
LIAB_KEYS = ("debt", "pay", "sal", "soc", "divp")
EQ_KEYS = ("cap", "re", "ni")

balances = {k: 0 for k in COL_KEYS}
rows = []  # list of (num, changes dict, detail)
txn_num = 0


def _f(x):
    if x == 0:
        return ""
    if x == int(x):
        return ("+" if x > 0 else "") + str(int(x))
    s = ("+" if x > 0 else "") + str(round(x, 2))
    return s


def assets_total():
    return sum(balances[k] for k in ASSET_KEYS)


def liab_total():
    return sum(balances[k] for k in LIAB_KEYS)


def equity_total():
    return sum(balances[k] for k in EQ_KEYS)


def check_balance():
    a = assets_total()
    r = liab_total() + equity_total()
    return abs(a - r) < 0.001, a, r


def apply_row(changes, detail="", num=None):
    global txn_num
    if num is None:
        txn_num += 1
        num = txn_num
    elif num > txn_num:
        txn_num = num
    for k, v in changes.items():
        balances[k] = balances.get(k, 0) + v
    rows.append((num, dict(changes), detail))
    ok, a, r = check_balance()
    if not ok:
        print("ATTENTION: equation desequilibree!")
        print("  Actif", a, " vs Passif+CP", r)
    return num


def row_na(detail="N/A: no entry"):
    return apply_row({}, detail)


def read_amount(prompt, default=None):
    while True:
        if default is not None:
            s = input(prompt + " [" + str(default) + "]: ")
            if s.strip() == "":
                return float(default)
        else:
            s = input(prompt + ": ")
        try:
            return float(s.replace(",", "."))
        except ValueError:
            print("Nombre invalide.")


def read_amount_nonneg(prompt, default=None):
    while True:
        v = read_amount(prompt, default)
        if v >= 0:
            return v
        print("Entrez un montant >= 0.")


# --- Templates d'evenements (style Rameau, methode periodique) ---

def ev_capital():
    eq = read_amount_nonneg("Valeur equipement / immo")
    cash = read_amount_nonneg("Apport cash")
    cap = eq + cash
    apply_row({"eq": eq, "cash": cash, "cap": cap}, "")


def ev_loan():
    m = read_amount_nonneg("Montant emprunt")
    apply_row({"cash": m, "debt": m}, "")


def ev_order_only():
    row_na()


def ev_advance_supplier():
    m = read_amount_nonneg("Acompte paye au fournisseur")
    apply_row({"adv": m, "cash": -m}, "")


def ev_merchandise_received():
    total = read_amount_nonneg("Prix total marchandises recues")
    adv_clear = read_amount_nonneg(
        "Acompte impute (advances)",
        default=min(balances["adv"], total) if balances["adv"] else 0,
    )
    if adv_clear > total:
        adv_clear = total
    payable = total - adv_clear
    ch = {"adv": -adv_clear, "ni": -total}
    if payable:
        ch["pay"] = payable
    apply_row(ch, "-" + str(int(total) if total == int(total) else total) + " Purchase")


def ev_sale_periodic():
    cash = read_amount_nonneg("Encaissement cash")
    credit = read_amount_nonneg("A credit (creances clients)")
    rev = cash + credit
    apply_row(
        {"cash": cash, "rec": credit, "ni": rev},
        "+" + str(int(rev) if rev == int(rev) else rev) + " Sales revenue",
    )


def ev_rent():
    m = read_amount_nonneg("Loyer paye")
    apply_row({"cash": -m, "ni": -m}, "-" + str(int(m) if m == int(m) else m) + " Rent expense")


def ev_pay_supplier():
    m = read_amount_nonneg("Paiement fournisseur")
    apply_row({"pay": -m, "cash": -m}, "")


def ev_collect_customer():
    m = read_amount_nonneg("Encaissement client")
    apply_row({"rec": -m, "cash": m}, "")


def ev_personnel_accrual():
    sal = read_amount_nonneg("Salaires (charges, non payes)")
    soc = read_amount_nonneg("Charges sociales (non payees)")
    n = txn_num + 1
    apply_row({"sal": sal, "ni": -sal}, "-" + str(int(sal) if sal == int(sal) else sal) + " Salaries", num=n)
    apply_row({"soc": soc, "ni": -soc}, "-" + str(int(soc) if soc == int(soc) else soc) + " Social charges", num=n)


def ev_interest_paid():
    m = read_amount_nonneg("Interets payes")
    apply_row({"cash": -m, "ni": -m}, "-" + str(int(m) if m == int(m) else m) + " Interest expense")


def ev_depreciation():
    m = read_amount_nonneg("Dotation amortissement (equip net)")
    apply_row({"eq": -m, "ni": -m}, "-" + str(int(m) if m == int(m) else m) + " Depreciation")


def ev_depreciation_auto():
    cost = read_amount_nonneg("Cout equipement")
    years = read_amount_nonneg("Duree (annees)")
    if years <= 0:
        print("Duree invalide.")
        return
    m = cost / years
    print("Amortissement:", m)
    apply_row({"eq": -m, "ni": -m}, "-" + str(int(m) if m == int(m) else m) + " Depreciation")


def ev_dividend_declared():
    m = read_amount_nonneg("Dividende declare")
    apply_row({"divp": m, "re": -m}, "")


def ev_ending_inventory():
    m = read_amount_nonneg("Inventaire fin de periode")
    apply_row(
        {"inv": m, "ni": m},
        "+" + str(int(m) if m == int(m) else m) + " Change in inventory",
    )


EVENTS = (
    ("1", "Apport capital (equip + cash)", ev_capital),
    ("2", "Emprunt bancaire", ev_loan),
    ("3", "Commande sans echange (N/A)", ev_order_only),
    ("4", "Acompte fournisseur (avances)", ev_advance_supplier),
    ("5", "Reception marchandises (periodic)", ev_merchandise_received),
    ("6", "Vente (periodic, revenue seul)", ev_sale_periodic),
    ("7", "Loyer paye", ev_rent),
    ("8", "Paiement fournisseur", ev_pay_supplier),
    ("9", "Encaissement client", ev_collect_customer),
    ("10", "Personnel (salaires + soc, a payer)", ev_personnel_accrual),
    ("11", "Interets payes", ev_interest_paid),
    ("12", "Amortissement (montant)", ev_depreciation),
    ("12a", "Amortissement lineaire auto", ev_depreciation_auto),
    ("13", "Dividende declare", ev_dividend_declared),
    ("14", "Inventaire fin (periodic)", ev_ending_inventory),
)


def print_menu():
    print("\n--- Evenements ---")
    for code, label, _ in EVENTS:
        print(code, label)
    print("T  Tableau complet")
    print("C  Tableau compact (NumWorks)")
    print("S  Soldes finaux")
    print("D  Demo Rameau (test)")
    print("U  Derniere ecriture annuler")
    print("R  Reinitialiser")
    print("Q  Quitter")


def format_compact(changes, detail=""):
    bits = []
    for k in COL_KEYS:
        v = changes.get(k, 0)
        if v:
            bits.append(COL_LABEL[k] + _f(v))
    line = " | ".join(bits) if bits else "(vide)"
    if detail:
        line += " — " + detail
    return line


def print_row_compact(num, changes, detail=""):
    print("#" + str(num) + ": " + format_compact(changes, detail))


def print_table_compact():
    for num, ch, det in rows:
        print_row_compact(num, ch, det)
    print("#Fin: " + format_compact(balances))


def print_row(num, changes, detail):
    parts = [str(num).ljust(2)]
    for k in COL_KEYS:
        parts.append(_f(changes.get(k, 0)).rjust(4))
    line = " ".join(parts)
    if detail:
        line += "  " + detail
    print(line)


def print_table_header():
    print("N ", " ".join(c.rjust(4) for c in COL_SHORT))
    print("-" * 72)


def print_table(from_n=1):
    print_table_header()
    for num, ch, det in rows:
        if num >= from_n:
            print_row(num, ch, det)
    print("--- Fin ---")
    print_final_row()


def print_final_row():
    ch = dict(balances)
    print_row("E", ch, "End")


def print_summary():
    ok, a, r = check_balance()
    print("\n=== Soldes ===")
    for k, short in zip(COL_KEYS, COL_SHORT):
        v = balances[k]
        if v != 0:
            print(short + ":", v)
    print("Total actif:", assets_total())
    print("Total passif:", liab_total())
    print("Cap + Res + RN:", equity_total())
    print("Equation OK:" if ok else "DESEQUILIBRE:", ok)


def undo_last():
    global txn_num
    if not rows:
        print("Rien a annuler.")
        return
    last_n = rows[-1][0]
    while rows and rows[-1][0] == last_n:
        _, ch, _ = rows.pop()
        for k, v in ch.items():
            balances[k] -= v
    txn_num = rows[-1][0] if rows else 0
    print("Annule ecriture(s) n", last_n)


def reset_all():
    global txn_num
    for k in balances:
        balances[k] = 0
    rows.clear()
    txn_num = 0
    print("Reinitialise.")


def run_demo_rameau():
    """Cas Rameau (study guide) — verification."""
    reset_all()
    apply_row({"eq": 240, "cash": 160, "cap": 400}, "")
    apply_row({"cash": 200, "debt": 200}, "")
    row_na()
    apply_row({"adv": 60, "cash": -60}, "")
    apply_row({"adv": -60, "pay": 90, "ni": -150}, "-150 Purchase")
    apply_row({"rec": 120, "cash": 100, "ni": 220}, "+220 Sales revenue")
    apply_row({"cash": -15, "ni": -15}, "-15 Rent expense")
    apply_row({"pay": -50, "cash": -50}, "")
    apply_row({"rec": -80, "cash": 80}, "")
    n = 10
    apply_row({"sal": 40, "ni": -40}, "-40 Salaries", num=n)
    apply_row({"soc": 20, "ni": -20}, "-20 Social charges", num=n)
    apply_row({"cash": -8, "ni": -8}, "-8 Interest expense")
    apply_row({"eq": -30, "ni": -30}, "-30 Depreciation")
    apply_row({"divp": 10, "re": -10}, "")
    apply_row({"inv": 60, "ni": 60}, "+60 Change in inventory")
    return check_balance()


def main():
    print("Equation comptable —", METHOD)
    print("Montants en milliers CU")
    ev_map = {code: fn for code, _, fn in EVENTS}
    while True:
        print_menu()
        choice = input("Choix: ").strip()
        if not choice:
            continue
        c = choice.lower()
        if c in ("q", "quit"):
            break
        if c == "t":
            print_table()
            continue
        if c == "c":
            print_table_compact()
            continue
        if c == "d":
            run_demo_rameau()
            ok, a, _ = check_balance()
            print("Demo chargee. Actif", a, "OK" if ok else "ERREUR")
            print_table_compact()
            continue
        if c == "s":
            print_summary()
            continue
        if c == "u":
            undo_last()
            continue
        if c == "r":
            reset_all()
            continue
        fn = ev_map.get(choice) or ev_map.get(c.upper())
        if fn:
            try:
                fn()
                if rows:
                    n, ch, det = rows[-1]
                    # Afficher toutes les lignes ajoutees (ex. personnel = 2 lignes)
                    i = len(rows) - 1
                    while i > 0 and rows[i - 1][0] == n:
                        i -= 1
                    for j in range(i, len(rows)):
                        print_row_compact(*rows[j])
                    ok, _, _ = check_balance()
                    print("Eq.", "OK" if ok else "!!")
            except (KeyboardInterrupt, EOFError):
                print("\nAnnule.")
        else:
            print("Choix inconnu.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        ok, a, r = run_demo_rameau()
        expected_a = 717
        assert ok and abs(a - expected_a) < 0.001, (ok, a, r, balances)
        print("Test Rameau OK — actif", a, "RN", balances["ni"])
        print_table()
    else:
        main()
