// Jenkinsfile: the Jenkins pipeline for Task Tracker
pipeline {
  // Run on any available Jenkins machine; here, the Jenkins server itself
  agent any
 
  // Check GitHub for new commits about every 5 minutes
  triggers {
    pollSCM('H/5 * * * *')
  }
 
  // Values that every stage can use
  environment {
    COVERAGE_MIN = '80'
    // Read the secret text credential whose ID is demo-token
    DEMO_TOKEN = credentials('demo-token')
  }
 
  stages {
    // Create a virtual environment and install the tools
    stage('Set up') {
      steps {
        sh 'python3 -m venv .venv'
        sh '.venv/bin/pip install -r requirements.txt'
      }
    }
 
    // Lint and Test run at the same time, in parallel
    stage('Quality checks') {
      parallel {
        stage('Lint') {
          steps {
            sh '.venv/bin/ruff check .'
          }
        }
        stage('Test') {
          steps {
            sh '''
              .venv/bin/python -m pytest -v --cov=app \\
                --cov-report=term-missing --cov-fail-under=$COVERAGE_MIN
            '''
          }
        }
      }
    }
 
    // Build the versioned artifact once, as in Labs 6 and 7
    stage('Package') {
      steps {
        sh '''
          VERSION=$(sed -n 's/^VERSION = "\\(.*\\)"$/\\1/p' app.py)
          ARTIFACT="task-tracker-${VERSION}-${GIT_COMMIT:0:7}.tar.gz"
          rm -rf dist
          mkdir dist
          tar -czf "dist/$ARTIFACT" app.py
          (cd dist && sha256sum "$ARTIFACT" > "$ARTIFACT.sha256")
          ls -l dist
        '''
        // Keep the artifact with this build in Jenkins
        archiveArtifacts artifacts: 'dist/*', fingerprint: true
      }
    }
 
    // Jenkins hides credential values in the log; never print a real secret
    stage('Show how Jenkins protects a secret') {
      steps {
        sh 'echo "The token has ${#DEMO_TOKEN} characters and is $DEMO_TOKEN"'
      }
    }
 
    // Continuous delivery: a person decides to release
    stage('Approve release') {
      steps {
        timeout(time: 15, unit: 'MINUTES') {
          input message: 'Release this build of Task Tracker?', ok: 'Release'
        }
      }
    }
 
    stage('Release') {
      steps {
        echo "Release approved for build ${env.BUILD_NUMBER}"
      }
    }
  }
 
  // Runs after all the stages, depending on the result
  post {
    success {
      echo 'Pipeline passed: Task Tracker is released.'
    }
    failure {
      echo 'Pipeline failed: open the stage that failed and read its log.'
    }
    always {
      echo "Build ${env.BUILD_NUMBER} result: ${currentBuild.currentResult}"
    }
  }
}
