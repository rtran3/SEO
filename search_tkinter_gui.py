import tkinter as tk
import webbrowser
from basic_query import search_function


def weblink(event):
    '''Take in each url and if clicked, open in the web browser'''
    w = event.widget
    if len(w.curselection())>0:
        index = w.curselection()[0]
        item = w.get(index)
        webbrowser.open_new('http://'+item)


# Creating overall window of gui.
root = tk.Tk()
root.title("Project 3: Search Engine")
root.geometry("800x800")

# Frame for the entry box and search button
frame = tk.Frame(root)
frame.pack()

# Bottom Frame for the listbox of results
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.BOTH, expand=True)

# Entry box for inputting search query.
entry1 = tk.Entry(frame, font=('Arial',15))


def getSearchQuery():
    '''Get the user text input and run it through the basic_query function.
        Display results in a ListBox'''
    # Delete the previous ListBox to display new search results
    for widget in bottom_frame.winfo_children():
        widget.destroy()
    
    # Get the text from entry box
    x1 = entry1.get()

    # Make scroll bar and result box to dynamically fill the window no matter what size
    scrollbar = tk.Scrollbar(bottom_frame, orient="vertical")
    lb = tk.Listbox(bottom_frame,yscrollcommand=scrollbar.set,font=('Arial',10))
    scrollbar.config(command=lb.yview)
    scrollbar.pack(side="right", fill="y")
    lb.pack(side="left",fill="both", expand=True)

    # Call search function with entry text
    results = search_function(x1)

    #bind each link to weblink to make it into a hyperlink
    lb.bind('<<ListboxSelect>>', weblink)
    for item in results:
        lb.insert(tk.END, item)

# If Search button is pressed, run the getSearchQuery function with the user text input
button1 = tk.Button(frame,text='Search', command=getSearchQuery)

entry1.pack(side=tk.LEFT)
button1.pack(side=tk.LEFT)

root.mainloop()
