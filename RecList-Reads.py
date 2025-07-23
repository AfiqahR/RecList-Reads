# RecList Reads: Recommendations and Reading list for books

import requests
import os
import csv
from tabulate import tabulate
from html2text import html2text


def main():
    while True:
        # print_menu printing the menu, 1-4 using specific format
        print_menu()
        choice = input("Enter your choice (1-4): ")

        # choice 1 is to give out recommendation
        if choice == "1":
            category, max_results = get_input()
            recommendations = get_recom(category, max_results) # with API return list of dictionary for title, authors, ratings

            if recommendations:
                print_recom(recommendations)

                while True:

                    more_info = input("\nWould you like to know more about a specific book? (yes/no): ").lower().strip()

                    if more_info == "yes" or more_info == "y":
                        # get the description, pages of book
                        number_book = check_get_book(max_results)
                        get_book_info(number_book, recommendations)

                        add_book_to = input("\nWould you like to add the book to the reading list? (yes/no): ").lower().strip()

                        if add_book_to == "yes" or add_book_to == "y":
                            # add the specific book into csv file
                            add_recom_book(number_book, recommendations)

                    else:
                        print("⊹ Returning to main menu...")
                        break

            else:
                print("No book recommendations found for the specified category.")

        elif choice == "2":
            # printing reading list in a format
            print_reading_list()

        elif choice == "3":
            # gives option to modify
            modify_reading_list()

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")



def print_menu():
    '''
    using tabulate, print the menu prettyly
    menu
    1. Book Recommendations
    2. Reading List
    3. Modify List
    4. Exit
    '''

    menu = [
        ["1", "Book Recommendations"],
        ["2", "Reading List"],
        ["3", "Modify Reading List"],
        ["4", "Exit"]
    ]
    print("\n  ✧ Welcome to RecList Reads!✧")
    print(tabulate(menu, headers=["Option", "Description"], tablefmt="pretty"))



def print_menu2():
    '''
    using tabulate print the menu prettily
    menu
    1. Add Book
    2. Remove Book
    3. Change Reading Status
    4. Back to Menu
    '''

    menu = [
        ["1", "Add Book"],
        ["2", "Remove Book"],
        ["3", "Change Reading Status"],
        ["4", "Back to Main Menu"]
    ]

    print("")
    print(tabulate(menu, headers=["Option", "Description"], tablefmt="pretty"))


def get_input():
    # get the category while making sure max_result is in int
    category = input("Enter book category (e.g., fiction, history): ")
    while True:
        try:
            max_results = int(input("Enter maximum number of book recommendations: "))
            return category, max_results
        except ValueError:
            print("Please enter a valid number.")


def get_recom(category, max_results):
    '''
    using google book API, takes in category and max rslt as args to pass in to request.get(link, param=params)
    it then run a loop based on how many items in data, get the key-value pairs for title, authors, and ratings, (also id),
    and then store those in a dict inside of a list, then return it(the list).

    reference link + params = data = https://www.googleapis.com/books/v1/volumes?q=subject:mystery&maxResults=10 (example)

    '''
    # Define the API url
    url = "https://www.googleapis.com/books/v1/volumes"

    # Define query parameters
    params = {
        "q": f"subject:{category}",
        "maxResults": max_results
    }

    # Send GET request to the API
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:

        data = response.json()
        # Extract book information
        books = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo")
            title = volume_info.get("title")
            authors = volume_info.get("authors", ["Unknown"]) # the author is in list, so need to join when append
            average_rating = volume_info.get("averageRating", "N/A")
            books.append({"title": title, "authors": (", ".join(authors)), "average_rating": average_rating, "id": item.get("id")})

        return books

    else:
        print("Failed to retrieve book recommendations.")
        return []


def print_recom(recommendations):
    '''
    printing book recommendations, taking list of books as param(recommendations) then using for loop and enumerate,
    it printed the number, along with  title, author, and ratings of the book.
    '''

    print("\nBook Recommendations:")
    for i, book in enumerate(recommendations, 1):
        print(f"{i}. Title: {book['title']}")
        print(f"   Authors: {book['authors']}")
        print(f"   Average Rating: {book['average_rating']}")


def check_get_book(max_results):
    # making sure the number input for which book user are interested on is an int and didn't exceed the provided recommendations.
    while True:
        try:
            number_book = int(input("Enter the number of the book you want to know more about: "))
            if 1 <= number_book <= max_results:
                return number_book
            else:
                print(f"Invalid number. Please enter a number between 1 and {max_results}.")
        except ValueError:
            print("Please enter a valid number.")


def get_book_info(number_book, recommendations):
    '''
    number_book = ask user about which book they would like to know more
    get the book id from recommendations, put it inside the API link to get the specific key value of needed key,
    which is published date, description, and pagecount
    reference: link+bookID = https://www.googleapis.com/books/v1/volumes/bIZiAAAAMAAJ (game of thrones)
    also return number_book
    '''

    book_id = recommendations[number_book-1]["id"]
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

    # more information of the book, using the book id of the specific book provide summary, date, and page count.
        volume_info = data.get("volumeInfo")
        description = volume_info.get("description", "Summary not available.")
        page_count = volume_info.get("pageCount", "Page count not available.")
        published_date = volume_info.get("publishedDate", "Published date not available.")

        print(f"\nHere are some information about {recommendations[number_book-1]['title']}: ")
        print(f"Published Date: {published_date}")
        print(f"Number of Pages: {page_count}")
        print(f"Summary: \n{html2text(description)}")

    else:
        print("Failed to retrieve book information.")



