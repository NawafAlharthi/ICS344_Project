# Phase 3: Defensive Strategy Proposal

This phase documents the implementation and validation of a defensive strategy to mitigate the ProFTPD vulnerability (CVE-2015-3306) that was exploited in Phase 1.

## 🛡️ Vulnerability Overview

In Phase 1, the attacker exploited ProFTPD 1.3.5 using the mod_copy feature. This allowed unauthenticated users to upload a malicious PHP reverse shell by using the FTP commands SITE CPFR and SITE CPTO. The payload was written into the web server directory and triggered remotely.

## ⚙️ Defense Implementation

The installed version of ProFTPD on Metasploitable3 did not include mod_copy as a loadable module, meaning there was no LoadModule directive available to disable. Instead, the defense involved explicitly blocking the use of SITE CPFR and SITE CPTO within the configuration file.

The configuration file was located at:

/opt/proftpd/etc/proftpd.conf

The file was edited with the following lines appended to the bottom:

```
<Limit SITE_CPFR>
  DenyAll
</Limit>

<Limit SITE_CPTO>
  DenyAll
</Limit>
```

These blocks prevent ProFTPD from accepting those FTP commands, effectively disabling the exploit vector.

The changes were saved, and the service was restarted using the following command:
```
sudo /etc/init.d/proftpd restart
```


## 🧪 Testing and Validation

The original Python script used in Phase 1 was re-executed on the attacker machine. The script failed to upload exploit.php, and no payload appeared in the web server directory.

Metasploit was also used to attempt the same exploit. The exploit failed to deliver the payload and no shell session was created.

A Netcat listener was left running on the attacker's machine during both attempts. No reverse shell was received.

## 📊 Before-and-After Comparison

This section demonstrates the security improvement by comparing the system's state before and after applying the defense.

**Before Defense (Phase 1):**
the attacker was able to upload exploit.php using the FTP SITE commands. The file was successfully placed in the web root, and a reverse shell was opened.


*Placeholder for Screenshot: Successful exploit execution from Phase 1.*
```
[Insert Screenshot from Phase 1 showing successful exploit execution, e.g., reverse shell connection or file upload confirmation]
```

**After Defense (Phase 3):**
After applying the defense, the FTP server rejected the commands required to perform the exploit. The file was not uploaded and the reverse shell could not be established.

*Placeholder for Screenshot: Failed exploit attempt after applying defense.*
```
[Insert Screenshot showing the Phase 1 script failing after the defense is applied, e.g., FTP command errors or script failure message]
```

## ✅ Conclusion

By adding configuration limits to deny SITE_CPFR and SITE_CPTO, the vulnerability in ProFTPD was successfully mitigated. Both scripted and manual exploit attempts failed after the change. This confirms that the defense is effective and the system is no longer vulnerable through this vector.

















