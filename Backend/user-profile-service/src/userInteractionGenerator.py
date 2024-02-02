import random
import string
import json
from faker import Faker
from faker.providers import DynamicProvider

book_ids = []
interactions = []
users=[]
fake=Faker()

cities=["Iasi", "Cluj", "Bucharest", "Vaslui", "Brasov","Madrid","Londra","Amsterdam","Budapest","Genk","Vardar",
               "Miami","Moscow","Chicago","New York"]
companies=["Ignitely","Ideaful","Moxily","Flowly","Nimblely","Nextellar","Freshly","RDFStore","Sparkly","Avvlo","Fortify"
               ,"TheLoneWolf","GearTwo","Artfully","Changely","ScaleGear","Evolvely","BoundLink","Cleverly","Boostly"]
skills=["Java","React","Angular","C#","Photoshop","AWS","Azure","Python","Javascript","Management","Audit","Machine Learning",
        "Deep Learning","Databases","C++","UI/UX"]
hobbies=['play_piano','chess','table_tennis','esports','hiking','music','books','movies']
cities_provider = DynamicProvider(
     provider_name="city_provider",
     elements=cities,
)
companies_provider = DynamicProvider(
     provider_name="company_provider",
     elements=companies,
)
locales_provider = DynamicProvider(
     provider_name="locale_provider",
     elements=["ro","en","uk","bg","uk","fr","gr","bn","af","ar","ba","ca","fo","in","it","ja"],
)
# then add new provider to faker instance
fake.add_provider(cities_provider)
fake.add_provider(companies_provider)
fake.add_provider(locales_provider)


def generate_random_stringid(length):
    if length <= 0:
        return ""
    random_numbers = ''.join(random.choices(string.digits, k=length))
    return random_numbers


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_bookids(books_data):
    ids = []
    for book in books_data:
        if book['book_id'] == '' or book['title'] == '' or book['average_rating'] == '' or book['image_url'] == '':
            continue
        book_id = int(book['book_id'])
        ids.append(book_id)
    return ids


def create_interactions_for_user(user_id):
    global interactions
    number_of_books = random.randint(1, 10)
    random_elements = random.sample(book_ids, number_of_books)
    ratings = [1, 2, 3, 4, 5]
    for elem in random_elements:
        if random.choice([0, 1]) > 0.5:
            rating = random.choice(ratings)
            interactions.append({
                "user_id": user_id,
                "book_id": elem,
                "rating": rating
            })

def create_user_data(user_id:str):
    global users
    users.append({
        "user_id": user_id,
        "user_name": fake.name(),
        "email": fake.email(),
        "city": fake.city_provider(),
        "company":fake.company_provider(),
        "locale": fake.locale_provider(),
        "isKnown":True
    })


def save_to_json(list_to_save: list ,file_path):
    with open(file_path, 'w') as file:
        json.dump(list_to_save, file, indent=4)

##############Function for users with foreign key
# def list_data_to_json(info_list:list, file_name:str):
#     dict=[]
#     for element in info_list:
#         dict.append({
#             "id":  info_list.index(element),
#             "name": element,
#         })
#     file_path=f'../resources/{file_name}.json'
#     save_to_json(dict,file_path)
# def create_user_data_with_foreign_keys(user_id:str):
#     global users
#     users.append({
#         "user_id":user_id,
#         "user_name": fake.name(),
#         "email": fake.email(),
#         "city": cities.index(fake.city_provider()),
#         "company":companies.index(fake.company_provider()),
#         "locale": fake.locale_provider(),
#         "isKnown":True
#    })


def main():
    global book_ids
    global interactions
    length = 21
    books_data = read_json('../resources/books.json')
    book_ids = get_bookids(books_data)
    for i in range(1, 500):
        user_id = generate_random_stringid(length)
        create_user_data(user_id)   ###if we are using foreign key mode this will be un commented and use this instead:
                                        #create_user_data_with_foreign_keys(user_id)
        create_interactions_for_user(user_id)
    # save_to_json(interactions,'../resources/user_interactions.json')
    # save_to_json(users,'../resources/users.json')
    print(users)

    """
    This is used only if users table has a foreign keys city id and company id
    """
    #list_data_to_json(cities,'cities')
    #list_data_to_json(companies,'companies')
    #list_data_to_json(skills,'skills')

main()
