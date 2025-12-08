import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded datasets
learning_data_path = '../dataset/employee_learning_data.csv'

# Read the CSV files to examine their contents
learning_data = pd.read_csv(learning_data_path)

# Normalize the relevant columns for scoring
learning_data['time_spent_minutes'] = learning_data['time_spent_minutes'].fillna(0)
learning_data['score'] = learning_data['score'].fillna(0)

# Create a scoring formula based on time spent, score, and learning style match
# Example weights (adjust as necessary):
time_weight = 0.3
score_weight = 0.4
learning_style_weight = 0.3

# Normalize time_spent_minutes (between 0 and 100 scale)
learning_data['time_spent_normalized'] = (learning_data['time_spent_minutes'] - learning_data['time_spent_minutes'].min()) / (learning_data['time_spent_minutes'].max() - learning_data['time_spent_minutes'].min()) * 100

# Normalize score (between 0 and 100 scale)
learning_data['score_normalized'] = (learning_data['score'] - learning_data['score'].min()) / (learning_data['score'].max() - learning_data['score'].min()) * 100

# Match learning style (simplified to a binary match, e.g., "Kinesthetic" match = 1, no match = 0)
learning_data['learning_style_match'] = learning_data['preferred_learning_style'].apply(lambda x: 1 if x == 'Kinesthetic' else 0)  # Example match to "Kinesthetic"

# Calculate the recommendation score for each employee-module pair
learning_data['recommendation_score'] = (
    time_weight * learning_data['time_spent_normalized'] +
    score_weight * learning_data['score_normalized'] +
    learning_style_weight * learning_data['learning_style_match']
)

# Let's check the data and see the calculated recommendation scores
learning_data[['employee_id', 'training_module_id', 'module_name', 'recommendation_score']].head()

# Define some example learner personas for validation
personas = {
    "Fast Finisher": learning_data[learning_data['time_spent_minutes'] < 50],
    "Deep Diver": learning_data[learning_data['time_spent_minutes'] > 100],
    "Passive Explorer": learning_data[learning_data['score'].isna()],
}

# Display the top recommended modules for each persona
persona_recommendations = {
    persona: persona_data.nlargest(3, 'recommendation_score')[['employee_id', 'training_module_id', 'module_name', 'recommendation_score']]
    for persona, persona_data in personas.items()
}

# Display recommendations for each persona
print(persona_recommendations)

# Visualize the top recommended modules for each persona
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# For each persona, create a bar plot of the top recommended modules
personas_names = ["Fast Finisher", "Deep Diver", "Passive Explorer"]
for i, (persona, data) in enumerate(persona_recommendations.items()):
    if not data.empty:
        axes[i].barh(data['module_name'], data['recommendation_score'], color='skyblue')
        axes[i].set_title(f"Top Modules for {persona}")
        axes[i].set_xlabel('Recommendation Score')
        axes[i].set_ylabel('Module Name')
    else:
        axes[i].text(0.5, 0.5, 'No Recommendations', horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')
        axes[i].set_title(f"Top Modules for {persona}")

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()