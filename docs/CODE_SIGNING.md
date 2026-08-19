# WINDOWS CODE SIGNING SPECIFICATION — SK AI 4.0

**Platform Version:** Jarvis Platform V5.0  
**Publisher:** SK Enterprises (Sumeet Kumar)  

---

## 1. PURPOSE

Code signing authenticates the publisher identity and verifies that the executable has not been tampered with or corrupted during distribution. On Windows, valid EV (Extended Validation) or Standard OV Code Signing certificates eliminate SmartScreen warnings.

---

## 2. SIGNING PROCESS WITH SIGNTOOL

To sign the standalone executable and installer binary using Microsoft `signtool.exe`:

```powershell
# Set path to Microsoft Windows SDK signtool.exe
$SignTool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"

# Sign standalone executable
& $SignTool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "dist\SK_AI_4.0\SK_AI_4.0.exe"

# Sign installer setup binary
& $SignTool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "release\SK_AI_4.0_Setup_x64_v5.0.0.exe"
```

---

## 3. SIGNATURE VERIFICATION

To verify code signature validity and RFC 3161 timestamping:

```powershell
& $SignTool verify /pa /v "dist\SK_AI_4.0\SK_AI_4.0.exe"
```

---

## 4. SECURITY COMPLIANCE RULES

1. **Never commit PFX certificates or private signing keys** to version control.
2. Store signing credentials strictly in Hardware Security Modules (HSM) or CI/CD Key Vaults (e.g. Azure Key Vault / GitHub Encrypted Secrets).
