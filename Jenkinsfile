CODE_CHANGES =  getGitChanges() //Maybe a call to a groovy script that checks if changes have occured in the code

pipeline {
  
  agent any

  environment {
    NEW_VERSION = '1.3.0' // hard coded!
    SERVER_CREDENTIALS = credentials('GCP_SERVICE_ACCOUNT') //extracting creds from jenkins server using credentials-binding plugin
  }

  tools {
    maven "Maven"
    // provided Maven is installed in Jenkins as aplugin or via CLI
  }

  parameters {
    //string(name: 'VERSION', defaultValue: '', description: 'version to deploy on prod')
    choice(name: 'VERSION', choices: ['1.1.0', '1.2.0', '1.3.0'], description: '')
    booleanPAram(name: 'executeTests', defaultValue: true, description: '')
  }
  
  stages {

    stage("build") {
        when {
            expression {
                BRANCH_NAME == 'dev' && CODE_CHANGES == true
            }
        }
        steps {
            echo "Building the application..."
            echo "Application version ${NEW_VERSION}"
        }

    }

     stage("test") {
        when {
            expression {
                // BRANCH_NAME is an env provided by Jenkins. See all in jenkins_server/env-vars.html/
                params.executeTests && (BRANCH_NAME == 'dev' || BRANCH_NAME == 'master')
                //params.executeTests == true && (BRANCH_NAME == 'dev' || BRANCH_NAME == 'master')
            }
        }
        steps {
            echo "Testing the application..."
        }
      
    }

     stage("deploy") {

        steps {
            echo "Deploying the application..."
            echo "Server credentials ${SERVER_CREDENTIALS}"
            echo "Application version ${params.VERSION}"
        }
      
    }

  }
  
  post {
    always {
        echo "Execution has ended"
    }
    success {
        echo "All stages passed"
    }
    failure {
        echo "There is a failure!"
    }
  }
}
