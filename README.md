
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
Não deve ser usado em produção sem validação adicional