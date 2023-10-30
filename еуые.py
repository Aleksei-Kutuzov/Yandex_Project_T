import paramiko

host = '188.225.40.140'
user = 'cz31021'
password = 'e36WQ#9S3nl1'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, port=port)
stdin, stdout, stderr = client.exec_command('python3 python_programms/connect.py')
data = stdout.read() + stderr.read()
client.close()
strings = data.decode('ascii').strip("\n")
string1 = strings.split("\n")[1:-2][0][1:-1]
print(dict(subString.split(":") for subString in string1.split(", ")))