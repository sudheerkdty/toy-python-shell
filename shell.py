import os
import subprocess
import sys

def redir_check(lis):
	'''To check for any redirection '''
	if '|' in lis:
		return True
	elif '>' in lis:
		return True
	elif '<' in lis:
		return True
	else:
		return False
		

def shell(prompt ="$"):
	'''Shell'''	
	while True:
		input_command = raw_input(prompt)
		command = input_command.split()
		check = redir_check(command)
		if check:
			print "Redirection is not implemented"
		if command[0] == 'exit':
			print 'Exit'
			return
		elif os.fork() == 0:
			try:
				err = os.execvp(command[0], command)
			except OSError:
				print command[0], ":command not found\n"
				sys.exit()
		os.wait()
	return	

def main():
	'''main'''
	shell()

if __name__ == '__main__':
	main()
