import pytest

from project import (
    calculate_health_score,
    calculate_monthly_profit,
    calculate_profit,
    calculate_profit_margin,
    calculate_revenue_growth,
    calculate_risk_level,
    create_financial_chart,
    financial_health,
    generate_management_insights,
    load_data
)


def test_calculate_profit():
    assert calculate_profit(1000, 700) == 300
    assert calculate_profit(5000, 2000) == 3000


def test_calculate_profit_margin():
    assert calculate_profit_margin(1000, 200) == 20
    assert calculate_profit_margin(2000, 500) == 25
    assert calculate_profit_margin(0, 100) == 0


def test_calculate_revenue_growth():
    assert calculate_revenue_growth(100, 120) == 20
    assert calculate_revenue_growth(1000, 1500) == 50
    assert calculate_revenue_growth(0, 100) == 0


def test_calculate_monthly_profit():
    data = [
        {
            "month": "January",
            "revenue": 1000,
            "expenses": 700
        },
        {
            "month": "February",
            "revenue": 2000,
            "expenses": 1200
        }
    ]

    result = calculate_monthly_profit(data)

    assert result[0]["month"] == "January"
    assert result[0]["profit"] == 300

    assert result[1]["month"] == "February"
    assert result[1]["profit"] == 800


def test_financial_health():
    assert financial_health(25) == "Healthy financial performance"
    assert financial_health(15) == "Moderate financial performance"
    assert financial_health(5) == "Financial performance needs attention"


def test_calculate_health_score():
    assert calculate_health_score(25, 30) == 100
    assert calculate_health_score(15, 10) == 60
    assert calculate_health_score(5, -10) == 20


def test_load_data_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("file_that_does_not_exist.csv")


def test_load_data_missing_column(tmp_path):
    file = tmp_path / "invalid.csv"

    file.write_text(
        "month,revenue\n"
        "January,1000\n"
    )

    with pytest.raises(ValueError):
        load_data(str(file))


def test_load_data_invalid_revenue(tmp_path):
    file = tmp_path / "invalid_revenue.csv"

    file.write_text(
        "month,revenue,expenses\n"
        "January,not_a_number,700\n"
    )

    with pytest.raises(ValueError):
        load_data(str(file))


def test_monthly_profit_margin():
    data = [
        {
            "month": "January",
            "revenue": 1000,
            "expenses": 700
        },
        {
            "month": "February",
            "revenue": 2000,
            "expenses": 1200
        }
    ]

    result = calculate_monthly_profit(data)

    assert result[0]["profit_margin"] == 30
    assert result[1]["profit_margin"] == 40


def test_calculate_risk_level():
    assert calculate_risk_level(25, 30, 70) == "Low Risk"
    assert calculate_risk_level(15, 5, 85) == "Medium Risk"
    assert calculate_risk_level(5, -10, 95) == "High Risk"


def test_create_financial_chart(tmp_path):
    data = [
        {
            "month": "January",
            "revenue": 1000,
            "expenses": 700
        },
        {
            "month": "February",
            "revenue": 2000,
            "expenses": 1200
        }
    ]

    output_file = tmp_path / "financial_chart.png"

    result = create_financial_chart(
        data,
        str(output_file)
    )

    assert result == str(output_file)
    assert output_file.exists()


def test_generate_management_insights():
    insights = generate_management_insights(
        70,
        23,
        77,
        "December",
        "March",
        "Low Risk"
    )

    assert len(insights) == 6
    assert "Revenue grew during the analyzed period." in insights
    assert "Overall profitability is healthy." in insights
    assert "Expenses are well controlled relative to revenue." in insights
    assert "December was the strongest month based on net profit." in insights
    assert "March was the weakest month based on net profit." in insights
    assert "Current financial risk level is Low Risk." in insights
