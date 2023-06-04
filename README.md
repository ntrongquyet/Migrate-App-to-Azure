# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource            | Service Tier                                                                                                                       | Monthly Cost |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| *Azure Postgres Database* | Single Service                                                                                                                     | $25.32       |
| *Azure Service Bus*       | Single Server Deployment, Basic Tier, 1 Gen 5 (1 vCore) x 1 Month, 5 GiB Storage, 0 GiB Additional Backup storage - LRS redundancy | $0.05        |
| *Azure Functions*         | Consumption tier, Pay as you go, 128 MB memory, 100 milliseconds execution time, 0 executions/mo                                   | $0.0         |
| *App Service*             | Free Tier; 1 F1 (0 Core(s), 1 GB RAM, 1 GB Storage) x 730 Hours; Linux OS                                                          | $0.0         |
| **Est monthly cost**      |                                                                                                                                    | $25.37       |
|                           |                                                                                                                                    |              |
## Architecture Explanation
***I have chosen both Azure App Service and Azure Functions because they offer the following advantages:***

### ***Azure App Service:***

- Easy and fast deployment of web apps: With Azure App Service, you don't have to worry about the underlying operating system or hardware. You can quickly deploy your web app without dealing with infrastructure complexities.

- Cost savings: Azure App Service provides a free tier (F1) with 1GB RAM and 1GB storage, allowing you to deploy your app at no cost.

### ***Azure Functions:***

- Seamless integration with Azure services: Azure Functions can easily be incorporated with other Azure services like Azure Service Bus or Azure Event Hub. This enables you to build event-driven architectures and process messages or events efficiently.

- Cost savings: With Azure Functions, you only pay for the execution time of your functions.

=> By combining Azure Web App and Azure Functions, you can create a scalable, cost-effective, and performant web application architecture with microservices. Utilizing Azure Service Bus for decoupling application components can further enhance the reliability and maintainability of your solution. For example, you can use Service Bus to queue messages, trigger functions for sending emails to attendees, and update status asynchronously.
