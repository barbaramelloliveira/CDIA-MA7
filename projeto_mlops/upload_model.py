from huggingface_hub import HfApi
import sklearn
import joblib as jl

api = HfApi()

repo_id = "Barbz2605/fraud-detector-v1"

# 1. Criar requirements.txt dinâmico
requirements = f"""scikit-learn=={sklearn.__version__}
joblib=={jl.__version__}
"""

with open("requirements.txt", "w") as f:
    f.write(requirements)

print("requirements.txt criado")

# 2. Upload dos arquivos
for filename in ["model.pkl", "README.md", "requirements.txt"]:
    api.upload_file(
        path_or_fileobj=filename,
        path_in_repo=filename,
        repo_id=repo_id,
        repo_type="model",
        commit_message=f"Add {filename}"
    )
    print(f"✅ {filename} publicado")

print(f"\nRepositório: https://huggingface.co/{repo_id}")