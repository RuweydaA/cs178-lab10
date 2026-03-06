# name: Ruweyda
# date: 03/06
# description: Custom CRUD interface with DynamoDB, CS178 Lab 10


import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Books")

def create_book():
    title = input("Enter book title: ").strip()
    genre = input("Enter genre: ").strip()
    year = int(input("Enter year: "))

    table.put_item(
        Item={
            "Title": title,
            "Genre": genre,
            "Year": year
        }
    )

    print("book created")

def print_book(book):
    title = book.get("Title", "Unknown Title")
    genre = book.get("Genre", "Unknown Genre")
    year = book.get("Year", "Unknown Year")

    print(f"  Title : {title}")
    print(f"  Genre : {genre}")
    print(f"  Year  : {year}")
    print()

def read_all_books():
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("no books found")
        return

    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)

def update_book():
    try:
        title = input("Enter book title: ").strip()
        genre = input("Enter new genre: ").strip()

        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Genre = :g",
            ExpressionAttributeValues={":g": genre}
        )

        print("book updated")
    except Exception:
        print("error updating book")

def delete_book():
    title = input("Enter book title: ").strip()
    table.delete_item(Key={"Title": title})
    print("book deleted")

def query_book():
    title = input("Enter book title: ").strip()

    response = table.get_item(Key={"Title": title})
    book = response.get("Item")

    if book is None:
        print("book not found")
        return

    print_book(book)

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new book")
    print("Press R: to READ all books")
    print("Press U: to UPDATE a book")
    print("Press D: to DELETE a book")
    print("Press Q: to QUERY a book")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")

        if input_char.upper() == "C":
            create_book()
        elif input_char.upper() == "R":
            read_all_books()
        elif input_char.upper() == "U":
            update_book()
        elif input_char.upper() == "D":
            delete_book()
        elif input_char.upper() == "Q":
            query_book()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()