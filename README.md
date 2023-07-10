
<p align="center">
  <img src="https://static.xx.fbcdn.net/rsrc.php/v3/y2/r/ZI3qMUkj5Tz.png" alt="Threads Logo" width="200" height="200">
</p>

<h1 align="center">Threads.net Media API</h1>

<p align="center">
  <strong>A Flask-based API for retrieving media information from Threads.net posts</strong>
</p>

<p align="center">
  <a href="https://github.com/shubhtoy/Threads.net-Media-API/stargazers"><img src="https://img.shields.io/github/stars/shubhtoy/Threads.net-Media-API.svg?style=social" alt="Star"></a>
  <a href="https://github.com/shubhtoy/Threads.net-Media-API/fork"><img src="https://img.shields.io/github/forks/shubhtoy/Threads.net-Media-API.svg?style=social" alt="Fork"></a>
</p>

---

This repository contains a Flask-based API that retrieves media information from Threads.net posts. It extracts media items such as photos and videos from a given Threads.net post URL and returns the data in a JSON format. The API also includes an HTML form to make it easy for users to submit Threads.net post URLs and retrieve the associated media information.

The API uses the Requests library for making HTTP requests, Flask for building the API endpoints, and integrates with a URL shortening service (Bitly or TinyURL) to generate shortened URLs for the Threads.net posts.

## Instructions

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Replace the placeholder Bitly/TinyURL API credentials in the code with your own credentials.
3. Run the Flask application by executing `python app.py`.
4. Access the API endpoints:
   - `GET /` - Renders the HTML form for entering Threads.net post URLs.
   - `POST /media` - Accepts a URL from the form submission, retrieves the media information, and returns it in JSON format.
5. Customize the code and HTML template as per your requirements.

Feel free to modify the code and add additional functionality as needed.

---

<p align="center">
  <strong>Like this project? Don't forget to star ⭐️ and fork 🍴 the repository to show your support!</strong>
</p>
