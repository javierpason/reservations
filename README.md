# AWS SAM Application: LoanPro Reservations

## Overview

This project is an AWS SAM (Serverless Application Model) application designed to manage reservations. It includes Lambda functions for creating, updating, listing, and deleting reservations, integrated with DynamoDB, API Gateway, and various other AWS services such as EventBridge, SQS and SNS.

## Prerequisites

Before you begin, make sure you have the following installed:

- **AWS CLI**: [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- **AWS SAM CLI**: [Install SAM CLI](https://docs.aws.amazon.com/serverless/latest/dg/install-sam-cli.html)
- **Python 3.12**: [Install Python 3.12](https://www.python.org/downloads/release/python-3120/)

## Setup and Deployment

### 1. **Configure AWS CLI**

Ensure you has been configured the AWS CLI with de rigths credentials and region:

```bash
aws configure
```
### 2. **Clone the Repository**

If you haven’t already, clone the repository containing your SAM application.

```bash
git clone https://github.com/javierpason/reservations.git
cd <repository-directory>
```
You will work on the branch: feature/refactory.

### 3. **Build the SAM Application**

After SAM installation, build the SAM application using the SAM CLI. This step packages your Lambda function code and prepares it for deployment.
Go to the LoanPro folder and run:

```bash
sam build
```
### 4. **Deploy the SAM Application**
If you don't hace any error with the previous command run the next command, it will deploy the application to your AWS account. You will be prompted to enter parameters such as the stack name and AWS region.

```bash
sam deploy --guided (use the --guide parameter only the first time)
```

### 5. **Validate Infrastructure Deploy**
When sam deploy finished you will see the URL API, something like this:
Outputs
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key                 ApiUrl
Description         The URL of the API Gateway endpoint
Value               https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/

https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production

### 6. **Create SNS Subscription**
Go to AWS Console and the Simple Notification Service, go to the loanpro-reservations topic and create a Subscription in order to recive emails.

### 7. **Testing with Postman**
#### a.- Create Reservation
Description: Creates a new reservation.
Endpoint: POST /reservations
URL Example: https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/reservations

Request Body:
json code

```bash
{
  "user": "Javier Marin",
  "details": "Reservation details here (1 person.)"
}
```
#### b.- List Reservations
Description: Retrieves a list of all reservations.
Endpoint: GET /reservations
URL Example: https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/reservations

Result expected:
```bash
[
    {
        "last_updated": "2024-08-26T04:45:22.839482",
        "deleted": 0,
        "reservation_id": "33e73dec-dfec-4088-83ee-8bcafda223ef",
        "reservation_status": "Created",
        "timestamp": 1724647522,
        "created": "2024-08-26T04:45:22.839482",
        "user": "Javier Marin",
        "details": "5 People"
    }
]
```

#### c.- Update Reservation
Description: Updates an existing reservation.
Endpoint: PATCH /reservations
URL Example: https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/reservations

```bash
{
   "reservation_id": "33e73dec-dfec-4088-83ee-8bcafda223ef",
    "timestamp": 1724647522,
    "updates": {   
      "details": "2 Persons"
    }
}
```

#### d.- Get Reservation
Description: Retrieves a specific reservation based on reservation_id and timestamp.
Endpoint: GET /reservations/{reservation_id}/{timestamp}
URL Example: https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/reservations/33e73dec-dfec-4088-83ee-8bcafda223ef/1724647522

Result expected:
```bash
{
    "last_updated": "2024-08-26T04:45:22.839482",
    "deleted": 0,
    "reservation_id": "33e73dec-dfec-4088-83ee-8bcafda223ef",
    "reservation_status": "Created",
    "timestamp": 1724647522,
    "created": "2024-08-26T04:45:22.839482",
    "user": "Javier Marin",
    "details": "2 Persons"
}
```

#### e.- Cancel Reservation
Description: Cancel a reservation as a logic way.
Endpoint: DELETE /reservations
URL Example: https://ph3uochjo9.execute-api.us-east-1.amazonaws.com/production/reservations/33e73dec-dfec-4088-83ee-8bcafda223ef/1724647522

Result expected:
```bash
{
   "reservation_id": "33e73dec-dfec-4088-83ee-8bcafda223ef",
    "timestamp": 1724647522,
    "updates": {   
      "details": "5 People"
    }
}
```

### 8. **Monitoring and Logs**
You can use CloudWatch to see Lambda logs.

### 8. **Cleanup**
To delete the stack and clean up all resources, use the following command:
```bash
sam delete
```
