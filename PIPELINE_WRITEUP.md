# Jenkins CI/CD Pipeline Write-Up

## Project Overview

This document provides a detailed explanation of the Jenkins CI/CD pipeline created for automating the build, test, and deployment process of a Flask web application. The pipeline is defined in a `Jenkinsfile` and consists of five main stages.

---

## Pipeline Stages Explanation

### Stage 1: Clone Repository

**Purpose:** Pull the latest code from the GitHub repository.

**What it does:**
- Cleans the Jenkins workspace to ensure a fresh start
- Uses the `checkout scm` command to clone the repository configured in the Jenkins job
- The GitHub plugin enables Jenkins to pull code from the specified repository

**Commands Used:**
```groovy
cleanWs()
checkout scm
```

**Why it's important:** This ensures Jenkins always works with the most recent version of the codebase, preventing issues from stale code.

---

### Stage 2: Install Dependencies

**Purpose:** Install all required Python packages for the application.

**What it does:**
- Creates a Python virtual environment (`venv`) for isolation
- Upgrades pip to the latest version
- Installs all packages listed in `requirements.txt`

**Commands Used:**
```batch
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies Installed:**
- Flask 2.3.3 - Web framework
- pytest 7.4.3 - Testing framework
- pytest-cov 4.1.0 - Test coverage reporting
- python-dotenv 1.0.0 - Environment variable management

**Why it's important:** Using a virtual environment ensures consistent dependencies across builds and prevents conflicts with system-wide packages.

---

### Stage 3: Run Unit Tests

**Purpose:** Execute automated tests to verify application functionality.

**What it does:**
- Activates the virtual environment
- Runs pytest with verbose output
- Generates a JUnit-compatible XML report for Jenkins
- Publishes test results in Jenkins UI

**Commands Used:**
```batch
call venv\Scripts\activate
pytest test_app.py -v --tb=short --junitxml=test-results.xml
```

**Tests Executed:**
- Home route tests (status code, content)
- Health endpoint tests (JSON response validation)
- API data endpoint tests (structure, content)
- API status endpoint tests
- Invalid route handling (404 responses)

**Why it's important:** Automated tests catch bugs early in the development cycle, ensuring code quality before deployment.

---

### Stage 4: Build Application

**Purpose:** Package the application for deployment.

**What it does:**
- Creates a `build` directory
- Copies application files to the build directory
- Generates a VERSION.txt file with build metadata
- Archives build artifacts for future reference

**Commands Used:**
```batch
mkdir build
copy app.py build\
copy requirements.txt build\
echo Build Version: 1.0.0 > build\VERSION.txt
```

**Artifacts Archived:**
- `app.py` - Main application file
- `requirements.txt` - Dependencies file
- `VERSION.txt` - Build version information

**Why it's important:** Build artifacts provide a deployable package and maintain a history of what was deployed.

---

### Stage 5: Deploy Application

**Purpose:** Deploy the application to the target environment.

**What it does:**
- Creates the deployment directory (`C:\deploy\flask_app`) if it doesn't exist
- Copies build files to the deployment directory
- Creates a deployment marker file with timestamp
- Displays deployment summary

**Commands Used:**
```batch
mkdir "%DEPLOY_DIR%"
xcopy /E /Y /I build\* "%DEPLOY_DIR%\"
echo Deployed on: %DATE% %TIME% > "%DEPLOY_DIR%\DEPLOYED.txt"
```

**Note:** This is a simulated deployment. In a production environment, this stage would typically:
- Deploy to a cloud server (AWS, Azure, GCP)
- Restart the application service
- Update a load balancer
- Perform health checks

**Why it's important:** Automating deployment reduces manual errors and ensures consistent deployment procedures.

---

## Pipeline Triggers

The pipeline is configured to trigger automatically when:
1. **GitHub Webhook:** Changes are pushed to the repository
2. **Manual Trigger:** Build Now button in Jenkins

```groovy
triggers {
    githubPush()
}
```

---

## Post-Build Actions

The pipeline includes post-build actions that execute regardless of build outcome:

- **On Success:** Displays success message with build number
- **On Failure:** Displays failure message prompting log review
- **Always:** Cleans up the virtual environment

---

## Required Jenkins Plugins

1. **Git Plugin** - For Git repository operations
2. **Pipeline Plugin** - For declarative pipeline support
3. **GitHub Plugin** - For GitHub integration and webhooks
4. **JUnit Plugin** - For test result publishing

---

## GitHub Repository Setup Instructions

### GitHub Repository

**Repository URL:** [https://github.com/moizarain/finalexam](https://github.com/moizarain/finalexam)

### Push Code (if not already pushed)
```bash
cd c:\Users\moiza\OneDrive\Desktop\i221704_SSD_Final
git init
git add .
git commit -m "Initial commit - Flask app with Jenkins pipeline"
git branch -M main
git remote add origin https://github.com/moizarain/finalexam.git
git push -u origin main
```

### Step 3: Configure Webhook (Optional)
1. Go to repository Settings → Webhooks
2. Add webhook: `http://YOUR_JENKINS_URL/github-webhook/`
3. Content type: `application/json`
4. Select: Just the push event

---

## Jenkins Job Configuration

### Creating the Pipeline Job

1. **New Item** → Enter name → Select "Pipeline"
2. **Configure:**
   - General: Check "GitHub project" and enter repository URL
   - Build Triggers: Check "GitHub hook trigger for GITScm polling"
   - Pipeline: 
     - Definition: "Pipeline script from SCM"
     - SCM: Git
     - Repository URL: Your GitHub repo URL
     - Credentials: Add GitHub credentials if private repo
     - Branch: `*/main`
     - Script Path: `Jenkinsfile`

3. **Save** and click **Build Now**

---

## Troubleshooting Common Issues

### Issue: Python not found
**Solution:** Ensure Python is installed and added to system PATH. Verify with `python --version`.

### Issue: pip install fails
**Solution:** Check internet connectivity. Verify `requirements.txt` has correct package names.

### Issue: Tests fail
**Solution:** Check test output in console. Ensure all test files are correctly named (`test_*.py`).

### Issue: Deployment directory access denied
**Solution:** Ensure Jenkins service account has write permissions to `C:\deploy\`.

### Issue: GitHub webhook not triggering
**Solution:** Verify webhook URL is correct and Jenkins is accessible from the internet.

---

## Files in Repository

| File | Description |
|------|-------------|
| `app.py` | Main Flask application with 4 routes |
| `requirements.txt` | Python dependencies |
| `test_app.py` | Unit tests using pytest |
| `.gitignore` | Git ignore patterns |
| `Jenkinsfile` | Jenkins pipeline definition |
| `PIPELINE_WRITEUP.md` | This documentation |

---

## Conclusion

This Jenkins pipeline provides a complete CI/CD solution for a Flask web application, automating the entire process from code checkout to deployment. The pipeline ensures code quality through automated testing and creates consistent, repeatable deployments.

The declarative pipeline syntax makes it easy to understand and modify the stages as project requirements evolve.
