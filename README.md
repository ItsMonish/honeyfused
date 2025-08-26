# Honeyfused
HoneyFiles is a Python-based application designed for Linux systems as a means of real time intrusion detection. It leverages FUSE (Filesystem in Userspace) bindings to create and mount decoy files in sensitive directories commonly targeted by infostealers. Whenever these decoy files are accessed, modified or deleted the application puts out an alert, acting as a lightweight intrusion detection system to detect unauthorized access or malicious activity. Note that, the said alerts are just logs, one would have to set up `watch` command on the log file or log aggregation software to generate actual alerts.

Currently supported decoy files include:
- Kubernetes (`kubeconfig`)
- AWS (`~/.aws/credentials, config`)
- Azure (`credentials.json`)
- GCP (`application_default_credentials.json`)
- Docker (`config.json`)
- Terraform (`credentials.tfrc.json, .terraform.lock.hcl`)
- Bitcoin (`bitcoin.conf`)

# Usage
- Clone the repository
```bash
git clone https://github.com/ItsMonish/honeyfused
```
- Install required python modules
```bash
pip install -r requirements.txt
```
- Use `config.yml` to specify what decoy files to be generated and how many of them to be mounted at a time.
- Then start the application using:
```bash
python main.py --out <your log file>
```

## Notes:
- Make sure to select decoy file applications that you don't already have on the system.
- You have to set up some monitoring on the log file for real time alerts
- This is a project meant for tinkering and experimentation.
- *It’s not a replacement for proper monitoring or intrusion detection*

