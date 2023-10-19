![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
# 📄 Template for creating a telegram bot using the aiogram framework
This bot was created for educational purposes and is a template with examples of using various functionality of the aiogram 3 framework for creating telegram bots.</br>
### This template has:

:white_medium_square: virtual environment,</br>
:white_medium_square: custom filters,</br>
:white_medium_square: environment variables,</br>
:white_medium_square: bot configuration,</br>
:white_medium_square: strict modularity,</br>
:white_medium_square: routers,</br>
:white_medium_square: replyKeyboards,</br>
:white_medium_square: inlineKeyboards,</br>
:white_medium_square: setMyCommands,</br>
:white_medium_square: callback Factory,</br>
:white_medium_square: FSM based on redis.</br>


# 🛠 Development

### 1. To create a virtual environment:

- For windows - ```python -m venv venv```
- For macOS & Linux - `python3 -m venv venv`

### 2. The virtual environment is activated with the command:

- For windows - `venv\Scripts\activate.bat`
- For Power Shell - `venv\Scripts\activate.ps1`
- For macOS & Linux - `source venv/bin/activate`

### 3. To install all dependencies in a virtual environment:

```bash
pip install -r requirements.txt
```

### 4. To add new dependencies:

```bash
pip freeze > requirements.txt
```

### 5. How to leave the virtual environment:

```bash
deactivate
```

### 6. How to launch a bot:

- For windows - `py start.py`
- For macOS & Linux - `python3 start.py`

# 💾 Deploying a bot

### 1. Docker installation
   **❗️ Important**
   
  Before starting installation, check the system requirements:
  - 64-bit architecture
  - kernel no lower than version 3.10 (suitable for Ubuntu version 16.04 and higher)

  Update the existing package list:
  ```bash
  sudo apt update
  ```

  Install a few necessary packages that allow `apt` to use packages over HTTPS:
  ```bash
  sudo apt install apt-transport-https ca-certificates curl software-properties-common
  ```

  Add the GPG key for the official Docker repository to your system:
  ```bash
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  ```

  Add the Docker repository to the APT sources:
  ```bash
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
  ```

  Update the package database and add the Docker packages from the newly added repository:
  ```bash
  sudo apt update
  ```

  Install Docker:
  ```bash
  sudo apt install docker-ce
  ```

  Docker must be installed. Check that it is running:
  ```bash
  sudo systemctl status docker
  ```

### 2. Installation make

  You need to update packages and install make on the server:
  ```bash
  sudo apt-get update && sudo apt-get -y install make
  ```

  Check the installed version:
  ```bash
  make -v
  ```

### 3. Docker container
 Go to the bot repository:
  ```bash
  cd name
  ```
  
  To create a container image you need:
  ```bash
  make build
  ```

  To start a container:
  ```bash
  make run
  ```