def add_recom_book(number_book, recommendations):
    '''
    will be executed if add_book_to = yes is True.
    will index through the recommendations[number_book-1] and save it into new variable
    using File I/O,
    open csv file, and with writeDict write title, authors, and reading status = unread
    '''

    # take the specific book info(a dictionary) to then put into the csv file
    specific_book = recommendations[number_book-1]

    need_header = not os.path.exists("reading_list.csv") or os.stat("reading_list.csv").st_size == 0

    with open("reading_list.csv", "a+", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "authors", "status"])
        if need_header:
            writer.writeheader()
        writer.writerow({"title": specific_book["title"], "authors": specific_book["authors"], "status": "Unread"})

    print(f"⊹ {specific_book['title']} is added to reading list.")


def print_reading_list():
    '''
    print book title, authors, and reading status of the list inside the csv file,
    by opening it first, read the csv file as a dict, append it into a list,
    and then for each book (dict inside the list) print title, authors, reading status
    '''

    # put csv file inside of a list (a dict(with the property of one book) inside a list)
    book_list = []

    try:
        with open("reading_list.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_list.append({"title": row["title"], "authors": row["authors"], "status": row["status"]})

    except FileNotFoundError:
        print("Reading list is empty.")
        return

    # print the property of a book / displaying on terminal
    print("\nReading List:")
    for i, book in enumerate(book_list, 1):
        print(f"{i}. Title: {book['title']}")
        print(f"   Authors: {book['authors']}") # might want to look into case when there is multiple author (using join)
        print(f"   Reading Status: {book['status']}")


def modify_reading_list():
    '''
    Where menu2 is executed.
    Based on the choice outputted will add book, remove book, or change status of the book.
    '''
    while True:
        print_menu2()
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            change_status()
        elif choice == "4":
            print("⊹ Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def add_book():
    '''
    gives input for title, authors, and reading status append it to the csv file,
    at the end it print("Book added to reading list.")
    return to menu2
    '''

    # ask user title, authors, and status of the book which then put into the csv file
    title = input("Title: ")
    authors = input("Authors: ")
    status = input("Reading Status(Finished/Reading/Unread): ")

    need_header = not os.path.exists("reading_list.csv") or os.stat("reading_list.csv").st_size == 0

    with open("reading_list.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "authors", "status"])
        if need_header:
            writer.writeheader()
        writer.writerow({"title": title, "authors": authors, "status": status})

    print(f"⊹ '{title}' is added to reading list.")


def check_book(book_list, question):
    '''
    Ask user for a book number based on the provided question.
    Validate the input to ensure it's a valid integer and within the range of book_list.
    '''

    # in a infinite loop, ask user number until it was valid.
    while True:
        try:
            book_changed = int(input(f"\n{question}"))
            if 1 <= book_changed <= len(book_list):
                return book_changed
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(book_list)}.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def remove_book():
    '''
    printed out the reading list,
    remove specific book(dict) from csv file after check_book is executed,
    by opening the csv file with w mode (rewrite the entire thing),
    and write the csv file based on the list after specific book is deleted.
    then it print "Book is removed from reading list."
    return to menu2
    '''

    # do the same thing as print_reading_list()
    book_list = []

    try:
        with open("reading_list.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_list.append({"title": row["title"], "authors": row["authors"], "status": row["status"]})

    except FileNotFoundError:
        print("Reading list is empty.")
        return

    # check if it empty
    if not book_list:
        print("Reading list is empty.")
        return

    print("\nReading List:")
    for i, book in enumerate(book_list, 1):
        print(f"{i}. Title: {book['title']}")
        print(f"   Authors: {book['authors']}")
        print(f"   Reading Status: {book['status']}")


    # check the validity of books user want to remove
    question = "Enter the number of the book you want to remove from the list: "
    book_remove = check_book(book_list, question)

    # delete the specific book
    deleted_book = book_list.pop(book_remove - 1)

    # rewrite the csv file with the now updated list.
    with open("reading_list.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "authors", "status"])
            writer.writeheader()
            for book in book_list:
                writer.writerow(book)

    print(f"⊹ {deleted_book['title']} is removed from reading list.")



def change_status():
    '''
    print out reading list,
    change reading status based on which number of book ask to be changed
    it then prompt the user the status it wanted to be changed as,
    later it printed out "status is UPDATED from reading list"
    Return to menu2
    '''

    # do the same thing as print_reading_list()
    book_list = []

    try:
        with open("reading_list.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_list.append({"title": row["title"], "authors": row["authors"], "status": row["status"]})

    except FileNotFoundError:
        print("Reading list is empty.")
        return

    # check if it empty
    if not book_list:
        print("Reading list is empty.")
        return

    print("\nReading List:")
    for i, book in enumerate(book_list, 1):
        print(f"{i}. Title: {book['title']}")
        print(f"   Authors: {book['authors']}")
        print(f"   Reading Status: {book['status']}")


    # check the validity of books user want to change
    question = "Enter the number of the book you want to modify the status for: "
    book_changed = check_book(book_list, question)

    new_status = input("updated status: ")
    # delete the specific book
    book_list[book_changed - 1]["status"] = new_status

    # rewrite the csv file with the now updated list.
    with open("reading_list.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "authors", "status"])
            writer.writeheader()
            for book in book_list:
                writer.writerow(book)

    print(f"⊹ Status of {book_list[book_changed - 1]['title']} is updated from reading list.")


if __name__ == "__main__":
    main()
