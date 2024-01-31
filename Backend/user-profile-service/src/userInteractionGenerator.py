import random
import string
import json

book_ids = []
interactions = []


# class UserInteraction:
#     def __init__(self, user_id, book_id, rating):
#         self.user_id = user_id
#         self.book_id = book_id
#         self.rating = rating

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


def save_to_json(user_interactions: list):
    with open('../resources/user_interactions.json', 'w') as file:
        json.dump(user_interactions, file, indent=4)


def main():
    global book_ids
    global interactions
    length = 21
    books_data = read_json('../resources/books.json')
    book_ids = get_bookids(books_data)
    for i in range(1, 500):
        user_id = generate_random_stringid(length)  # extend this to generate fake user with all data necessary for saving him in db
        create_interactions_for_user(user_id)
    save_to_json(interactions)


main()
