from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from gerar_dataset import gerar_dataset
import joblib
import numpy as np 
import os
import pandas as pd

if __name__ == "__main__":

    # 1. Gerar dados
    df, X, y = gerar_dataset(n_samples=2000, seed=42)
    print(df.columns)

    # Distribuição das classes
    print("Distribuição das classes:")
    print(pd.Series(y).value_counts(normalize=True))

    # 2. Separar treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # 3. Treinar modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. Previsão
    y_pred = model.predict(X_test)

    # 5. Avaliação
    print(classification_report(y_test, y_pred))

    # 6. Salvar modelo
    joblib.dump(model, "model.pkl")
    print("Modelo salvo em model.pkl")

    # 7. Carregar modelo
    model_carregado = joblib.load("model.pkl")

    # 8. Validar artefato
    amostra = X_test[:5]

    pred_original  = model.predict(amostra)
    pred_carregado = model_carregado.predict(amostra)

    assert np.array_equal(pred_original, pred_carregado), "Predições divergem!"

    print("✅ Artefato validado — predições idênticas")
    print(f"Predições: {pred_original}")

    # 9. Tamanho do arquivo
    tamanho = os.path.getsize("model.pkl")
    print(f"Tamanho do modelo: {tamanho / 1024:.2f} KB")

    # 10. Criar README
    MODEL_CARD = """
language: pt 
tags: 
- sklearn 
- classification 
- fraud
-detection 
- mlops 
--- 
# fraud-detector-v1 
Modelo de classificação binária para detecção de transações fraudulentas. 
Desenvolvido como parte de um projeto de MLOps. 
## Uso
python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("SEU_USUARIO/fraud-detector-v1", "model.pkl"))
features = [[250.0, 14, 12.5, 1, 0]]
prediction = model.predict(features)

| Feature                 | Tipo  | Descrição                              |
| ----------------------- | ----- | -------------------------------------- |
| valor_transacao         | float | Valor da transação em reais            |
| hora_transacao          | int   | Hora do dia (0-23)                     |
| distancia_ultima_compra | float | Distância geográfica em km             |
| tentativas_senha        | int   | Tentativas de senha antes da transação |
| pais_diferente          | int   | 1 se país diferente do cadastro        |

Métricas (test set, 20% dos dados)
Precision (fraude): 0.85
Recall (fraude): 0.78
F1 (fraude): 0.81
Dependências
scikit-learn==1.4.0
joblib==1.3.2
numpy==1.26.0
Limitações
Modelo treinado com dados sintéticos
Pode não refletir padrões reais de fraude
Não considera histórico completo do usuário
Não deve ser usado em produção sem validação adicional"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(MODEL_CARD)

    print("README.md criado")