def wait_go_button():
    import tkinter as tk

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    def endPgrm():
        root.destroy()
    button = tk.Button(frame,
                       text="GO",
                       fg="green",
                       command=endPgrm)

    button.pack(side=tk.TOP)

    root.mainloop()
