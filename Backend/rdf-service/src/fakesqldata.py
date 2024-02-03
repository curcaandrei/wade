from faker import Faker
fake = Faker()

num_records = 20

sql_template = "INSERT INTO users_data (user_id, user_name, email, locale, city, company) VALUES\n  {};"

# Generate data
values = []
for i in range(1, num_records + 1):
    user_id = str(i)
    user_name = fake.first_name() + str(i)
    email = fake.email()
    locale = fake.country_code().lower()
    city = fake.city()
    company = fake.company()
    values.append(f"('{user_id}', '{user_name}','{email}','{locale}','{city}','{company}')")

sql_query = sql_template.format(",\n  ".join(values))

print(sql_query)
