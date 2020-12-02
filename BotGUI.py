import tkinter as tk
from tkinter import messagebox
import tweepy
from tweepy import *
from plyer.utils import platform
from plyer import notification
from datetime import datetime  
import webbrowser
import sys
import os

python=sys.executable

class MyListener(StreamListener):

	def __init__(self):
		super(MyListener, self).__init__()

	def on_status(self, status):

		#Only listen to tweets posted by the user himself, not mentions.
		if status.user.id_str not in [str(v.get())]:
			return

		output.insert(tk.END, f'{status.user.name} tweeted at ')
		output.insert(tk.END, datetime.now().strftime("%H:%M:%S")+':\n')
		output.insert(tk.END, f'{status.text}\n')

		notification.notify(
		title='Twitter bot alert!',
		message=f'{status.user.name} tweeted!',
		app_name='finalbot.py',
		app_icon='C:/Users/klaas/Desktop/TwitterBot/BotProject/logo.' + ('ico' if platform == 'win' else 'png')
		)

	def on_error(self, status_code):

		print(status_code, flush=True)

		notification.notify(
		title='Twitter bot alert!',
		message='Error, please check the program and restart manually',
		app_name='finalbot.py',
		app_icon='C:/Users/klaas/Desktop/TwitterBot/BotProject/logo.' + ('ico' if platform == 'win' else 'png')
		)
		
		if status_code == 420:
			tk.messagebox.showerror(title='ERROR', message='420 rate limit error. Close and restart the program manually.')
		
		# returning False in on_error disconnects the stream
		return False


#Enter API keys here
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

root = tk.Tk()
root.title("Twitter Listener")

#Start listening and unbind to prevent errors from clicking listen twice
def listen(event=None):
	val = [str(v.get())]

	bot(val)

	listen_button['state'] = tk.DISABLED
	listen_button.unbind("<Button-1>")

#Quit listening by deleting stream and restarting the program (I couldn't find another way to properly close the stream within tkinter)
#Listening and quiting in rapid succession can still cause rate limit errors. Manual restart fixes it.
def quit_listen(event=None):
	global listener
	global stream

	del listener
	del stream
	root.destroy()
	os.execl(python,python,*sys.argv)
	
def bot(val):
	global stream
	global listener
	#Start stream, is_async allows stream to be on new thread everytime, allowing normal tkinter functionality
	listener = MyListener()
	stream = Stream(auth=api.auth, listener=listener)
	stream.filter(follow=val, is_async=True)
		
def clear(event):
	v.set('')

#Limit input to integers
def test_val(inStr,acttyp):
	if acttyp == '1': #insert
		try:
			int(inStr)
		except ValueError:
			return False
	return True

def character_limit(v):
	if len(v.get()) > 30:
		tk.messagebox.showerror(title='ERROR', message='Max length of entry widget is 30 ch')
		clear(event=None)
		return 'break'

def hyperlink(event):
	webbrowser.open_new(event.widget.cget("text"))

#Set stringvar to be able to register input. "2899773086" is an account that tweets every three minutes for testing.
v = tk.StringVar()
v.set("")
v.trace("w", lambda *args: character_limit(v))

#Defining buttons and widgets
text = tk.Label(root, height=4, width=100, text="Enter the twitter ID of the account you want to listen to.\n\
When the account sends out a tweet, the program sends a desktop notification and the tweet will be displayed in the output widget\n\
\nUse the link to get the twitter ID of a username.\n", anchor='nw', wraplength=1000, justify='left')
entry = tk.Entry(root, textvariable=v, validate="key", width=30)

entry['validatecommand'] = (entry.register(test_val),'%P','%d')

label = tk.Label(root, text='Twitter id:')
listen_button = tk.Button(root, text="Listen")
quit = tk.Button(root, text="Quit and restart")
link = tk.Label(root, text=r"http://gettwitterid.com/", fg="blue", cursor="hand2")
output = tk.Text(root, width=80, height=20)

#Binding callbacks
listen_button.bind("<Button-1>", listen)
link.bind("<Button-1>", hyperlink)
quit.bind("<Button-1>", quit_listen)

#Placement
text.grid(row=0, column=0)
link.grid(row=1, column=0)
label.grid(row=2, column=0)
entry.grid(row=3, column=0)
listen_button.grid(row=4, column=0)
quit.grid(row=5, column=0)
output.grid(row=6, column=0)

#Start program
root.mainloop()
