import os
import matplotlib.pyplot as plt
import pandas as pd


def load_data(filename):
    """Load and validate financial data from a CSV file."""

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    try:
        data = pd.read_csv(filename)
    except Exception as error:
        raise ValueError(f"Could not read CSV file: {error}")

    required_columns = {"month", "revenue", "expenses"}

    if not required_columns.issubset(data.columns):
        missing_columns = required_columns - set(data.columns)
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    if data.empty:
        raise ValueError("The CSV file contains no data.")

    data["revenue"] = pd.to_numeric(
        data["revenue"],
        errors="coerce"
    )

    data["expenses"] = pd.to_numeric(
        data["expenses"],
        errors="coerce"
    )

    if data["revenue"].isna().any():
        raise ValueError("Revenue contains invalid or missing values.")

    if data["expenses"].isna().any():
        raise ValueError("Expenses contains invalid or missing values.")

    if (data["revenue"] < 0).any():
        raise ValueError("Revenue cannot be negative.")

    if (data["expenses"] < 0).any():
        raise ValueError("Expenses cannot be negative.")

    if data["month"].isna().any():
        raise ValueError("Month contains missing values.")

    return data.to_dict("records")


def calculate_profit(revenue, expenses):
    """Calculate net profit."""

    return revenue - expenses


def calculate_profit_margin(revenue, profit):
    """Calculate profit margin as a percentage."""

    if revenue == 0:
        return 0

    return (profit / revenue) * 100


def calculate_expense_ratio(revenue, expenses):
    """Calculate expenses as a percentage of revenue."""

    if revenue == 0:
        return 0

    return (expenses / revenue) * 100


def calculate_risk_level(profit_margin, revenue_growth, expense_ratio):
    """Classify financial risk based on key financial indicators."""

    if (
        profit_margin >= 20
        and revenue_growth >= 10
        and expense_ratio < 80
    ):
        return "Low Risk"

    elif (
        profit_margin >= 10
        and revenue_growth >= 0
        and expense_ratio < 90
    ):
        return "Medium Risk"

    else:
        return "High Risk"


def calculate_revenue_growth(first_revenue, last_revenue):
    """Calculate revenue growth as a percentage."""

    if first_revenue == 0:
        return 0

    return ((last_revenue - first_revenue) / first_revenue) * 100


def calculate_monthly_profit(data):
    """Calculate detailed profitability for each month."""

    monthly_data = []

    for row in data:
        profit = calculate_profit(
            row["revenue"],
            row["expenses"]
        )

        profit_margin = calculate_profit_margin(
            row["revenue"],
            profit
        )

        expense_ratio = calculate_expense_ratio(
            row["revenue"],
            row["expenses"]
        )

        monthly_data.append({
            "month": row["month"],
            "revenue": row["revenue"],
            "expenses": row["expenses"],
            "profit": profit,
            "profit_margin": profit_margin,
            "expense_ratio": expense_ratio
        })

    return monthly_data


def analyze_monthly_data(data):
    """Analyze monthly financial performance."""

    monthly_data = calculate_monthly_profit(data)

    best_month = max(
        monthly_data,
        key=lambda row: row["profit"]
    )

    worst_month = min(
        monthly_data,
        key=lambda row: row["profit"]
    )

    total_revenue = sum(row["revenue"] for row in data)
    total_expenses = sum(row["expenses"] for row in data)

    total_profit = calculate_profit(
        total_revenue,
        total_expenses
    )

    profit_margin = calculate_profit_margin(
        total_revenue,
        total_profit
    )

    expense_ratio = calculate_expense_ratio(
        total_revenue,
        total_expenses
    )

    revenue_growth = calculate_revenue_growth(
        data[0]["revenue"],
        data[-1]["revenue"]
    )

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "expense_ratio": expense_ratio,
        "revenue_growth": revenue_growth,
        "best_month": best_month,
        "worst_month": worst_month
    }


def financial_health(profit_margin):
    """Classify financial performance."""

    if profit_margin >= 20:
        return "Healthy financial performance"

    elif profit_margin >= 10:
        return "Moderate financial performance"

    else:
        return "Financial performance needs attention"


def calculate_health_score(profit_margin, revenue_growth):
    """Calculate a financial health score from 20 to 100."""

    score = 0

    if profit_margin >= 20:
        score += 50

    elif profit_margin >= 10:
        score += 30

    else:
        score += 10

    if revenue_growth >= 20:
        score += 50

    elif revenue_growth >= 0:
        score += 30

    else:
        score += 10

    return score


