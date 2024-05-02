import paramiko

# Configuration for SSH connection
ssh_config = {
    'hostname': 'example.com',  # Change to your server's hostname or IP
    'port': 22,                 # Default SSH port
    'username': 'your_username', # SSH username
    'password': 'your_password', # SSH password
}

# The payload to be executed on the remote server
payload = """
import os

# Example payload - Create a new file
with open("payload_test.txt", "w") as f:
    f.write("This is a test payload.\\n")
"""

# Connect to the remote server via SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**ssh_config)

# Send the payload as a Python script
payload_filename = "payload_script.py"
sftp_client = ssh_client.open_sftp()
with sftp_client.file(payload_filename, 'w') as remote_file:
    remote_file.write(payload)

# Execute the payload on the remote server
stdin, stdout, stderr = ssh_client.exec_command(f'python3 {payload_filename}')

# Wait for the command to complete
stdout.channel.recv_exit_status()

# Output the result of the payload execution
output = stdout.read().decode()
errors = stderr.read().decode()

print("Payload Output:", output)
print("Payload Errors:", errors)

# Clean up
sftp_client.remove(payload_filename)
sftp_client.close()
ssh_client.close()
