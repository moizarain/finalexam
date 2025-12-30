pipeline {
    agent any
    
    // Environment variables
    environment {
        PYTHON_PATH = 'python'
        DEPLOY_DIR = 'C:\\deploy\\flask_app'
    }
    
    // Trigger on GitHub push (webhook)
    triggers {
        githubPush()
    }
    
    stages {
        // Stage 1: Clone Repository
        stage('Clone Repository') {
            steps {
                echo '=========================================='
                echo 'Stage 1: Cloning Repository from GitHub'
                echo '=========================================='
                
                // Clean workspace and clone repository explicitly
                bat '''
                    if exist ".git" rmdir /s /q .git
                    if exist "app.py" del /q *.py
                    git clone https://github.com/moizarain/finalexam.git .
                '''
                
                echo 'Repository cloned successfully!'
            }
        }
        
        // Stage 2: Install Dependencies
        stage('Install Dependencies') {
            steps {
                echo '=========================================='
                echo 'Stage 2: Installing Python Dependencies'
                echo '=========================================='
                
                // Create virtual environment
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                
                echo 'Dependencies installed successfully!'
            }
        }
        
        // Stage 3: Run Unit Tests
        stage('Run Unit Tests') {
            steps {
                echo '=========================================='
                echo 'Stage 3: Running Unit Tests with pytest'
                echo '=========================================='
                
                bat '''
                    call venv\\Scripts\\activate
                    pytest test_app.py -v --tb=short --junitxml=test-results.xml
                '''
                
                echo 'Unit tests completed!'
            }
            post {
                always {
                    // Publish test results
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }
        
        // Stage 4: Build Application
        stage('Build Application') {
            steps {
                echo '=========================================='
                echo 'Stage 4: Building/Packaging Application'
                echo '=========================================='
                
                // Create build directory and package application
                bat '''
                    if not exist "build" mkdir build
                    
                    REM Copy application files to build directory
                    copy app.py build\\
                    copy requirements.txt build\\
                    
                    REM Create version file
                    echo Build Version: 1.0.0 > build\\VERSION.txt
                    echo Build Date: %DATE% %TIME% >> build\\VERSION.txt
                    echo Build Number: %BUILD_NUMBER% >> build\\VERSION.txt
                '''
                
                // Archive build artifacts
                archiveArtifacts artifacts: 'build/**/*', fingerprint: true
                
                echo 'Application packaged successfully!'
            }
        }
        
        // Stage 5: Deploy Application
        stage('Deploy Application') {
            steps {
                echo '=========================================='
                echo 'Stage 5: Deploying Application'
                echo '=========================================='
                
                bat '''
                    REM Create deployment directory if it doesn't exist
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    
                    REM Copy build files to deployment directory
                    xcopy /E /Y /I build\\* "%DEPLOY_DIR%\\"
                    
                    REM Create deployment marker
                    echo Deployed on: %DATE% %TIME% > "%DEPLOY_DIR%\\DEPLOYED.txt"
                    echo Build Number: %BUILD_NUMBER% >> "%DEPLOY_DIR%\\DEPLOYED.txt"
                    
                    echo.
                    echo ==========================================
                    echo Deployment Summary:
                    echo ==========================================
                    echo Deployed to: %DEPLOY_DIR%
                    echo.
                    dir "%DEPLOY_DIR%"
                '''
                
                echo 'Application deployed successfully!'
            }
        }
    }
    
    // Post-build actions
    post {
        success {
            echo '=========================================='
            echo 'PIPELINE COMPLETED SUCCESSFULLY!'
            echo '=========================================='
            echo "Build #${BUILD_NUMBER} passed all stages"
        }
        failure {
            echo '=========================================='
            echo 'PIPELINE FAILED!'
            echo '=========================================='
            echo "Build #${BUILD_NUMBER} failed - check logs for details"
        }
        always {
            echo 'Pipeline execution completed.'
            // Clean up virtual environment
            bat 'if exist "venv" rmdir /s /q venv'
        }
    }
}
