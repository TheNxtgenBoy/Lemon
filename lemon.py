from requests import session, get
from time import sleep
from pytube import YouTube
import vlc, os, datetime

class Lemon():
	def __init__(self):
		self.switch = False
		self.session = session()
		self.Instance = vlc.Instance('--no-xlib -q')
		self.Instance.log_unset()
		print('\033[?25l', end="")
		self.player = self.Instance.media_player_new()
		self.Main_Loop()

	def Main_Loop(self):
		while True:
			os.system('cls')
			cmd = input('╔══Play@Lemon\n╚════•$: ')
			if cmd.strip() != '':
				print(f"[+] Searching : {cmd.strip()}")
				try:
					self.play(cmd.strip())
				except:
					self.player.stop()
					self.switch = False
			while self.switch == True:
				sleep(1)

	def play(self, query):
		query = query + ' lyrics'
		r = self.session.get(f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}')
		content = r.text[r.text.find('</script>'):]
		starting = content.find('videoId":"') + 10
		link = f'https://www.youtube.com/watch?v={content[starting:starting+11]}'
		content = content[starting+11:]
		starting = content.find('"title":{"runs":[{"text":"') + 26
		ending = content[starting:].find('"}],"accessibility"')
		name = content[starting:starting+ending].replace('\\u0026', '&')
		for i in ['(','[','|','official','full song','song']:
			name = name.lower().split(i)[0]
		for i in [' lyrics',' lyrical video', 'youtube', '\\"']:
			name = name.replace(i, '')
		print(f"[+] Found : {name}")
		self.youtube_link_fetch_from_url(link)

	def youtube_link_fetch_from_url(self, url):
		yt = YouTube(url)
		print('[+] Getting Ready')
		url = yt.streams.get_by_itag(251).url
		self.play_from_url(url)

	def play_from_url(self, url):
		self.switch = True
		Media = self.Instance.media_new(url)
		self.player.set_media(Media)
		self.player.play()
		total = 0
		while True:
			if self.player.get_length() > 0:
				total = self.player.get_length()
				break
			sleep(0.2)
		while self.switch == True:
			perct = int((self.player.get_time()/total)*50) + 1
			if perct > 50:
				break
			start = str(datetime.timedelta(milliseconds=self.player.get_time())).split('.')[0][2:]
			end = str(datetime.timedelta(milliseconds=total)).split('.')[0][2:]
			self.progress(perct, start, end)
			if self.player.is_playing() == 0:
				self.switch = False
			sleep(1)

	def progress(self, value, start, end):
		st = f'{start} : '
		for i in range(value):
			st += '•'
		for i in range(50-value):
			st += '-'
		print(f'{st} {end}\r',end="")

if __name__ == "__main__":
	Lemon()