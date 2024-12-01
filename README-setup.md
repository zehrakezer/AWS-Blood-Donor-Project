# react-fastapi

### Backend
```bash
    python3 -m venv .venv
    source .venv/bin/activate

    pip3 install -r requirements.txt

    uvicorn main:app --reload
```
### Front-End

```bash
npm install
npm run start
```
----

EC2 Create services:

systemctl status kan.service

Repo download:

project backend create:

mkdir /home/kan-project

git clone https://github.com/mesutspr/aws.mesuty.com.tr.git .

python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

Create services:

nano /etc/systemd/system/kan.service

inside kod:
------------------------------------------------
[Unit]
Description=FastAPI kan Uygulaması
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/home/kan-project
ExecStart=/home/kan-project/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
------------------------------------------------

systemctl start kan.service // start services
systemctl stop kan.service  // stop services
systemctl status kan.service // status services

Check: 

http://ip_adress:8000/api

---

Frontend build:

npm install
npm run build