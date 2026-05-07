# CDS Brazil Data Scraper

![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Scraper para coletar dados históricos de Credit Default Swaps (CDS) do Brasil a partir do Investing.com, com análise exploratória integrada.

## Funcionalidades

- Coleta dados de múltiplos prazos de CDS (1, 2, 3, 4, 5, 7 e 10 anos)
- Combina os dados em um único DataFrame indexado por data
- Gera gráficos de séries temporais e matriz de correlação
- Opção de salvar gráficos em arquivo via `--save-plots`

## Pré-requisitos

- Python >= 3.10
- pip

## Instalação

```bash
git clone https://github.com/peuserrano/cds-brazil-scraper.git
cd cds-brazil-scraper

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Uso

Coleta todos os prazos e exibe os gráficos na tela:

```bash
python main.py
```

Coleta apenas os prazos de 1 e 5 anos:

```bash
python main.py --tenors cds-1-year cds-5-years
```

Coleta todos os prazos e salva os gráficos em `output/`:

```bash
python main.py --save-plots
```

## Desenvolvimento

```bash
pip install -r requirements-dev.txt
pytest
```

## Limitações

- O Investing.com pode bloquear requisições automatizadas. Se a coleta falhar com erro HTTP 403, o site pode ter alterado sua política de acesso.
- A estrutura da tabela HTML pode mudar sem aviso prévio, exigindo atualização do parser.
- Este projeto é para fins educacionais e de pesquisa. Verifique os termos de uso do Investing.com antes de utilizar os dados.

## Contribuições

Contribuições são bem-vindas. Abra uma issue ou envie um pull request.

## Licença

MIT — veja [LICENSE](LICENSE).
