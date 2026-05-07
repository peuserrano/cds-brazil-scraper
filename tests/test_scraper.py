from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.cds_scraper import CDSDataScraper

HEADERS = {"user-agent": "test-agent"}


class TestCDSDataScraper:
    def test_get_combined_data_empty(self):
        scraper = CDSDataScraper(HEADERS)
        result = scraper.get_combined_data()
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_get_combined_data_returns_dataframe(self):
        scraper = CDSDataScraper(HEADERS)
        df = pd.DataFrame({"cds-5-years": [100.0, 101.0]})
        df.index = pd.to_datetime(["2024-01-01", "2024-01-02"])
        scraper._dfs.append(df)

        result = scraper.get_combined_data()
        assert "cds-5-years" in result.columns
        assert len(result) == 2

    def test_get_combined_data_multiple_tenors(self):
        scraper = CDSDataScraper(HEADERS)
        for tenor in ["cds-1-year", "cds-5-years"]:
            df = pd.DataFrame({tenor: [100.0]})
            df.index = pd.to_datetime(["2024-01-01"])
            scraper._dfs.append(df)

        result = scraper.get_combined_data()
        assert set(result.columns) == {"cds-1-year", "cds-5-years"}

    @patch("src.cds_scraper.requests.get")
    def test_fetch_data_http_error(self, mock_get):
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("403")
        mock_get.return_value = mock_response

        scraper = CDSDataScraper(HEADERS)
        scraper.fetch_data("cds-5-years")

        assert scraper._dfs == []

    @patch("src.cds_scraper.time.sleep", return_value=None)
    @patch("src.cds_scraper.requests.get")
    def test_fetch_data_unexpected_error(self, mock_get, _mock_sleep):
        mock_get.side_effect = Exception("connection error")

        scraper = CDSDataScraper(HEADERS)
        scraper.fetch_data("cds-5-years")

        assert scraper._dfs == []
