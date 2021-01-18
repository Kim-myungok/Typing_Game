# from tkinter import 
# root=Tk()
# root.geometry("360x200")


try:
    import Tkinter as tk
except:
    import tkinter as tk


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Title)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Title(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="\n", font=('Helvetica', 25, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="=== Typing_Game ===", font=('Helvetica', 25, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="\n", font=('Helvetica', 25, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="게임 시작", font=('Helvetica', 13), height=2, width=20, 
                  command=lambda: master.switch_frame(Title_name)).pack()
        tk.Button(self, text="플레이 데이터", font=('Helvetica', 13), height=2, width=20,
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Label(self, text="\n", font=('Helvetica', 25, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="게임 종료",
                  command=lambda: exit()).pack()

class Title_name(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Game Start", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="< 다음 >",
                  command=lambda: master.switch_frame(Game_Start)) .pack()
        tk.Button(self, text="..게임 종료..",
                  command=lambda: exit()).pack()

class Game_Start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(Title)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(Title)).pack()

if __name__ == "__main__":
    root = SampleApp()
    root.geometry("480x480")
    root.title("Typing_Game")
    
    root.mainloop()
    
# def getTextInput():
#     result=textExample.get(1.0, END+"-1c")
#     print(result)

# text=Text(root, height=10)
# textExample.pack()
# Button(root, height=1, width=10, text="입력", 
#                     command=getTextInput)



# root.mainloop()


