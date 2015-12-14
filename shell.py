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
		
def execute(lis):
	for cmd in range(len(lis)):
		if lis[cmd] == '<':
			in_redir(lis)
			break
		if lis[cmd] == '>':
			out_redir(lis)
			break
		if lis[cmd] == '|':
			print "pipe"
			break


def out_redir(command):
	''' Output redirection- Write output to a file'''
	std_out = os.dup(1)
	cmd = []
	for index in range(len(command)):
		if command[index] == '>':
			cmd = command[:index]
			fil = command[index+1]
			break
	fd = os.open( fil,os.O_WRONLY|os.O_CREAT)
	os.dup2(fd,1)
	if os.fork() ==0:
		try:
			err=os.execvp(cmd[0],cmd)
		except OSError:
				print command[0], ":command not found\n"
				sys.exit()
	os.wait()
	os.close(fd)
	os.dup2(std_out,1)
	return

def in_redir(command):
	''' Input redirection- Read input from a file'''
	std_out = os.dup(1)
	std_in=os.dup(0)
	for index in range(len(command)):
		if command[index] == '<':
			cmd = command[:index]
			fil = command[index+1]
			break
	fd = os.open( fil,os.O_RDONLY)
	os.dup2(fd,0)
	if os.fork() ==0:
		try:
			err=os.execvp(cmd[0],cmd)
		except OSError:
				print command[0], ":command not found\n"
				sys.exit()
	os.wait()
	os.close(fd)
	os.dup2(std_out,1)
	os.dup2(std_in,0)
	return


def shell(prompt ="$"):
	'''Shell'''	
	while True:
		input_command = raw_input(prompt)
		command = input_command.split()
		check = redir_check(command)
		if check:
			execute(command)
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
