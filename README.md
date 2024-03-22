# air-gapped-backups
Python script and instructions how to set up an air-gapped vault in AWS for malware protected backups.  
The script supports configurations for different environments (dev, test, qa, prod) - script and logging configs.  
The script can be manually run or set up to run automatically with cron job. If automatic, the file need to be removed 
or deleted between runs to avoid multiple version of the same file in S3. 

To set up AWS with an air-gapped account, read more in [docs](docs/Home.md).

![](docs/img/AWS_Air-Gapped_Vault_v1.png)

## Python support
Recommended Python ≥ 3.10

## Limitations
* A file with the same name will be added as a new version of the file in S3, even if it is exactly the same file.
* The script does not remove the copied file -> Running the script more then once will create a additional versions.
* The bucket set up in Compliance mode, i.e. "write only - automatic delete" so an uploaded file can not be manually deleted. 

## Recommended Python setup
1. Install you global Python, the latest version.
2. Install virtualenv so you have needed dependencies for this script seperated, not in your global python installation.
3. Create a virtual environment in your project root folder.
4. Activate your virtual environment.
5. Install dependencies (see below)

## Set up and run the script 
1. Install needed packages: `pip install -r requirements.txt`
2. Add an `.env` file in the project root stating your environment (dev, test, qa, prod):  
   ```ENV=dev```  
   This is used for the path to config files: `<env>-config,json`, `<env>-secrets` and `<env>-logging-config.json`
3. Copy the example files in `config/`, remove `_example` and add your values to the stated keys.
4. Run the script with the following parameters: `"/Path/to/local/directory" "FileInDirectory.txt" "FolderInS3"`
   1. First: path to local directory.
   2. Backup file name in the above directory.
   3. Name of the folder in S3 where to store the file.
