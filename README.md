# Link Hunter By Group-17

  

  

## Contributors

* Iustinian - Lead Developer, Project Manager, Team Leader, Tester, Project Coordinator and Technical Writer

* Ben - Programmer, Assistant Project Manager, Designer

* Jake - Programmer

* Ash - Programmer

* Stuart - Programmer

* Jac - Programmer, Designer

* Konstantinos - Programmer, Designer

* Rudresh - Programmer, Designer

  

# Installing Required Dependencies

**To install Depenencies**

>  `pip install -r requirements.txt`

  
# Running the project through LocalHost
To run the project your terminal/CLI must be opened inside the same folder as the project.
<br/>
 ***Be sure that you've installed the required dependencies before trying this stage!***

| Operating System    | Commands                        |
|---------------------|---------------------------------|
| **Windows 10 & 11** | python app.py **or** python3 app.py |
| **Linux**           | python3 app.py                  |
| **MacOS**           | python3 app.py                  |

# Setting Up Database

While the Database is already technically already setup. The client may want to update the Database to their own personal controlled Database. This can be done by changing the following below:

    db  = "mysql+pymysql://USERNAME:PASSWORD@HOST/DATABASE?charset=utf8mb4"
    engine  =  create_engine(
    db, connect_args={
    "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
    }}
*Sometimes the client when changing the database may run into some issues with the **SSL permits**. Due to some Database hosts requiring **different** verifications for SSL, therefore I'm unable to provide example/help for the issue itself. **However the host may be able to provide guidance on how to configure SSL settings properly or provide alternative solutions for establishing a secure connection to the database.***

## Prerequisits required for the Database
 #### Creating the Table

    CREATE TABLE `main` (
      `id` int NOT NULL AUTO_INCREMENT,
      `link` varchar(500) DEFAULT NULL,
      `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      `jdata` json DEFAULT NULL,
      PRIMARY KEY (`id`)
That is all that is required from the client if they wish to implement their own Database, since almost everything is controlled through the database_query.py and a call is used inside app.py for the downloading of the raw_data.json.
  

In the current Repository we have already implemented our own Database, along side the required Keys to access the Database, as shown below:

    HOST=aws-eu-west-2.connect.psdb.cloud
    USERNAME=jw5r4s4hpygud6jvnpz4
    PASSWORD=pscale_pw_UhWVMFwGSC6tPag2kVQHRRE2Cy7p06qF8BqKIpYDUNA
    DATABASE=group17demo

# Hosting the Website
For the demonstration meeting, we have setup a simple hosting for the group project hosted on the web. 
And it can be accessed by following the link below.
> https://group17demo.onrender.com

Keeping in mind that since we are using the **Free** version, the same goes for the database. The server may sometimes take a moment for it to load since it may require a re-boot of the server hosting it. 
### Demo of setting up a host for the website on render.com

![Stage 1](IFRM/1.png?raw=true)
![Stage 2](IFRM/2.png?raw=true)
![Stage 3](IFRM/3.png?raw=true)
![Stage 4](IFRM/4.png?raw=true)
![Stage 5](IFRM/5.png?raw=true)
![Stage 6](IFRM/6.png?raw=true)
![Stage 7](IFRM/7.png?raw=true)
![Stage 8](IFRM/8.png?raw=true)
![Stage 9](IFRM/9.png?raw=true)
![Stage 10](IFRM/10.png?raw=true)

# To view the current live website you may click on the link below
https://group17demo.onrender.com/

I must mention that it will take time to load at first if there has not been any recent activity in the past hour. If that is the case just give it a few minutes and it should be all up and running. Furthermore if there are any internal server issues, this is likely due to the server being migrated and this takes a few hours to finish.
