$ aws cloudformation package --s3-bucket 531calc --template-file template.yaml --output-template-file gen/cloudformationtemplate.yaml

$ aws cloudformation deploy --template-file cloudformationtemplate.yaml --stack-name NotifSamApp --region eu-west-2 --parameter-overrides Email=kaizad00@gmail.com --capabilities CAPABILITY_IAM

# Or...

$ sam package --s3-bucket 531calc --template-file template.yaml --output-template-file gen/cloudformationtemplate.yaml

$ sam deploy --template-file gen/cloudformationtemplate.yaml --stack-name SamApp --region eu-west-2 --parameter-overrides Email=kaizad00@gmail.com --capabilities CAPABILITY_IAM
