from datetime import date

from models.financials import FinancialData
from models.state import ResearchState
from tools.financial_api import FinancialAPI


financial_api = FinancialAPI()


def get_latest_metric(
    metrics: dict,
    metric_name: str,
) -> tuple[float | None, date | None]:

    series = metrics.get(metric_name)

    if not series:
        return None, None
    
    if isinstance(series, list):
        valid_entries = [
            item
            for item in series
            if item.get("period") and item.get("v") is not None
        ]

        if not valid_entries:
            return None, None

        latest = max(
            valid_entries,
            key=lambda item: item["period"]
        )

        return (
            float(latest["v"]),
            date.fromisoformat(latest["period"])
        )
    
    if isinstance(series, (int, float)):
        return float(series), None

    return None, None


def get_fundamentals(state: ResearchState) -> dict:

    if not state.company:
        return {
            "errors": [
                "Cannot retrieve fundamentals: company not resolved"
            ]
        }

    ticker = state.company.ticker

    try:
        response = financial_api.get_basic_financials(ticker)

        metrics = response.get("metric", {})

        pe_ratio, pe_date = get_latest_metric(
            metrics,
            "peTTM",
        )

        pb_ratio, pb_date = get_latest_metric(
            metrics,
            "pb",
        )

        net_margin, margin_date = get_latest_metric(
            metrics,
            "netProfitMarginTTM",
        )

        operating_margin, operating_date = get_latest_metric(
            metrics,
            "operatingMarginTTM",
        )

        debt_to_equity, debt_date = get_latest_metric(
            metrics,
            "totalDebt/totalEquityQuarterly",
        )

        available_dates = [
            d
            for d in [
                pe_date,
                pb_date,
                margin_date,
                operating_date,
                debt_date,
            ]
            if d is not None
        ]

        latest_period = (
            max(available_dates)
            if available_dates
            else None
        )

        financial_data = FinancialData(
            ticker=ticker,
            pe_ratio=pe_ratio,
            pb_ratio=pb_ratio,
            net_margin=net_margin,
            operating_margin=operating_margin,
            debt_to_equity=debt_to_equity,
            latest_period=latest_period,
        )

        return {
            "financial_data": financial_data
        }

    except Exception as e:
        return {
            "errors": [
                f"Fundamental retrieval failed: {str(e)}"
            ]
        }