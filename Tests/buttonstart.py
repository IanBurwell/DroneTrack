def wait_go_button(size=8):
    import tkinter as tk


    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    def endPgrm():
        root.destroy()
    button = tk.Button(frame,
                       text="GO",
                       bg="green",
                       height=size,
                       width=size,
                       font=('Helvetica', int(size*2)),
                       command=endPgrm)

    button.pack(side=tk.TOP)

    root.mainloop()

if __name__ == "__main__":
    wait_go_button()