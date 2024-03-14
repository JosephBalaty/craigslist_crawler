import pprint
from tkinter import *
from tkinter import ttk
from crawler.cragislist_postings import craigslistCrawl
from notifications.send_responses import sendEmail
from database.db_app import *
from tkinter import messagebox
import time

# Start with the bare essential of the application.

def repeat_function():
    # Your function to execute goes here
    print("Executing function at", time.strftime("%Y-%m-%d %H:%M:%S"))

    # Schedule the function to run again after 24 hours
    root.after(24 * 60 * 60 * 1000, repeat_function)
    sendEmails()

def sendEmails():
    listings = getListings()
    for list in listings:
        try:
            relevant_listings = craigslistCrawl(list["Query"], zipcode=list["Zipcode"],
                                                query=list["Query"], max_dist=list["Max_Dist"], )

            if len(relevant_listings) == 0:
                continue

            sendEmail(relevant_listings, list["Query"], list["Email"])
        except:
            print("Error! Did not work.")

    print("Finished sending emails!")


# Create a listing on a screen which accepts information to
# have a web crawler scour the facebook marketplace.
# Results returned should be parsed and then emailed and texted to the user.
class WelcomePage():
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)


        ttk.Label(self.mainframe, text="""Welcome Page""").grid(column=2, row=1, sticky=(W, E))

        ttk.Label(self.mainframe, text="Add a new listing Notification").grid(column=1, row=2, sticky=W)
        ttk.Button(self.mainframe, text="Add New Listing", command=self.addListingPage).grid(column=2, row=2, sticky=W)

        ttk.Label(self.mainframe, text="Delete a Listing Notification").grid(column=1, row=3, sticky=W)
        ttk.Button(self.mainframe, text="Delete Listing", command=self.addDeleteListingPage).grid(column=2, row=3, sticky=W)

        ttk.Label(self.mainframe, text="Update Listing Notifications").grid(column=1, row=4, sticky=W)
        ttk.Button(self.mainframe, text="Update Listings", command=self.addUpdatePage).grid(column=2, row=4, sticky=W)

        ttk.Label(self.mainframe, text="Obtain all Notifications").grid(column=1, row=5, sticky=W)
        ttk.Button(self.mainframe, text="Obtain all Listings", command=self.sendEmails).grid(column=2, row=5, sticky=W)


        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def addUpdatePage(self):
        UpdateListingPage(root)
    def sendEmails(self):
        t0 = time.time()
        listings = getListings()
        messagebox.showinfo(message=f'Obtaining results and sending emails!')
        for list in listings:
            try:
                relevant_listings = craigslistCrawl(list["Query"], zipcode=list["Zipcode"],
                                                    query=list["Query"], max_dist=list["Max_Dist"], )

                if len(relevant_listings) == 0:
                    continue

                sendEmail(relevant_listings, list["Query"], list["Email"])
            except:
                print("Error! Did not work.")
        t1 = time.time()

        messagebox.showinfo(message=f'Finished sending results\nTime taken: {t1-t0}')

    def addListingPage(self):
        NewListingPage(root)

    def addDeleteListingPage(self):
        DeleteListingPage(root)


