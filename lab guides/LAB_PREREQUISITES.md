# Lab Prerequisites

Use this checklist before starting the lab.

## 1) Download and verify Visual Studio Code (free)
- Download: https://code.visualstudio.com/
- Install VS Code and open the app.
- Open any folder and create a test file to confirm the editor works.

## 2) First-time Python setup (if you are new to VS Code/Python)
If this is your first time using Visual Studio Code for Python labs, install Python and pip first.

- Download Python 3.10+ from: https://www.python.org/downloads/
- During installation, select Add Python to PATH.
- Open a new terminal and verify:
	- Preferred (inside VS Code, after Step 1):
		1. Open VS Code.
		2. Select Terminal > New Terminal from the top menu.
		3. A terminal panel opens at the bottom (PowerShell by default on Windows).
	- Alternative (Windows, without VS Code):
		1. Press Windows key.
		2. Type PowerShell.
		3. Select Windows PowerShell.
	- `python --version`
	- `python -m pip --version`
- (Recommended) Upgrade pip:
	- `python -m pip install --upgrade pip`

## 3) Create a Microsoft personal account
- Go to: https://account.microsoft.com/account
- Select Create one and finish sign-up.
- Verify your email and sign in successfully.

## 4) Create an Azure Free Account using that Microsoft account
- Go to: https://azure.microsoft.com/free/
- Sign in with your Microsoft personal account.
- Complete phone/card identity verification to activate the free account.

Important note about credit card charges (per Microsoft documentation):
- Microsoft states your card is used for identity verification for the Azure free account.
- You are not charged unless you explicitly upgrade/convert to pay-as-you-go or use billable services beyond free limits.
- Official reference: https://learn.microsoft.com/azure/cost-management-billing/manage/avoid-charges-free-account

## 5) Verify access in Azure Portal and Microsoft Foundry
- Azure Portal: https://portal.azure.com
- Microsoft Foundry: https://ai.azure.com
- Sign in and confirm both portals open without access errors.

## 6) Create a GitHub account and verify access
- Go to: https://github.com/signup
- Create your account and verify email.
- Sign in at: https://github.com and confirm your dashboard loads.

## 7) Create a local folder and clone the lab repository
- Open PowerShell and move to a location where you keep projects.
- Create a parent folder and enter it:
	- `mkdir anuraguni-labs`
	- `cd anuraguni-labs`
- Clone the repository:
	- `git clone https://github.com/anuragunidemo/labs.git`
- Enter the cloned lab root folder:
	- `cd labs`

## 8) Run the startup script (creates virtual env + installs dependencies)
From the cloned lab root folder, run:

- `. .\startup_lab.ps1`

What this script does:
- Creates a local virtual environment named `.venv` (if it does not exist).
- Upgrades pip inside `.venv`.
- Activates `.venv` in script scope.
- Installs all dependencies from `requirements.txt`.
- Prints the activation status and ready message.

**Setup Duration:**
- **First run: 5–10 minutes** (resolves and downloads all dependencies)
  - This is normal. Python packages have many transitive dependencies (e.g., azure-ai-evaluation pulls ~10+ Azure SDK packages).
  - Keep the terminal open and monitor the output. You will see package download and install messages.
  - When you see `[Done] Lab environment is ready.`, setup is complete.
- **Subsequent runs: < 1 minute** (pip uses cached wheels)

**How to monitor:**
- Look for lines like `Collecting package-name...`, `Installing collected packages...`, and `Successfully installed...`
- Do not close the terminal or interrupt the script (Ctrl+C).
- If the script stalls for > 5 minutes without output, it may be stuck; check your internet connection and restart.

Then activate the environment:
- `.\.venv\Scripts\Activate.ps1`

Tip:
- To keep `.venv` active in your current terminal after setup, run with dot-sourcing:
	- `. .\startup_lab.ps1`

---

## Quick Completion Checklist
- [ ] VS Code installed and working
- [ ] Python 3.10+ and pip installed
- [ ] Microsoft personal account created and verified
- [ ] Azure Free Account activated
- [ ] Azure Portal opens successfully
- [ ] Microsoft Foundry opens successfully
- [ ] GitHub account created and accessible
- [ ] `anuragunidemo/labs` cloned locally
- [ ] `. .\startup_lab.ps1` completed successfully
