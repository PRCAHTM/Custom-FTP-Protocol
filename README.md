# FTP Server Implementation and Network Analysis

This project was developed as part of the Data Communication Networks course.  
The goal was to deeply understand the FTP protocol by implementing it, analyzing its behavior at the packet level, securing it, and improving its performance through bandwidth control.

The project combines practical implementation with protocol-level analysis.

---

## Project Overview

This project includes:

- Implementation of a custom FTP client and server
- Theoretical analysis of FTP and alternative protocols
- Packet-level inspection using Wireshark
- Setting up a local FTP server on Ubuntu (vsftpd)
- Firewall configuration
- User isolation and directory control
- Securing FTP using SSL/TLS
- Bandwidth and transfer rate control

The objective was not only to use FTP, but to understand how it works internally and how to properly configure and secure it in a real environment.

---

## Part 1: Client and Server Implementation

A functional FTP client and server were implemented supporting:

- File upload (put)
- File download (get)
- Directory listing (ls)
- Multiple users
- Proper command handling

All required FTP commands were implemented and tested successfully.

---

## Part 2: FTP Protocol Understanding

### Comparison with Other File Transfer Protocols

FTP was compared with:

- SFTP (SSH File Transfer Protocol)
- FTPS (FTP over SSL/TLS)
- HTTP/HTTPS
- SMB

Key observations:

- Traditional FTP transfers data in plaintext (not secure).
- SFTP and FTPS provide encryption.
- HTTPS is widely used for secure web-based file transfers.
- SMB is more common in local network environments.

---

### Transport Layer Analysis

- FTP uses TCP as its transport protocol.
- TCP ensures reliable, ordered, and error-checked delivery.
- UDP is not suitable for file transfer due to lack of reliability.

---

### Active vs Passive Mode

Active Mode:
- Server initiates data connection.
- Problematic with firewalls and NAT.

Passive Mode:
- Client initiates all connections.
- More firewall-friendly and secure.

---

### Wireshark Analysis

File transfers were monitored using Wireshark:

- Local transfer showed maximum TCP packet size around 65549 bytes.
- Download from Sharif University FTP showed packet size around 1514 bytes.

The difference is due to Ethernet MTU limitations:

- Standard Ethernet MTU = 1500 bytes
- +14 bytes Ethernet header = 1514 bytes

This demonstrates how the data link layer constrains packet sizes in real networks.

---

## Part 3: Setting Up a Local FTP Server (Ubuntu)

A local FTP server was configured using vsftpd.

### Installation

```bash
sudo apt install vsftpd
```

### Configuration

Key configuration changes:

- Enabled local users
- Disabled anonymous login
- Enabled write access
- Enabled chroot jail

Users were created and tested successfully.

---

### Firewall Configuration

Firewall (UFW) was enabled and configured:

- Opened port 21 (control)
- Opened port 20 (data for active mode)

Reasons for firewall configuration:

- Prevent unauthorized access
- Ensure reliable FTP communication
- Protect against network abuse
- Manage traffic properly

---

### Changing Default Directory

User home directories were customized to:

- Restrict users to specific folders
- Improve organization
- Increase security through isolation (chroot jail)

File creation, deletion, and download were tested successfully.

---

## Part 4: Securing FTP (SSL/TLS)

FTP was secured using SSL/TLS encryption.

Steps included:

- Installing OpenSSL
- Generating SSL certificates
- Updating vsftpd configuration
- Restarting service

Why encryption is important:

- Protect usernames and passwords
- Prevent eavesdropping
- Ensure data integrity
- Prevent man-in-the-middle attacks
- Meet regulatory compliance requirements

Methods used to limit user access:

- Chroot jail
- Proper file permissions
- Command restrictions
- Account isolation

---

## Part 5: Bandwidth and Transfer Rate Control

The FTP implementation was extended to include bandwidth control.

Server-side changes:
- Converted bandwidth from KB/s to bytes/s
- Sent file in 1024-byte chunks
- Applied delay when transfer rate exceeded limit
- Displayed transfer progress and rate

Client-side changes:
- Calculated received bytes
- Displayed progress percentage
- Printed transfer rate in real time

---

### Example Test

A 10MB file was generated:

```bash
fallocate -l 10M testfile.txt
```

Transfer rate was limited to:

```
100 KB/s
```

Result:

Transfer time ≈ 100 seconds

(10MB) / (100KB/s) = 100 seconds

Both client and server displayed:

- Bytes transferred
- Percentage completed
- Transfer rate

This confirms that bandwidth throttling worked correctly.

---

## Key Concepts Demonstrated

- FTP protocol behavior
- TCP segmentation and MTU limitations
- Firewall configuration and port management
- Secure communication using SSL/TLS
- User isolation with chroot
- Real-time bandwidth throttling
- Network monitoring using Wireshark

---

## Technologies Used

- Python (FTP client/server implementation)
- Ubuntu Linux
- vsftpd
- OpenSSL
- UFW (Firewall)
- Wireshark
- Socket Programming

---

## Course Information

Data Communication Networks  
Sharif University of Technology  

---

## Author

Parsa Hatami
