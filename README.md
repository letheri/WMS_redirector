# WMS Redirector
This app is built for redirecting a WMS link using Flask.

## Installation
- Install Python 3.11
- It is recommended to create a new environment for the app. Create the environment using on CMD with,
  - python -m venv C:\ { _APP_FOLDER_ } \env
- Active the environment using CMD with following,
  + C:\ { _APP_FOLDER_ } \env\Scripts\activate.bat
- After activating the environment, install the necessary libraries for the app.
  + Flask
  + waitress
  + requests

## Deployment
Deployement steps only include how to deploy for IIS Windows servers.
Normally, any WMS link can be redirected on IIS directly, but WMS responses contain links which directs to certain features.
Any web application that relies on these links get broken if the links were to be just directed on IIS.

As a solution, this flask app is used to update the response XML content to match the redirected links.

- The app needs to be installed as a windows service using <a href="https://nssm.cc/download">NSSM tool</a>.
- Reverse proxy functionaly needs to be enabled on IIS. <a href="https://www.jenkins.io/doc/book/system-administration/reverse-proxy-configuration-iis/">Link</a>
- Use the localhost link to redirect on IIS.

