# **RecList Reads**
#### ✧ Video Demo:  <[⋆ URL HERE ⋆](https://youtu.be/oX4MW5lBW6E)>
#### ✧ Description: A program that gives book recommendations and provides a reading list.


### ⊹ About Program ⊹

Sometimes when you feel like flipping through book pages, you're not quite sure on what to read. And after looking through many recommendations on the internet, you feel overwhelmed, not even sure where to store those recommendations. That's why I created RecList Reads.

RecList Reads is a program that essentially has two main functions. Giving out book recommendations, and providing a reading list for it.

On the main menu after running the program, it gives options for getting book recommendations, looking through the reading list, and modifying said reading list.

The book recommendations are put together by inputting both the category and max results, which then passed to Google Books API, giving out lists of multiple books along with authors and the ratings of the books.

The user is then given an option to get more information about a specific book if they are interested in that book. The additional information given was summary, date published, and the number of pages of the book.

Further, they can add that book to a reading list, which then stores the specific book title, author, and reading status (which automatically put to be unread) into a csv file.

If the user wants to see the reading list, they can simply go back to the main menu and look through an option for reading list. With that option, the program will then print out the title, authors, and reading status of books inside of the reading list which was stored inside of a csv file.

The user is also given an option to modify the reading list. The option to do are adding book to reading list (by typing title, authors, and reading status yourself), deleting book from reading list (by entering the number of said book on the list), and changing reading status of a certain book (by typing number associated to the book on the list and typing out the updated status).

At the end, the user can go back (to the main menu) to see the newly updated reading list.

<br/>


### ⊹ Decision Making (deep dive on my thought process) ⊹

The first decision making to be done is about what project to do, I already explained that in the beginning.

The second decision I need to make is about what API I'm using in order to give out recommendations. There's a lot of searching, but my hand landed on Google books' API for the sole reason of being understandable enough and quite easy to access (at least for me).

As for the csv file, it contains title, authors, and status as the column (fieldnames). The truth is between writing the final project, I had to take a (long) break, leaving the csv part of the code (reading list related) unwritten. After coming back, trying to undertake the project again, I would have been lying if I say I didn't forget the whole week 6 file I/O shenanigans, meaning I had to rewatch the whole class and relearning the psets again. I domanaged to do it at the end though.

The hardest decision to make is on how I'm going to write the test file for the project. And at the end, I only tested for three functions and I used monkeypatch (definitely feels a bit cheeky). I clearly didn't make it easy for myself to test it when writing those custom functions. I don't even want to see them or talk about them ever again.

In the end, I'm quite happy with how the project turned. The fact that I decided and managed to think of some corner cases and making it more user friendly is nice! Thank you!

I truly enjoy every single one of the pain, sweat, eye sore, headache, and time "wasted" I had to endure on this project. (Or so I believe)

