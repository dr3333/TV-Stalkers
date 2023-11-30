# TV Stalkers
#### Video Demo: https://youtu.be/Y6D1saCI6J0
#### Description: An application that uses a third party API to get data on tv shows.
#### data.json file:
##### This is used to store tv shows information
#### helpers.py file:
##### This is used to store helper code for main.py
#### main.py file:
##### This is where all the important code is located
#### TV shows API:
##### https://www.episodate.com/api
#### Basic App Info
##### The Application is uses GMT as its standard time. It is light blue in color. With alternating row colors On its main window you have a table and 4 buttons(Title Info, Update, ADD, Delete).
##### Title Info.
###### This is used to look at information on the tv show like its name, id, next episode release date and the time to its release. it uses GMT. The time to release displays a countdown to when the episode will drop. Once the epsode drops it will update the list to released. If you have not clicked on any show when you click on "Title Info" it will display an error window requiring you to click on a title.
##### Update.
###### This is used to Update any TV show you with current information if any is available. The application automatically tries to update all of them on start update. If you have not clicked on any show when you click on "Update" it will display an error window requiring you to click on a title. If you have not clicked on any show when you click on "Update" it will display an error window requiring you to click on a title.
##### Delete
###### To delete a show from watchlist you simply click on it and then click delete, to delete the show from list. If you have not clicked on any show when you click on "Delete" it will display an error window requiring you to click on a title.
##### ADD
###### This opens a new window with an input field and a display for all the shows. It has 4 buttons (Search, Clear, Add to Watchlist, Exit)
##### Search
###### Once you input the show you want to look up into the text field. you can hit search to send a request to the API. If you have not typed anything into the text box it will alert you that you need to add to input something. If you input something and hit search, it will display any titles if any into its display box. It will also let you know of any errors
##### Clear
###### Clear just clears the input field and the display box.
##### Add to Watchlist
###### Once you find the show youre looking for you simply click on it in the display list and click "Add to Watchlist" to add to your list of shows you want updates on. It will check your list if it has the title already, if it does it will only update it, this is to prevent duplicates. If you have not clicked on any show when you click on "Add to Watchlist" it will display an error window requiring you to click on a title.
##### Exit
###### You exit the ADD window. Or you can hit the "X" on the title bar.
