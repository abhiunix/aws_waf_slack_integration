pipeline {
    agent any 
    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
    } 
    stages{
        stage('Checking python version'){
            steps{
                sh 'python3 -V'
            }
        }
        stage('Cloning the repo'){
            steps{
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/abhiunix/aws_waf_slack_integration']])
                sh 'echo clone completed'        
            }
        } 
        stage('converting the repo to prod') {
            steps{
                script{
                    withCredentials([
                        string(credentialsId: 'YourUserName_id', variable: 'YourUserName'),
                        string(credentialsId: 'YourAWSprofile_id', variable: 'YourAWSprofile'),
                        string(credentialsId: 'YourTeamDomain_id', variable: 'YourTeamDomain'),
                        string(credentialsId: 'YourChannelName_id', variable: 'YourChannelName')
                    ]) {
                        sh """
                        SEARCH_DIR="\${WORKSPACE}"
                        find "\$SEARCH_DIR" -type f \\( -name "*.py" -o -name "*.txt" \\) | while read -r FILE; do
                            sed -i '' "s/YourUserName/\${YourUserName}/g" "\$FILE"
                            sed -i '' "s/YourAWSprofile/\${YourAWSprofile}/g" "\$FILE"
                            sed -i '' "s/YourTeamDomain/\${YourTeamDomain}/g" "\$FILE"
                            sed -i '' "s/YourChannelName/\${YourChannelName}/g" "\$FILE"
                            echo "The file \$FILE has been updated."
                        done
                        echo "Conversion to prod completed."
                        """
                    }
                }
            }
        }
        stage('building the docker image'){
            steps{
                script{
                    sh '/opt/homebrew/bin/docker build -t abhiunix/aws_waf_slack_integration:v1 .'
                    sh 'echo "docker build successful"'
                }
            }
        }
        stage('Push to docker hub'){
            steps{
                script{
                    withCredentials([string(credentialsId: 'dockerhub_pwd', variable: 'docker_pwd')]) {
                    sh '/opt/homebrew/bin/docker login -u abhiunix -p ${docker_pwd}'
                    }
                    sh '/opt/homebrew/bin/docker push abhiunix/aws_waf_slack_integration:v1'
                }
            }
        }
        stage('Run the container') {
            steps {
                script {
                    sh """ 
                        IMAGE_ID=\$(/opt/homebrew/bin/docker images | grep 'abhiunix/aws_waf_slack_integration' | awk -F' ' '{print \$3}' | head -n 1)
                        if [ ! -z "\$IMAGE_ID" ]; then
                            /opt/homebrew/bin/docker run -dt -p 8002:8002 -v /Users/abhijeetsingh/Downloads/scripts/.aws:/root/.aws:ro -e AWS_DEFAULT_REGION=ap-south-1 -e AWS_PROFILE=curefit-security-devs \$IMAGE_ID
                        else
                            echo "Image not found!"
                        fi
                        """
                }
            }
        }

    }
}
