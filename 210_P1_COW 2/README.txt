CSC 210 Project 1
Spring 2023 - 03/05/23
MaKayla Robinson - mrobin45

I built a Community Organization Website featuring UR Events.
The events are added to the website through a JSON file under the app.app_context()
method in app.py.
Users can't add events, but they can sign up for an account and register for events once
logged into their account. There are currently 5 events in the database.

There are 2 views to my website--
1 for users who are logged in, and another for users that are not logged in.

    View when logged in:
    HOME - this is the default view. Each event card has a button to register for the event 
        or delete a current registration. When a user chooses to register for an event on the home page
        it prints a message at the top if the registration is successful and refreshes the page,
        with the corresponding button showing the user is registered. If a user deletes a registration
        the message is shown at the top (if successful) and takes the user to their profile page so
        they can view their other events.
    PROFILE - shows the user a table of the events they've registered for, including title,
        date, and actions to take on event. If successful, the 'delete' action will show a message at the top
        and refresh the page with the user's remaining events, or display a message telling the user they
        aren't registered for any events. If the user chooses the 'register for more events' action,
        they're taken to the home page where the events are listed, where they can register for events
        using the button on the event cards.
    LOGOUT - a link for users to logout. When a user clicks the logout button, they're logged out
        and redirected to the home page.

    View when not logged in:
    HOME - this is the default view, and the only place where events are listed.
        Each event card prompts the viewer to 'login to register' for the event.
    LOGIN - allows users to login to their account. Rememebrs user's credentials for ease of login.
    SIGN UP - allows users to sign up for an account. Displays form for user's info.

All actions work correctly. Most print messages at the top of the screen to let you know
the action was successful.

My models, classes, and routes are all in app.py. I used bootstrap for css styling, and extended
a base.html page for all html pages. There's an html page for base, home, login, profile, and signup;
all html files are in the templates folder.