# create_dataset.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("Generating synthetic dataset...")

# Define internship domains and their initial popularity weights
domains = {
    "Software Engineering": 0.25,
    "Data Science": 0.20,
    "AI/ML Engineering": 0.10,  # Lower initial popularity
    "Cloud Computing": 0.15,
    "Cybersecurity": 0.10,     # Lower initial popularity
    "UI/UX Design": 0.12,
    "DevOps": 0.08,
}

# Number of records to generate
num_records = 5000

# Date range for applications
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 5, 31)

# Generate data
data = []
for i in range(num_records):
    # Make emerging fields more likely in later years
    year = random.randint(start_date.year, end_date.year)
    
    # Increase probability for emerging fields for 2023 and 2024
    current_domains = list(domains.keys())
    weights = list(domains.values())
    if year >= 2023:
        # Increase weights for AI and Cybersecurity
        weights[current_domains.index("AI/ML Engineering")] *= 2.5
        weights[current_domains.index("Cybersecurity")] *= 2.0
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    # Choose domain based on weights
    domain = np.random.choice(current_domains, p=normalized_weights)
    
    # Generate a random date within the year
    month = random.randint(1, 12) if year < end_date.year else random.randint(1, end_date.month)
    day = random.randint(1, 28) # Simple way to avoid month-end issues
    application_date = datetime(year, month, day)

    # Simulate participation status
    status = random.choices(["Applied", "Completed Internship"], weights=[0.7, 0.3], k=1)[0]
    
    data.append({
        "application_id": 10000 + i,
        "domain": domain,
        "application_date": application_date.strftime('%Y-%m-%d'),
        "status": status
    })

df = pd.DataFrame(data)
df.to_csv("internship_data.csv", index=False)

print(f"Successfully created 'internship_data.csv' with {len(df)} records.")
