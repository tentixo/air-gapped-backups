# Set up an air-gapped AWS account

## Background
The basis for air-gapping is to protect for content like backups from malicious actors - internal and external.  
By having a separate AWS account without network connectivity to any operational environment the backups are 
protected malware spreading over the network.  
To protect from disgruntled co-worker, not co-worker that has access to an organizational environment should 
have access to the air-gapped account. For smaller organization, handing over the keys to the vault to members 
in the board of directors is a good choice. For larger organization non-technical C-level executives would work.

## Best practice
### Separate DNS and domain
An AWS account can be, with an extensive process, be unlocked by access to the root account's email address.  
Our recommendation is to register a new domain with a separate DNS vendor. 

### MFA for root account and 2-head policy
In AWS you can only have one multi-factor authentication device, virtual (MFA app) or physical (YubiKey).  
The root account should serve as break glass account and never be used for administrative or backup retrieval purposes.  
With these requirements you have two choices for the root account protection: 
* Use physical MFA but then only have one break glass envelope. 
* Use virtual MFA and save two printed copies of the QR code and having two break glass envelope.

If you have only two Global Administrators we recommend the QR code option, if you have more than two, you can go for 
physical MFA.

To follow PoLP^2 (Principle of Least Privilege and Privilege of Least People) while still following 2-head policy, 
you need at least 2 global administrators but not more than 4.

## Set up AWS root, billing & notifications

### VPC Preparation

Before you sign up for AWS it is good to know the nature of AWS.

The account you sign up with is your SuperAdmin account - the account you use to set up your global admin users and then 
never use the root account again, unless in an emergency.

The best practice for root account:

* Should be kept in a break glass envelope in a secure location.
* Strong password (min 24 char).
* Multi-Factor Authentication - virtual or physical
* Email and potentially SMS notification to global admins when used.

Apart from the root account, AWS has three other contacts account to add:

* Billing
* Operations
* Security

### Preparation before sign-up

1. Select a new domain: `examplevault.com`
2. Select what email provider to use
3. Select share mailbox names for the root admin and base communication:
   1. root (name & email): `Cloud Admin cloud@examplevault.com`
   2. Billing: `billing@examplevault.com`
   3. Operations: `ops@examplevault.com`
   4. Security: `security@examplevault.com`
4. Decide what persons should be AWS Admins.
5. Choose what phone number should be used for the root account. Remember to change number in the off-boarding process!
6. Install an authenticator app on root user's phone.

### Step by step AWS account registration
1. Purchase and your domain and set up DNS.
2. Add the domain to your chosen email provider.
3. Add SPF, DKIM and DMARC records linked to your email provider the domain in the DNS.
4. Register at least one user with your new domain in your email provider.
5. Add the share email boxes and give your user access:
   1. root (name & email): `Cloud Admin cloud@examplevault.com`
   2. Billing: `billing@examplevault.com`
   3. Operations: `ops@examplevault.com`
   4. Security: `security@examplevault.com`
6. Send an email from a non-domain account to your `cloud@examplevault.com` to validate mail flow and read access for your domain user.
7. Sign up for a new AWS account: [https://portal.aws.amazon.com/billing/signup](https://portal.aws.amazon.com/billing/signup)
8. Retrieve the sent code to the `cloud@examplevault.com` mailbox to activate your account.
9. Add MFA to your root account.