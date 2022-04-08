from urllib.parse import unquote
import socket
import datetime

class Info:
	types = {
		0: "Info",
		1: "Revision",
		2: "Manifest"
	}
	def __init__(self, data, types):
		if types == 0:
			# Info
			self.version =			 data.get("version")
			self.mode =				 data.get("mode")
			self.can_respawn = 		 data.get("respawn")
			self.can_enter =		 data.get("enter")
			self.can_vote = 		 data.get("vote")
			self.ai = 				 data.get("ai")
			self.host = 			 data.get("Host")
			self.players_num =		 data.get("players")
			self.station_time =		 data.get("stationtime")
			self.round_duration =	 data.get("roundduration")
			self.round_time =		 data.get("roundtime")
			self.map =				 data.get("map")
			self.ticker_state =		 data.get("ticker_state")
			self.admins_num =		 data.get("admins")
			self.players =			 data.get("playerlist").split("\n") if data.get("playerlist") else None
			self.admins =			 data.get("adminlist")
			self.active_players = 	 data.get("active_players")
		elif types == 1:
			# Revision
			self.gameid =			 data.get("gameid")
			self.dm_version =		 data.get("dm_version")
			self.dm_build =			 data.get("dm_build")
			self.dd_verion =		 data.get("dd_version")
			self.dd_build =			 data.get("dd_build")
			self.revision =			 data.get("revision")
			self.git_branch =		 data.get("branch")
			self.date =				 data.get("date")
		elif types == 2:
			# Manifest
			self.manifest = {}
			for k, v in data.items():
				self.manifest[k] = []
				peoples = v.split("\n")
				for i in peoples:
					name, role = i.split(", ")
					self.manifest[k].append({name: role})

			# self.manifest = data
		self.raw_data = data
		self.type = self.types[types]
		self.rdp = False

	def __str__(self) -> str:
		if self.rdp: return str(self.raw_data)
		return f"<ByondAPI.Info by {self.type}>"


class BAPImeta:
	set_names = {
		"heads": "Command",
		"spt": "Command Support",
		"sec": "Security",
		"med": "Medical",
		"sci": "Science",
		"chr": "Church",
		"exp": "Expedition",
		"car": "Cargo",
		"sup": "Supply",
		"eng": "Engineering",
		"srv": "Service",
		"civ": "Miscellaneous",
		"bot": "Synthetic",
	}
	exceptions = {
		"storyteller": "Выбирается...",
		"playerlist": "Ой ой, а тут пусто!"
	}
	fields = {
		"status": {
			"eris": {
				"storyteller": "Story teller",
				"shiptime": "Station time"
			},
			"bay": {
				"mode": "Gamemode",
				"map": "Map",
				"stationtime": "Station time"
			},
		},
		"revision": {
			"eris": {
			},
			"bay": {
				"gameid": "Game id",
				"dm_version": "DM version",
				"dm_build": "DM build",
				"dd_version": "DD version",
				"dd_build": "DD build"
			}  
		},
	}

	replacements = {
		"%3a": ":",
		"+": " ",
		"%2b": " ",
		"%3d": ", ",
		"%26": "\n",
		"%2526%252339%253b": "'"
	}

class ByondAPI(BAPImeta):
	def __init__(self):
		self.servers		=	{} # {"servername" = ("domen", port:int)}
		self.comm_tokens	=	{} # {"servername" = "token"}

	def add_server(self, name: str, data: tuple):
		if len(data) != 2 or not isinstance(data[0], str) or not isinstance(data[1], int): raise TypeError("Wrong type of data. Awaited: (\"ip\", port)")
		if not name: raise TypeError("Empty server name.")
		if name in self.servers: raise NameError("Trying to add already added server name.")
		self.servers[name] = data
		return True

	def edit_server(self, name: str, data: tuple):
		if len(data) != 2 or not isinstance(data[0], str) or not isinstance(data[1], int): raise TypeError("Wrong type of data. Awaited: (\"ip\", port)")
		if not name: raise TypeError("Empty server name.")
		if name not in self.servers: raise NameError(f"Server with name \"{name}\" dosn't exist.")
		self.servers[name] = data
		return True

	def __do_command(self, server, cmd:str):
		if not server: raise TypeError("Empty server name.")
		return self.__decode_byond(self.__send_recieve_data(server, cmd))

	def get_server_revision(self, server:str=None):
		return Info(self.__do_command(server, "revision"), 1)

	def get_server_info(self, server:str=None):
		return Info(self.__do_command(server, "status=2"), 0)

	def get_server_manifest(self, server:str=None):
		return Info(self.__do_command(server, "manifest"), 2)

	def __prepare_packet(self, server, data):
		if server in self.comm_tokens: data += "&key="+self.comm_tokens[server]
		return bytes([0x00, 0x83, 0x00, len(data)+7, 0x00, 0x00, 0x00, 0x00, 0x00, 63, *map(ord, data), 0x00])

	def __send_recieve_data(self, server, command):
		if server not in self.servers: raise TypeError(f"Server with name \"{server}\" dosn't exist.")

		sock = socket.socket()
		try:
			sock.connect(self.servers[server])
		except ConnectionRefusedError:
			return None
		dat = self.__prepare_packet(server, command)
		sock.send(dat)
		dbuff = sock.recv(10240)
		sock.close()
		return dbuff

	def __decode_byond(self, data=None):
		if not data: return None

		data = "".join([chr(x) for x in data[5:-1]])
		for k, v in self.replacements.items():
			data = data.replace(k, v)
		data = data.split("&")

		ndat = {}
		for i in data:
			j = i.split("=")
			if(j[0]=="adminlist" and len(j[1])>0):
				adms = j[1].split("\n")
				admin_list = {}
				for k in adms:
					l = k.split(", ")
					admin_list[l[0]] = unquote(unquote(l[1]))

				ndat["adminlist"] = admin_list
			elif(len(j)-1):
				ndat[j[0]] = j[1]
			else:
				ndat[j[0]] = None
		return ndat

	def __str__(self) -> str:
		return f"<ByondAPI servers={self.servers.keys()}>"