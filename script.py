import subprocess
from subprocess import DEVNULL

# Deleting previously created services
subprocess.Popen(['kubectl', 'delete', '-f', 'service1.yaml'], stdout=DEVNULL, stderr=DEVNULL)
subprocess.Popen(['kubectl', 'delete', '-f', 'service2.yaml'], stdout=DEVNULL, stderr=DEVNULL)

while(1):
	# Creating services almost at the same time
	p1 = subprocess.Popen(['kubectl', 'apply', '-f', 'service1.yaml'], stdout=DEVNULL, stderr=DEVNULL)
	p2 = subprocess.Popen(['kubectl', 'apply', '-f', 'service2.yaml'], stdout=DEVNULL, stderr=DEVNULL)
	p1.communicate()[0]
	p2.communicate()[0]

	# Check if flaw was exploited
	if (p1.returncode == 0 and p2.returncode == 0):
		print("Both services running simultaneously, breaking.")
		print("Kubectl output:")
		subprocess.run(['kubectl', 'get', 'services'])
		break
	else:
		print("Services creation prevented thanks to OPA policy. Deleting and retrying.")
	        # Deleting previously created services
		subprocess.Popen(['kubectl', 'delete', '-f', 'service1.yaml'], stdout=DEVNULL, stderr=DEVNULL)
		subprocess.Popen(['kubectl', 'delete', '-f', 'service2.yaml'], stdout=DEVNULL, stderr=DEVNULL)
