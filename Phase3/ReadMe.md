# Phase 3: Defensive Strategy Proposal

This phase focuses on implementing and validating a defensive strategy to mitigate the ProFTPD vulnerability exploited in Phase 1.

## 🛡️ Chosen Defense Mechanism: Disabling `mod_copy`

The vulnerability exploited in Phase 1 (CVE-2015-3306) relies on the `mod_copy` module in ProFTPD 1.3.5. This module allows unauthenticated users to copy files using the `SITE CPFR` and `SITE CPTO` commands, which was leveraged to upload the malicious PHP shell to the web server directory.

The most direct and effective defense is to disable the `mod_copy` module entirely within the ProFTPD configuration.

## ⚙️ Implementation Steps

Implementing this defense requires modifying the ProFTPD configuration file (`proftpd.conf`) on the victim machine (Metasploitable3).

1.  **Locate the Configuration File:** The ProFTPD configuration file is typically located at `/etc/proftpd/proftpd.conf` or `/etc/proftpd.conf`.

2.  **Edit the Configuration File:** Open the file using a text editor with root privileges (e.g., `sudo nano /etc/proftpd/proftpd.conf`).

3.  **Disable `mod_copy`:** Find the line that loads the `mod_copy` module. This line might look similar to `LoadModule mod_copy.c`. Comment out this line by adding a `#` at the beginning:
    ```
    # LoadModule mod_copy.c
    ```
    Alternatively, if the module is loaded within a conditional block like `<IfModule mod_copy.c>`, you can comment out the entire block:
    ```
    # <IfModule mod_copy.c>
    #   # Configuration specific to mod_copy
    # </IfModule>
    ```
    *Note: The exact syntax might vary slightly depending on the specific ProFTPD setup.* 

4.  **Save and Close:** Save the changes to the configuration file and exit the editor.

5.  **Restart ProFTPD Service:** Apply the changes by restarting the ProFTPD service. The command to restart the service usually is:
    ```bash
    sudo service proftpd restart
    ```
    or
    ```bash
    sudo /etc/init.d/proftpd restart
    ```

## 🧪 Testing and Validation

To validate the effectiveness of the defense, the original attack script from Phase 1 must be rerun against the hardened victim machine.

1.  **Rerun Attack Script:** Execute the Python script (`script.py`) from the Phase 1 directory on the attacker machine (Kali Linux):
    ```bash
    python3 /path/to/Phase1/script.py
    ```

2.  **Expected Outcome:** With `mod_copy` disabled, the script should fail to upload the `exploit.php` file. The FTP commands `SITE CPFR` and `SITE CPTO` will no longer be recognized or permitted, preventing the core mechanism of the exploit.

## 📊 Before-and-After Comparison

This section demonstrates the security improvement by comparing the system's state before and after applying the defense.

**Before Defense (Phase 1):**
- The attack script successfully uploads `exploit.php` using `mod_copy`.
- A reverse shell connection is established.

*Placeholder for Screenshot: Successful exploit execution from Phase 1.*
```
[Insert Screenshot from Phase 1 showing successful exploit execution, e.g., reverse shell connection or file upload confirmation]
```

**After Defense (Phase 3):**
- The attack script fails because the `SITE CPFR` and `SITE CPTO` commands are disabled.
- The `exploit.php` file is not uploaded to the web server.
- No reverse shell connection can be established via this exploit vector.

*Placeholder for Screenshot: Failed exploit attempt after applying defense.*
```
[Insert Screenshot showing the Phase 1 script failing after the defense is applied, e.g., FTP command errors or script failure message]
```

## ✅ Conclusion

Disabling the `mod_copy` module in the ProFTPD configuration effectively mitigates the CVE-2015-3306 vulnerability exploited in Phase 1. Rerunning the attack script confirms that the defense prevents the malicious file upload, thereby securing the service against this specific exploit.
