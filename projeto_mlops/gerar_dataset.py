import numpy as np
import pandas as pd


def gerar_dataset(
    n_samples: int = 1000, seed: int = 42, proporcao_positivos: float = 0.3
):
    """
    Gera um dataset sintético para análise de crédito (inadimplência).

    Parâmetros:
    ----------
    n_samples : int
        Número de amostras a serem geradas.
    seed : int
        Seed para reprodutibilidade.
    proporcao_positivos : float
        Proporção de casos positivos (inadimplentes).
        Deve estar entre 0.05 e 0.95.

    Retorno:
    -------
    df : pandas.DataFrame
        DataFrame completo com features e target.
    X : pandas.DataFrame
        Apenas as features.
    y : pandas.Series
        Variável target (inadimplente).

    Exemplo:
    --------
    df, X, y = gerar_dataset(n_samples=1000, seed=42, proporcao_positivos=0.3)
    """

    # 🔴 Validação
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError("proporcao_positivos deve estar entre 0.05 e 0.95")

    rng = np.random.default_rng(seed)

    # Define quantidade de positivos
    n_positivos = int(n_samples * proporcao_positivos)
    n_negativos = n_samples - n_positivos

    # Cria target balanceado manualmente
    inadimplente = np.array([1] * n_positivos + [0] * n_negativos)
    rng.shuffle(inadimplente)

    # Features condicionadas ao target
    renda_mensal = np.where(
        inadimplente,
        rng.uniform(1000, 3000, n_samples),
        rng.uniform(3000, 10000, n_samples),
    )

    divida_atual = np.where(
        inadimplente,
        rng.uniform(2000, 15000, n_samples),
        rng.uniform(0, 5000, n_samples),
    )

    historico_pagamentos = np.where(
        inadimplente, rng.integers(0, 5, n_samples), rng.integers(5, 10, n_samples)
    )

    idade = rng.integers(18, 70, n_samples)

    num_dependentes = rng.integers(0, 5, n_samples)

    # DataFrame final
    df = pd.DataFrame(
        {
            "renda_mensal": renda_mensal,
            "divida_atual": divida_atual,
            "historico_pagamentos": historico_pagamentos,
            "idade": idade,
            "num_dependentes": num_dependentes,
            "inadimplente": inadimplente,
        }
    )

    # Separação padrão ML
    X = df.drop(columns="inadimplente")
    y = df["inadimplente"]

    return df, X, y


# Teste rápido
if __name__ == "__main__":
    df, X, y = gerar_dataset(n_samples=2000, proporcao_positivos=0.3)

    print(df.head())
    print("\nDistribuição:\n", y.value_counts(normalize=True))
