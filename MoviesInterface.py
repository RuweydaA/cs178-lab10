# name: Ruweyda
# date: 03/04
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) 

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    title = input("Enter movie title: ").strip()

    table.put_item(
        Item={
            "Title": title,
            "Ratings": []
        }
    )

    print("Movie added successfully.\n")

def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    genre = movie.get("Genre", "Unknown Genre")
    ratings = movie.get("Ratings", [])

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Genre  : {genre}")
    print(f"  Ratings: {ratings if ratings else 'No ratings'}")
    print()

def print_all_movies():
    """
    Display all movies in the database.
    """
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No movies found.")
        return

    print(f"Found {len(items)} movie(s):\n")

    for movie in items:
        print_movie(movie)

def update_rating():
    try:
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))

        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={":r": [rating]}
        )
    except Exception:
        print("error in updating movie rating")

def delete_movie():
    title = input("What is the movie title? ")
    table.delete_item(Key={"Title": title})


def query_movie():
    title = input("What is the movie title? ")

    response = table.get_item(Key={"Title": title})
    movie = response.get("Item")

    if movie is None:
        print("movie not found")
        return

    ratings = movie.get("Ratings")

    if not ratings:
        print("movie has no ratings")
        return

    average = sum(ratings) / len(ratings)
    print(average)

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
