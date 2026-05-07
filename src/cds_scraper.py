import logging
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://br.investing.com/rates-bonds/brazil-{tenor}-usd-historical-data"


class CDSDataScraper:
    """Coleta dados históricos de CDS do Brasil a partir do Investing.com."""

    def __init__(self, headers: dict) -> None:
        self.headers = headers
        self._dfs: list[pd.DataFrame] = []

    def fetch_data(self, tenor: str) -> None:
        """Busca e armazena os dados do CDS para o prazo especificado.

        Args:
            tenor: Identificador do prazo (ex: 'cds-5-years').
        """
        url = BASE_URL.format(tenor=tenor)

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, features="lxml")
            table = soup.find_all("table")[0]

            df = pd.read_html(str(table))[0][["Último", "Data"]]
            df = df.set_index("Data")
            df.index = pd.to_datetime(df.index, format="%d.%m.%Y")
            df.columns = [tenor]

            self._dfs.append(df)
            logger.info("Dados coletados com sucesso para %s", tenor)

        except requests.HTTPError as e:
            logger.error("Erro HTTP ao coletar %s: %s", tenor, e)
        except Exception as e:
            logger.error("Erro inesperado ao coletar %s: %s", tenor, e)

        time.sleep(2)

    def get_combined_data(self) -> pd.DataFrame:
        """Combina todos os DataFrames coletados em um único DataFrame.

        Returns:
            DataFrame com todos os prazos de CDS coletados, ou vazio se nenhum.
        """
        if not self._dfs:
            logger.warning("Nenhum dado foi coletado.")
            return pd.DataFrame()

        return pd.concat(self._dfs, axis=1)
