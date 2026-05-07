import argparse
import logging

from src.cds_scraper import CDSDataScraper
from src.eda import correlation_matrix, plot_cds_data

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    )
}

CDS_TENORS = [
    "cds-1-year",
    "cds-2-years",
    "cds-3-years",
    "cds-4-years",
    "cds-5-years",
    "cds-7-years",
    "cds-10-years",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coleta e analisa dados de CDS do Brasil.")
    parser.add_argument(
        "--tenors",
        nargs="+",
        default=CDS_TENORS,
        metavar="TENOR",
        help="Prazos de CDS a coletar (ex: cds-1-year cds-5-years). Padrão: todos.",
    )
    parser.add_argument(
        "--save-plots",
        action="store_true",
        help="Salva os gráficos em output/ em vez de exibir na tela.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    scraper = CDSDataScraper(HEADERS)
    for tenor in args.tenors:
        scraper.fetch_data(tenor)

    base_cds = scraper.get_combined_data()

    if base_cds.empty:
        logging.error("Nenhum dado coletado. Encerrando.")
        raise SystemExit(1)

    print(base_cds.describe())

    if args.save_plots:
        plot_cds_data(base_cds, save_path="output/cds_series.png")
        correlation_matrix(base_cds, save_path="output/cds_correlation.png")
    else:
        plot_cds_data(base_cds)
        correlation_matrix(base_cds)
