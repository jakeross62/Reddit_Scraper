from sqlalchemy import create_engine
db = "mysql+pymysql://jw5r4s4hpygud6jvnpz4:pscale_pw_UhWVMFwGSC6tPag2kVQHRRE2Cy7p06qF8BqKIpYDUNA@aws-eu-west-2.connect.psdb.cloud/group17demo?charset=utf8mb4"
engine = create_engine(
    db,
    connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
        }
  }
)