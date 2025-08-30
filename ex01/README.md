# pgAdmin 4 Installation & Configuration on Ubuntu (with Apache)

This guide explains how to install pgAdmin 4, configure it, and run it using Apache on Ubuntu.

## 1. Update system
```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Install required packages
```bash
sudo apt install curl ca-certificates gnupg apache2 -y
```

## 3. Add pgAdmin repository
```bash
curl https://www.pgadmin.org/static/packages_pgladmin_org.pub | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/pgadmin.gpg
echo "deb [signed-by=/etc/apt/trusted.gpg.d/pgadmin.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list
sudo apt update
```

## 4. Install pgAdmin
```bash
sudo apt install pgadmin4-web -y
```

## 5. Initial setup

Run the setup script:
```bash
sudo /usr/pgadmin4/bin/setup-web.sh
```

- Enter email and password for the initial pgAdmin admin account.
- When asked about Apache configuration, type `y` (yes).

## 6. Configure Apache port (optional, if default 80 is in use)

**Why change the port?**  
Port 80 is the default HTTP port and might already be in use by other applications like Nginx, another Apache instance, or other web services. Using a different port (like 8082) prevents conflicts and allows multiple web services to run simultaneously on the same system.

**Important:** Before using port 8082, verify it's not already in use by running:
```bash
sudo netstat -tlnp | grep :8082
```
If the command returns nothing, the port is available. If it shows any output, choose a different port number.

Edit Apache ports:
```bash
sudo nano /etc/apache2/ports.conf
```

Change the line:
```
Listen 80
```

to:
```
Listen 8082
```

Edit pgAdmin config:
```bash
sudo nano /etc/apache2/conf-available/pgadmin4.conf
```

Wrap the config with `<VirtualHost>`:
```apache
<VirtualHost *:8082>
    WSGIDaemonProcess pgadmin processes=1 threads=25 python-home=/usr/pgadmin4/venv
    WSGIScriptAlias /pgadmin4 /usr/pgadmin4/web/pgAdmin4.wsgi

    <Directory /usr/pgadmin4/web/>
        WSGIProcessGroup pgadmin
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

## 7. Enable pgAdmin config & restart Apache
```bash
sudo a2enconf pgadmin4
sudo systemctl restart apache2
```

## 8. Access pgAdmin

Open your browser and go to:
```
http://127.0.0.1:8082/pgadmin4
```

Login with the email and password created during setup.

 pgAdmin is now installed and running with Apache on Ubuntu.