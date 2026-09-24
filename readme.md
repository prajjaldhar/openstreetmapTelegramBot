

```markdown
# 🚀 Business Finder Telegram Bot

A Python-based Telegram bot that helps users find nearby businesses by **category, city, and radius** using OpenStreetMap data.

The bot can search for businesses such as restaurants, cafes, gyms, hospitals, pharmacies, schools, hotels, banks, and more.

It also provides:

- 📍 Business address
- 📏 Distance from the searched city center
- 🗺️ OpenStreetMap location
- 📞 Phone number (when available)
- 🌐 Website (when available)
- 📊 CSV export
- 📗 Excel export

---

## ✨ Features

### 🔎 Business Search

Search businesses using:

```text
/find <category> <city> <radius>
```

Examples:

```text
/find restaurant Bhopal
/find cafe Jaipur
/find gym Indore 10
/find pharmacy Delhi 5
```

If radius is not provided, the default radius is **5 km**.

---

## 🏢 Supported Categories

Currently supported:

- 🍽️ Restaurant
- ☕ Cafe
- 🏥 Hospital
- 💊 Pharmacy
- 🏫 School
- 🎓 College
- 🏦 Bank
- 🏨 Hotel
- 🏋️ Gym
- 🛒 Supermarket
- 🥐 Bakery
- 🦷 Dentist
- 🏥 Clinic
- 👮 Police
- ⛽ Fuel

More categories can easily be added.

---

## 📏 Radius Search

Users can specify a search radius in kilometers.

Example:

```text
/find gym Bhopal 15
```

This searches for gyms and filters the returned businesses based on their distance from the city coordinates.

Maximum supported radius:

```text
50 km
```

---

## 🗺️ Map Integration

Each business includes an OpenStreetMap link.

Example:

```text
🗺️ Open Map
```

Clicking the button opens the business location on OpenStreetMap.

---

## 📞 Contact Information

If available in OpenStreetMap data, the bot can display:

```text
📞 Phone
🌐 Website
```

The bot automatically provides buttons for calling or opening the website when the required information is available.

---

## 📊 Export Data

Search results can be exported automatically.

### CSV

```text
Business Name
Category
Address
Phone
Website
Latitude
Longitude
Distance KM
```

### Excel

The bot generates an `.xlsx` file containing the same business information.

---

# 🏗️ Project Structure

```text
business-finder-bot/
│
├── bot.py
├── requirements.txt
├── Procfile
├── .gitignore
│
└── services/
    ├── __init__.py
    └── openstreetmap.py
```

---

# ⚙️ Technologies Used

- 🐍 Python
- 🤖 Python Telegram Bot
- 🗺️ OpenStreetMap
- 📍 Nominatim API
- 📊 OpenPyXL
- 🌐 Requests
- 🔐 Python Dotenv

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/business-finder-bot.git
```

Move into the project:

```bash
cd business-finder-bot
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Create Telegram Bot

Open Telegram and search for:

```text
@BotFather
```

Create a new bot and obtain your bot token.

Create a `.env` file in the project root:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

⚠️ **Never commit your `.env` file to GitHub.**

---

# ▶️ Run the Bot

Start the bot:

```bash
python bot.py
```

You should see:

```text
🤖 Business Finder Bot running...
```

Now open your Telegram bot and use:

```text
/start
```

Then try:

```text
/find gym Bhopal 15
```

---

# 🔐 Environment Variables

The project currently requires:

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Telegram Bot API token |

Example:

```env
BOT_TOKEN=123456789:XXXXXXXXXXXX
```

---

# ☁️ Deployment

The bot can be deployed on cloud platforms such as:

- Railway
- Render
- VPS
- Other Python-compatible hosting platforms

For deployment, configure:

```text
BOT_TOKEN
```

as an environment variable.

The included `Procfile` contains:

```text
worker: python bot.py
```

---

# ⚠️ Data & API Limitations

This project uses **OpenStreetMap/Nominatim**, not Google Maps.

Therefore:

- Google Maps ratings are not available.
- Google Maps reviews are not available.
- Phone numbers may be missing.
- Websites may be missing.
- Search results depend on OpenStreetMap data.
- The bot does not guarantee that every business in a geographic area will be returned.

The radius filter is applied to the businesses returned by the search service.

---

# 🔮 Future Improvements

Possible future features:

- [ ] More business categories
- [ ] Better POI discovery
- [ ] Pagination
- [ ] Duplicate business detection
- [ ] Business detail pages
- [ ] User search history
- [ ] Database integration
- [ ] Saved businesses
- [ ] Advanced filters
- [ ] Admin dashboard
- [ ] Lead management
- [ ] Authentication
- [ ] Cloud deployment
- [ ] Analytics
- [ ] Interactive Telegram menus

---

# 🎯 Use Cases

This project can be used as a foundation for:

- 🔎 Local business discovery
- 📊 Business research
- 🏢 Lead generation
- 📍 Location-based search
- 🤖 Telegram automation
- 📈 Business intelligence tools

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit:

```bash
git commit -m "Add new feature"
```

5. Push:

```bash
git push origin feature/new-feature
```

6. Open a Pull Request

---

# 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Prajjal Dhar**

Building projects around:

- Python
- MERN Stack
- Data Science
- Generative AI
- Agentic AI
- Automation

---

⭐ If you find this project useful, consider giving the repository a star!
```

> 🤖 A Python Telegram bot for finding local businesses by category, city and radius using OpenStreetMap, with CSV & Excel export.
