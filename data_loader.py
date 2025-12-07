

## **5️⃣ data_loader.py**
import kagglehub
import os

def download_dataset():
    path = kagglehub.dataset_download("ayoubcherguelaine/company-documents-dataset")
    os.makedirs("data", exist_ok=True)
    # Move/Extract dataset to data folder
    print("Dataset downloaded at:", path)
    return path

if __name__ == "__main__":
    download_dataset()