class NewListingPage():
    def __init__(self, root):


        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.listingName = StringVar()
        ttk.Label(self.mainframe, text="Listing Name").grid(column=1, row=1, sticky=W)
        listing_entry = ttk.Entry(self.mainframe, width=14, textvariable=self.listingName)
        listing_entry.grid(column=2, row=1, sticky=(W, E))

        self.query = StringVar()
        ttk.Label(self.mainframe, text="Enter a Query: ").grid(column=1, row=2, sticky=W)
        query_entry = ttk.Entry(self.mainframe, width=14, textvariable=self.query)
        query_entry.grid(column=2, row=2, sticky=(W, E))


        ttk.Label(self.mainframe, text="Notifications").grid(column=1, row=3, sticky=W)


        self.email = StringVar()
        ttk.Label(self.mainframe, text="Email: ").grid(column=2, row=5, sticky=W)
        email = ttk.Entry(self.mainframe, width=14, textvariable=self.email)
        email.grid(column=3, row=5, sticky=(W, E))

        ttk.Label(self.mainframe, text="User Location").grid(column=1, row=6, sticky=W)

        self.zipcode = IntVar()
        ttk.Label(self.mainframe, text="Zip Code (5 digits): ").grid(column=2, row=7, sticky=W)
        zipcode = ttk.Entry(self.mainframe, width=14, textvariable=self.zipcode)
        zipcode.grid(column=3, row=7, sticky=(W, E))

        self.max_dist = IntVar()
        ttk.Label(self.mainframe, text="Maximum Distance: ").grid(column=2, row=8, sticky=W)
        max_dist = ttk.Entry(self.mainframe, width=14, textvariable=self.max_dist)
        max_dist.grid(column=3, row=8, sticky=(W, E))

        self.max_price = IntVar()
        ttk.Label(self.mainframe, text="Max Price: ").grid(column=1, row=9, sticky=W)
        max_price = ttk.Entry(self.mainframe, width=14, textvariable=self.max_price)
        max_price.grid(column=2, row=9, sticky=(W, E))

        ttk.Button(self.mainframe, text="Submit Listing", command=self.addQuery).grid(column=3, row=12, sticky=W)
        ttk.Button(self.mainframe, text="Go Back", command=self.prevWindow).grid(column=1, row=12, sticky=W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def prevWindow(self):
        self.mainframe.destroy()

    def addQuery(self):
        listing = {"Listing_Name": self.listingName.get(),
         "Max_Price": self.max_price.get(),
         "Zipcode": self.zipcode.get(),
         "Max_Dist": self.max_dist.get(),
         "Query": self.query.get(),
         "Email": self.email.get()}
        addListing(listing)
        messagebox.showinfo(message=f'Listing added to database.')


class UpdateListingPage():
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="6 6 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # retrieve the listings on the page, and then display them,
        # each with an option to delete the listing.
        listings = getListings()
        i = 0
        # Create a dictionary of the
        # postings with the updated values for each one.
        self.dict_listings = {}
        for list in listings:
            list_id = list["_id"]
            self.dict_listings[list_id] = {}

            self.dict_listings[list_id]["Listing_Name"] = StringVar()
            self.dict_listings[list_id]["Listing_Name"].set(list["Listing_Name"])
            ttk.Label(self.mainframe, text=f'Listing Name: ',).grid(column=i, row=0, sticky=E)
            listingName = ttk.Entry(self.mainframe, width=25, textvariable=self.dict_listings[list_id]["Listing_Name"])
            listingName.grid(column=i+1, row=0, sticky=W)

            self.dict_listings[list_id]["Query"] = StringVar()
            self.dict_listings[list_id]["Query"].set(list["Query"])
            ttk.Label(self.mainframe, text=f'Query: ').grid(column=i, row=1, sticky=E)
            query = ttk.Entry(self.mainframe, width=14, textvariable=self.dict_listings[list_id]["Query"])
            query.grid(column=i+1, row=1, sticky=W)

            self.dict_listings[list_id]["Zipcode"] = IntVar()
            self.dict_listings[list_id]["Zipcode"].set(list["Zipcode"])
            ttk.Label(self.mainframe, text=f'Zipcode: ').grid(column=i, row=2, sticky=E)
            zipcode = ttk.Entry(self.mainframe, width=14, textvariable=self.dict_listings[list_id]["Zipcode"])
            zipcode.grid(column=i+1, row=2, sticky=W)

            self.dict_listings[list_id]["Max_Dist"] = IntVar()
            self.dict_listings[list_id]["Max_Dist"].set(list["Max_Dist"])
            ttk.Label(self.mainframe, text=f'Max Distance: ').grid(column=i, row=3, sticky=E)
            max_dist = ttk.Entry(self.mainframe, width=14, textvariable=self.dict_listings[list_id]["Max_Dist"])
            max_dist.grid(column=i+1, row=3, sticky=W)

            self.dict_listings[list_id]["Max_Price"] = IntVar()
            self.dict_listings[list_id]["Max_Price"].set(list["Max_Price"])
            ttk.Label(self.mainframe, text=f'Max Price: ').grid(column=i, row=4, sticky=E)
            max_price = ttk.Entry(self.mainframe, width=14, textvariable=self.dict_listings[list_id]["Max_Price"])
            max_price.grid(column=i+1, row=4, sticky=W)

            self.dict_listings[list_id]["Email"] = StringVar()
            self.dict_listings[list_id]["Email"].set(list["Email"])
            ttk.Label(self.mainframe, text=f'Email: ').grid(column=i, row=5, sticky=E)
            email = ttk.Entry(self.mainframe, width=25, textvariable=self.dict_listings[list_id]["Email"])
            email.grid(column=i+1, row=5, sticky=W)


            ttk.Button(self.mainframe, text="Update Listing", command=lambda v=list["_id"]: self.updatePost(v)).grid(column=i+1, row=6,)
            i += 2

        ttk.Button(self.mainframe, text="Go Back", command=self.prevWindow).grid(column=0, row=7, sticky=W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def prevWindow(self):
        self.mainframe.destroy()

    def updatePost(self, id):
        print(f'retrieved id : {id}')
        list = self.dict_listings[id]
        new_list = {key : value.get() for key, value in list.items()}

        updateListing(id, new_list)
        messagebox.showinfo(message=f'Listing with id {id} is updated. Returning to home screen.')
        self.prevWindow()


class DeleteListingPage():
    def __init__(self, root):
        self.mainframe = ttk.Frame(root, padding="6 6 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # retrieve the listings on the page, and then display them,
        # each with an option to delete the listing.
        listings = getListings()
        i = 0
        for list in listings:
            ttk.Label(self.mainframe, text=f'Listing Name: {list["Listing_Name"]}',).grid(column=i, row=0, sticky=W)
            ttk.Label(self.mainframe, text=f'Query: {list["Query"]}').grid(column=i, row=1, sticky=W)
            ttk.Label(self.mainframe, text=f'Zipcode: {list["Zipcode"]}').grid(column=i, row=2, sticky=W)
            ttk.Label(self.mainframe, text=f'Max Distance: {list["Max_Dist"]} Miles').grid(column=i, row=3, sticky=W)
            ttk.Label(self.mainframe, text=f'Max Price: ${list["Max_Price"]}').grid(column=i, row=4, sticky=W)
            ttk.Label(self.mainframe, text=f'Email: {list["Email"]}').grid(column=i, row=5, sticky=W)
            ttk.Button(self.mainframe, text="Delete Listing", command=lambda v=list["_id"]: self.deletePost(v)).grid(column=i, row=6, sticky=W)
            i += 1

        ttk.Button(self.mainframe, text="Go Back", command=self.prevWindow).grid(column=0, row=7, sticky=W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def prevWindow(self):
        self.mainframe.destroy()

    def deletePost(self, id):
        print(f'retrieved id : {id}')
        deleteListing(id)
        messagebox.showinfo(message=f'Listing with id {id} is deleted. Returning to home screen.')
        self.prevWindow()


# With our values, we need to crawl Facebook.
if __name__ == "__main__":
    root = Tk()
    root.after(24 * 60 * 60 * 1000, repeat_function)
    root.title("Craigslist Notifier")
    WelcomePage(root)
    root.mainloop()
