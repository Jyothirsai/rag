import pandas as pd
import random
from datetime import datetime, timedelta

columns = [
    "Name", "priority", "state", "state reason", "assignment group", "assigned to",
    "opened", "resolved", "business duration", "closed", "opened by", "short description",
    "configuration item", "resolved ci", "initial priority", "reassignment", "reopen count",
    "reason to reopen", "closed by", "location", "category", "subcategory", "department",
    "closed code", "closed notes"
]

names = ["INC001", "INC002", "INC003", "INC004"]
priorities = ["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"]
states = ["New", "In Progress", "On Hold", "Resolved", "Closed"]
state_reasons = ["Awaiting user info", "Awaiting vendor", "Customer follow-up", "Solved"]
assignment_groups = ["Service Desk", "Network Team", "App Support", "Security Team"]
assigned_to = ["Alice", "Bob", "Charlie", "Diana"]
users = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
descriptions = ["Email not working", "VPN issue", "Software installation", "Account locked"]
config_items = ["Email Server", "VPN Gateway", "App XYZ", "Active Directory"]
resolved_cis = ["Email Server", "VPN Gateway", "App XYZ", "Active Directory"]
initial_priorities = ["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"]
reassignments = [0, 1, 2]
reopen_reasons = ["User request", "Not resolved", "Reopened by monitoring"]
locations = ["NYC", "London", "Tokyo", "Berlin"]
categories = ["Software", "Hardware", "Network", "Access"]
subcategories = ["Email", "Laptop", "WiFi", "Login"]
departments = ["IT", "HR", "Finance", "Operations"]
closed_codes = ["Solved (Permanently)", "Solved (Workaround)", "Not Solved", "Duplicate"]
closed_notes = ["Issue resolved after patch", "Temporary fix applied", "No issue found", "User error"]

data = []
for i in range(50):
    opened_date = datetime.now() - timedelta(days=random.randint(1, 30))
    resolved_date = opened_date + timedelta(hours=random.randint(1, 72))
    closed_date = resolved_date + timedelta(hours=random.randint(1, 24))
    business_duration = str(resolved_date - opened_date)

    row = [
        random.choice(names),
        random.choice(priorities),
        random.choice(states),
        random.choice(state_reasons),
        random.choice(assignment_groups),
        random.choice(assigned_to),
        opened_date.strftime('%Y-%m-%d %H:%M:%S'),
        resolved_date.strftime('%Y-%m-%d %H:%M:%S'),
        business_duration,
        closed_date.strftime('%Y-%m-%d %H:%M:%S'),
        random.choice(users),
        random.choice(descriptions),
        random.choice(config_items),
        random.choice(resolved_cis),
        random.choice(initial_priorities),
        random.choice(reassignments),
        random.randint(0, 3),
        random.choice(reopen_reasons),
        random.choice(users),
        random.choice(locations),
        random.choice(categories),
        random.choice(subcategories),
        random.choice(departments),
        random.choice(closed_codes),
        random.choice(closed_notes),
    ]
    data.append(row)

df = pd.DataFrame(data, columns=columns)
df.to_excel("servicenow_dummy_data.xlsx", index=False)
