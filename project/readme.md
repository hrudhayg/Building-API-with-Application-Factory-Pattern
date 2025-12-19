

# Mechanic Service API (Flask + Application Factory)

This project is a **REST API built with Flask**, using the **Application Factory Pattern** and **Blueprints** for modular structure.  
It manages **Customers, Mechanics, and Service Tickets**, demonstrating full CRUD operations and relationships.

---

## 📂 Project Structure


project/
├── application/
│ ├── init.py # Application Factory
│ ├── extensions.py # SQLAlchemy, Marshmallow init
│ ├── models.py # Database models
│ ├── /blueprints
│ │ ├── customers/ # Customer routes + schema
│ │ ├── mechanics/ # Mechanic routes + schema
│ │ └── service_tickets/ # Ticket routes + schema
├── app.py # Entry point
├── config.py # Config settings (DB, etc.)
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🚀 Features
- **Customers**
  - Create, Read, Update, Delete customers
- **Mechanics**
  - Create, Read, Update, Delete mechanics
- **Service Tickets**
  - Create service tickets
  - Assign/remove mechanics to tickets (Many-to-Many)
  - Update or delete tickets
  - Fetch all or specific tickets

---

## 🛠️ Setup & Installation

1. Clone the repo:
   ```bash
   git clone git@github.com:hrudhayg/Building-API-with-Application-Factory-Pattern.git
   cd Building-API-with-Application-Factory-Pattern


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Configure your MySQL Database inside config.py:

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://username:password@localhost/mechanic_db"


Initialize database tables:

flask shell
>>> from application.extensions import db
>>> from application.models import *
>>> db.create_all()


Run the app:

python app.py


The API will be available at:
👉 http://127.0.0.1:5000/

📬 Example Postman Requests
Create Customer

POST http://127.0.0.1:5000/customers/

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}

Create Mechanic

POST http://127.0.0.1:5000/mechanics/

{
  "name": "Jane Smith",
  "email": "jane@workshop.com",
  "phone": "9876543210"
}

Create Service Ticket

POST http://127.0.0.1:5000/service_tickets/

{
  "VIN": "1HGCM82633A004352",
  "service_date": "2025-09-05",
  "service_desc": "Oil change + brakes",
  "customer_id": 1
}

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License.


---

Would you also like me to add a **`.gitignore`** block (for venv, pycache, etc.) in the same single-copy style so you never push unwanted files?
