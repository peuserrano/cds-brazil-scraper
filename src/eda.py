import matplotlib.pyplot as plt
import seaborn as sns


def plot_cds_data(df, save_path: str | None = None) -> None:
    """Plota a evolução dos spreads de CDS ao longo do tempo."""
    plt.figure(figsize=(12, 8))

    for column in df.columns:
        plt.plot(df.index, df[column], label=column)

    plt.title("Evolução dos Spreads de CDS ao longo do tempo")
    plt.xlabel("Período")
    plt.ylabel("Spread (bps)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

    plt.close()


def correlation_matrix(df, save_path: str | None = None) -> None:
    """Plota a matriz de correlação dos spreads de CDS."""
    corr_matrix = df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Matriz de Correlação dos spreads de CDS")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

    plt.close()
