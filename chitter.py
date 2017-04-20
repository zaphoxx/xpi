__colorize__=True
__gDebug__=False
__gInfo__=False
try:
	import colorama
	from colorama import Fore,Style,Back
	colorama.init()
except Exception as e:
	print("[!] Could not import 'colorama' module.")
	print("[!] {}".format(e))
	__colorize__=False
	pass
else:
	__colorize__=True

def post(message):
	msg="{}".format(message)
	if __colorize__:
		msg="{}{}{}{}".format(Fore.GREEN,Style.BRIGHT,msg,Fore.RESET)
	print(msg)
	
def fatal(functionname,message,error):
	msg="{} '{}()':{}".format("[ERROR]",functionname,error)
	msg+="\n{} {}".format("[!]",message)
	if __colorize__:
		msg="{}{}{}{}".format(Fore.RED,Style.BRIGHT,msg,Fore.RESET)
	print(msg)

def debug(message):
	if(__gDebug__):
		msg="{} {}".format("[DEBUG]",message)
		if __colorize__:
			msg="{}{}{}{}".format(Fore.YELLOW,Style.BRIGHT,msg,Fore.RESET)
		print(msg)

def info(message):
	if __gInfo__:
		msg="{} {}".format("[+]",message)
		if __colorize__:
			msg="{}{}{}{}".format(Fore.WHITE,Style.NORMAL,msg,Fore.RESET)
		print(msg)

def status(message):
	msg="{} {}".format("[STATUS]",message)
	if __colorize__:
		msg="{}{}{}{}".format(Fore.CYAN,Style.BRIGHT,msg,Fore.RESET)
	print(msg)
	
def warn(message):
	msg="{} {}".format("[WARNING]",message)
	if __colorize__:
		msg="{}{}{}{}".format(Fore.YELLOW,Style.BRIGHT,msg,Fore.RESET)
	print(msg)
	