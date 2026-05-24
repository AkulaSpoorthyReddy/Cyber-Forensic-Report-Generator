import pandas as pd
import numpy as np

print("Generating Synthetic Forensic Evidence...")

# 1. Create 100 rows of fake malware data
n_rows = 100

# 2. Define the exact columns your app is looking for
data = {
    'Class': np.random.choice([1, 2, 3, 4, 5], n_rows), # 1: Adware, 2: Banking, etc.
    'transact': np.random.randint(0, 500, n_rows),
    'bind_service': np.random.randint(0, 100, n_rows),
    'on_bind': np.random.randint(0, 50, n_rows),
    'attach_interface': np.random.randint(0, 200, n_rows),
    'get_calling_uid': np.random.randint(0, 300, n_rows),
    'read_phone_state': np.random.randint(0, 50, n_rows),
}

# Add 10 more random "system call" columns to make the RAG engine work well
for i in range(10):
    data[f'sys_call_{i}'] = np.random.randint(0, 100, n_rows)

# 3. Create the DataFrame and save it exactly how your app expects it
df = pd.DataFrame(data)
df.to_csv("malware_data.csv", index=False)

print("✅ Success! 'malware_data.csv' has been created in your folder.")
print("You can now run: streamlit run app.py")