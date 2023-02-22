# Commerce (E-Bay Adaptation)

![Screen Shot 2023-01-27 at 12 37 40 PM](https://user-images.githubusercontent.com/92412291/215155985-2ed5c985-8088-47ae-84b2-a666fe62aebe.png)

# Specifications

## Models

This project included the usage of 5 models in User, Listing, Bid, PersonalWatchList, and Comment. 

## User Authentication and Authorization

Potential users were given the opportunity to register for an account by providing a username and password, which allows them to create listings, bid and comment on other listings, and add listings to their watchlist.
Users also have the ability to delete their own comments made on a listing, and have the ability to close their listing(s) whenever they please.

## Active Listings Page (Home Page)

The default route of this web application lets all users (logged in or not) to view all of the currently active auction listings. For each active listing, this page should display the title, current price, and photo (if one exists for the listing).
Also, users that are authenticated will be able to see whether listings are in their watchlist or not, giving them a "Remove" button instead of the "watchlist" button seen above.

## Listing Page

![Screen Shot 2023-01-27 at 12 57 54 PM](https://user-images.githubusercontent.com/92412291/215160325-b290f30c-1360-4c4d-b216-197f2982eb44.png)
![Screen Shot 2023-01-27 at 1 05 47 PM](https://user-images.githubusercontent.com/92412291/215161605-c7fda380-c626-44d7-a783-e2f0443c2a5f.png)

Clicking on a listing should take users to a page specific to that listing. On that page, users can view all details about the listing including the current price for the listing and add comments to the bottom of the page.

- If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.
- If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user will be presented with an error.
- If the user is signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active, and gets moved to the "Closed Listings" tab.
- If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
- Users who are signed in can add comments to the listing page. The listing page should display all comments that have been made on the listing. Users can also delete their own comments.

## Watchlist

Users who are signed in can visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
Users may also remove listings from their watchlist by clicking the "Remove" button.

## Closed Listings

Listings that have been closed by authorized users (Creators of the listings) are presented here with the name of the winner, the price it sold for, and the image of the listing.

## Categories

 Users can visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

## Usage:

Requires Python(3) and the Python Pacakage Installed (pip) to run:

Install requirements (Django): 
 ```
 pip3 install django
 ```
To download this app, enter the following in your terminal: 
```
git clone https://github.com/ronaakk/E-Commerce-Site.git
```
Migrate and run the app locally: 
```
python3 manage.py makemigrations auctions
python3 manage.py migrate
python3 manage.py runserver
```
