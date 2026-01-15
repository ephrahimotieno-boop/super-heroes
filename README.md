#  Late Show API

A Flask REST API for managing a late show database featuring episodes, guests, and appearances. This project includes a complete backend API and a React-based frontend for a full-stack experience.

##  Features

- **Full CRUD API**: Manage episodes, guests, and appearances.
- **Robust Validations**: Enforced 1-5 rating scale for appearances.
- **Smart Seeding**: Works with or without CSV files.
- **Interactive UI**: View episode details, guest info, and create new appearances.

##  Quick Start

### 1. Setup Environment
```bash
pip install -r requirements.txt
```

### 2. Initialize and Seed
```bash
# This creates the database and populates it with initial data
python seed.py
```

### 3. Run the App
```bash
python app.py
```
The server will start at `http://localhost:5000`.

---

## 🛠 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/episodes` | List all episodes |
| **GET** | `/episodes/:id` | Episode details + appearances |
| **GET** | `/guests` | List all guests |
| **POST** | `/appearances` | Create a new appearance |
| **DELETE** | `/episodes/:id` | Remove episode (cascades appearances) |

---

##  Project Structure

```text
├── app.py           # Main entry point
├── models.py        # Database schema & validations
├── routes.py        # API endpoint logic
├── seed.py          # Database population script
└── frontend/        # React application
```

##  Testing

You can use the provided **Postman collection** to test all endpoints. Ensure the server is running on port 5000 before testing.

---
