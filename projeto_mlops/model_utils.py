from huggingface_hub import hf_hub_download
import joblib
import time

def load_model(
    repo_id: str,
    filename: str = "model.pkl",
    force_download: bool = False
):
    inicio = time.time()

    local_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        force_download=force_download
    )

    model = joblib.load(local_path)

    fim = time.time()

    origem = "Hub (forçado)" if force_download else "cache/local automático"

    print(f"✅ Modelo carregado de: {origem}")
    print(f"📁 Caminho: {local_path}")
    print(f"⏱️ Tempo: {fim - inicio:.4f} segundos\n")

    return model


if __name__ == "__main__":
    repo_id = "Barbz2605/fraud-detector-v1"

    print("🔹 Primeira chamada (download):")
    load_model(repo_id)

    print("🔹 Segunda chamada (cache):")
    load_model(repo_id)

    print("🔹 Terceira chamada (force_download=True):")
    load_model(repo_id, force_download=True)