def create_financial_chart(data, filename="financial_chart.png"):
    """Create a revenue and expenses chart."""

    months = [row["month"] for row in data]
    revenue = [row["revenue"] for row in data]
    expenses = [row["expenses"] for row in data]

    plt.figure(figsize=(10, 6))

    plt.plot(
        months,
        revenue,
        marker="o",
        label="Revenue"
    )

    plt.plot(
        months,
        expenses,
        marker="o",
        label="Expenses"
    )

    plt.title("Monthly Revenue vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()

    return filename


def generate_management_insights(
    revenue_growth,
    profit_margin,
    expense_ratio,
    best_month,
    worst_month,
    risk_level
):
    """Generate management insights from financial indicators."""

    insights = []

    if revenue_growth > 0:
        insights.append(
            "Revenue grew during the analyzed period."
        )
    else:
        insights.append(
            "Revenue declined during the analyzed period."
        )

    if profit_margin >= 20:
        insights.append(
            "Overall profitability is healthy."
        )
    elif profit_margin >= 10:
        insights.append(
            "Overall profitability is moderate."
        )
    else:
        insights.append(
            "Overall profitability needs attention."
        )

    if expense_ratio < 80:
        insights.append(
            "Expenses are well controlled relative to revenue."
        )
    elif expense_ratio < 90:
        insights.append(
            "Expenses require monitoring relative to revenue."
        )
    else:
        insights.append(
            "Expenses are high relative to revenue."
        )

    insights.append(
        f"{best_month} was the strongest month based on net profit."
    )

    insights.append(
        f"{worst_month} was the weakest month based on net profit."
    )

    insights.append(
        f"Current financial risk level is {risk_level}."
    )

    return insights


def main():
    filename = input("Enter CSV filename: ")

    try:
        data = load_data(filename)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    analysis = analyze_monthly_data(data)

    health_score = calculate_health_score(
        analysis["profit_margin"],
        analysis["revenue_growth"]
    )

    risk_level = calculate_risk_level(
        analysis["profit_margin"],
        analysis["revenue_growth"],
        analysis["expense_ratio"]
    )

    print("\nFINANCIAL SUMMARY")
    print("-" * 50)

    print(f"Total Revenue:   ${analysis['total_revenue']:,.2f}")
    print(f"Total Expenses:  ${analysis['total_expenses']:,.2f}")
    print(f"Net Profit:      ${analysis['total_profit']:,.2f}")
    print(f"Profit Margin:   {analysis['profit_margin']:.2f}%")
    print(f"Expense Ratio:   {analysis['expense_ratio']:.2f}%")
    print(f"Revenue Growth:  {analysis['revenue_growth']:.2f}%")

    print("\nMONTHLY PROFITABILITY")
    print("-" * 50)

    for month in calculate_monthly_profit(data):
        print(f"\n{month['month']}")
        print(f"Revenue:        ${month['revenue']:,.2f}")
        print(f"Expenses:       ${month['expenses']:,.2f}")
        print(f"Profit:         ${month['profit']:,.2f}")
        print(f"Profit Margin:  {month['profit_margin']:.2f}%")
        print(f"Expense Ratio:  {month['expense_ratio']:.2f}%")

    print("\nBEST / WORST MONTH")
    print("-" * 50)

    print(f"Best Month:      {analysis['best_month']['month']}")
    print(f"Worst Month:     {analysis['worst_month']['month']}")

    print("\nFINANCIAL HEALTH")
    print("-" * 50)

    print(f"Health Score:    {health_score}/100")
    print(
        f"Assessment:      "
        f"{financial_health(analysis['profit_margin'])}"
    )

    print("\nFINANCIAL RISK")
    print("-" * 50)

    print(f"Risk Level:      {risk_level}")

    print("\nMANAGEMENT INSIGHTS")
    print("-" * 50)

    insights = generate_management_insights(
        analysis["revenue_growth"],
        analysis["profit_margin"],
        analysis["expense_ratio"],
        analysis["best_month"]["month"],
        analysis["worst_month"]["month"],
        risk_level
    )

    for insight in insights:
        print(f"• {insight}")

    chart_file = create_financial_chart(data)

    print("\nCHART")
    print("-" * 50)
    print(f"Financial chart saved as: {chart_file}")


if __name__ == "__main__":
    main()
