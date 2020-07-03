# Setting up a website in s3 to display content

## using this guide:
```https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photos-view.html```


## steps

 1. create bucket and configure for public access
 2. create congnito identity pool
 3. take the created role for unauthenticated users and give it permission to list content on the bucket
 4. configure cors
 5. Enabling website hosting (https://docs.aws.amazon.com/AmazonS3/latest/dev/EnableWebsiteHosting.html)
 6. Setting permissions for website access (https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteAccessPermissionsReqd.html) 

Cognito_SolAuth_Role
Cognito_SolUnauth_Role

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "mobileanalytics:PutEvents",
        "cognito-sync:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}


Sample code:

Get AWS Credentials
// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'eu-west-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'eu-west-1:12054b51-3896-4011-b266-7eac2a5a10a5',
});

Policy:
ListBucketStellavagen

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::stellavagen-website"
            ]
        }
    ]
}


cors: 

<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>HEAD</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>


bucket policy:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::example.com/*"
            ]
        }
    ]
}
