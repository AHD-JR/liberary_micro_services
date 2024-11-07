def buidApp() {
    echo "Building the application..."
}

def testApp() {
    echo "Testing the application..."
}

def deployApp() {
    echo "Deploying the application..."
    echo "Application version ${params.VERSION}"
}

return this
