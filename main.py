from google_sheets import get_data


COMPANIES_ID = '1457129417'
CONTACTS_ID = '350809406'

print("*"*21)
print(" APPLICATION TRACKER ")
print("*"*21)

data = get_data()

if not data: exit(1)

print(data)