pipeline {
  agent {
    kubernetes {
      label 'homeautomation'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: default
  containers:
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
"""
}
   }
  stages {
    stage('Clone') {
        steps {
            container('docker') {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']],
    userRemoteConfigs: [[url: 'https://github.com/campbill01/home_automation.git']]])
            }
        }
        
    }
    stage('Build') {
      steps {
        container('docker') {
          withCredentials([usernamePassword(credentialsId: 'DockerHub', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
          sh """
             docker login -u $Username -p $Password
             docker build  -t campbill/home_automation:latest .
             docker push campbill/home_automation:latest
          """
          }
        }
      }
    }
  }
}
