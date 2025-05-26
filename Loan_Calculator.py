def is_valid_loan(loan):
    try:
        loan['principal'] = float(loan['principal'])
        loan['annual_rate'] = float(loan['annual_rate'])
        loan['term_years'] = int(loan['term_years'])
        loan['escalation_rate'] = float(loan.get('escalation_rate', 0.0))

        if loan['principal'] <= 0:
            return "Error: Principal amount must be positive."
        if loan['annual_rate'] <= 0:
            return "Error: Annual interest rate must be greater than zero."
        if loan['term_years'] <= 0:
            return "Error: Loan term must be positive."
        return True
    except (ValueError, TypeError):
        return "Error: Invalid input type (must be numeric)."

def calculate_monthly_payment(P, r, n):
    return P * (r * (1 + r)**n) / ((1 + r)**n - 1)

def generate_schedule(loan):
    P = loan['principal']
    r = loan['annual_rate'] / 12 / 100
    n = loan['term_years'] * 12
    escalation_rate = loan.get('escalation_rate', 0.0)
    payment_year_1 = calculate_monthly_payment(P, r, n)

    total_interest = 0
    balance = P
    month = 1

    print(f"\nLoan (Principal: ${P:.2f}, Rate: {loan['annual_rate']}%, Term: {loan['term_years']} years, Escalation: {escalation_rate*100:.1f}%)")

    for year in range(loan['term_years']):
        current_payment = payment_year_1 * ((1 + escalation_rate) ** year)
        for m in range(12):
            if month > n:
                break
            interest = balance * r
            principal = current_payment - interest
            balance -= principal
            balance = max(balance, 0)
            total_interest += interest
            print(f"Month {month}: Payment: ${current_payment:.2f}, Interest: ${interest:.2f}, Principal: ${principal:.2f}, Balance: ${balance:.2f}")
            month += 1

    print(f"Total Interest Paid: ${total_interest:.2f}\n")

def prompt_user_for_loan():
    print("Enter loan details:")
    principal = input("Principal amount: ")
    annual_rate = input("Annual interest rate (%): ")
    term_years = input("Loan term (years): ")
    escalation = input("Escalation rate (% per year, optional): ")

    loan = {
        "principal": principal,
        "annual_rate": annual_rate,
        "term_years": term_years,
        "escalation_rate": escalation if escalation else 0.0
    }

    return loan


if __name__ == "__main__":
    print("=== Loan Repayment Schedule Calculator ===")

    while True:
        loan = prompt_user_for_loan()
        validation = is_valid_loan(loan)
        if validation == True:
            generate_schedule(loan)
        else:
            print(validation)
        again = input("Do you want to calculate another loan? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break
