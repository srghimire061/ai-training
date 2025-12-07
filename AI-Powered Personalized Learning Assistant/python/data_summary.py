import pandas as pd
import matplotlib.pyplot as plt

# Load dataset using correct relative path
df = pd.read_csv("../dataset/employee_learning_data.csv")

# -----------------------------
# 1. Completion Rate by Department
# -----------------------------
dept = df.groupby('department')['completion_status'].apply(lambda x: (x == "Completed").mean())

plt.figure(figsize=(8,5))
plt.bar(dept.index, dept.values)  # no colors specified
plt.title("Completion Rate by Department")
plt.xticks(rotation=45)
plt.ylabel("Completion Rate")
plt.tight_layout()
plt.show()

# -----------------------------
# 2. Module Type Distribution
# -----------------------------
mod = df['module_type'].value_counts()

plt.figure(figsize=(7,5))
plt.bar(mod.index, mod.values)
plt.title("Module Type Distribution")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Time Spent vs Quiz Score
# -----------------------------
quiz = df[df['score'].notna()]

plt.figure(figsize=(7,5))
plt.scatter(quiz['time_spent_minutes'], quiz['score'])
plt.title("Time Spent vs Quiz Score")
plt.xlabel("Time Spent (minutes)")
plt.ylabel("Quiz Score")
plt.tight_layout()
plt.show()
