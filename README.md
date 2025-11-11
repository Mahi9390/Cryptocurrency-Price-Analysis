🪙 Cryptocurrency Price Analysis & Prediction System

A Django & Machine Learning-based Web Application

🧩 Project Overview

This project is a Cryptocurrency Price Analysis and Prediction System built using Python, Django, and Machine Learning.
The main goal of the project is to allow admins, agents, and users to interact in a crypto-based environment — where admins manage crypto data, agents perform price predictions using trained ML models, and users can view and trade cryptocurrencies based on predicted results.

It integrates machine learning for price forecasting, data visualization, and a blockchain ledger to maintain secure crypto transactions.

🧱 Modules in the Project
🔹 1. Admin Module

The Admin has complete control over the system.
The admin can:

Log in to the admin dashboard.

Upload cryptocurrency datasets (CSV files).

Manage agents and users (view, block, or delete them).

Update or manage the current cryptocurrency rates.

View the blockchain ledger that records all transactions securely.

Monitor the system analytics and prediction reports.

🔹 2. Agent Module

The Agent acts as an intermediate user who predicts cryptocurrency prices using the machine learning model.
Agents can:

Register or log in to their account.

Access the Agent Dashboard.

Upload or use the available dataset for prediction.

Perform coin price predictions (like Bitcoin, Ethereum, etc.) using the trained ML model.

Buy cryptocurrency based on predicted results.

View transaction history and prediction accuracy reports.

Each transaction made by the agent is securely recorded in the blockchain ledger for transparency.

🔹 3. User Module

The User interacts with the platform to view prices and trade cryptocurrencies.
Users can:

Register or log in to their account.

Browse through the available cryptocurrencies and their predicted prices.

Make buying or selling decisions based on the agent’s predicted results.

View their wallet balance and trading history.

Track their investment and growth through visual reports.

⚙️ Project Workflow (Step-by-Step)

Here’s how the project works from start to finish 👇

Admin logs in and uploads the dataset (contains historical cryptocurrency data such as price, date, volume, etc.).

The machine learning model (like XGBoost, RandomForest, or Decision Tree) processes this data.

The system trains the model and stores it for future predictions.

Admin also updates the current cryptocurrency rates in the system.

Agents log in and select the coin for which they want to make a prediction.

The trained model predicts the future price of the selected cryptocurrency.

Based on the prediction result, the agent can buy or sell cryptocurrency.

Every transaction (buy/sell) is stored in the blockchain ledger to ensure transparency and immutability.

Users log in and view predicted prices and make their own buy/sell decisions accordingly.

The system generates visual reports and charts showing actual vs predicted price comparisons, and transaction summaries.

🤖 Machine Learning Logic

The dataset (uploaded by admin) is preprocessed to clean and structure the data.

Important features like Open, Close, High, Low, Volume, and Market Cap are used for training.

A Regression Model (XGBoost or RandomForest) predicts the next-day cryptocurrency price.

Accuracy, F1-score, and performance metrics are displayed on the console or prediction screen.

Example Output:

Predicted Price for Bitcoin: $52,340
Actual Price: $51,800
Model Accuracy: 96.2%

📊 Data Visualization

The system provides clear visual insights:

Line charts showing Actual vs Predicted prices.

Bar charts displaying number of transactions per cryptocurrency.

Pie charts for portfolio distribution.

These visualizations help both agents and users make better decisions.

🔐 Blockchain Ledger Integration

Every transaction (buy/sell) is stored in a blockchain-like ledger model.
Each transaction has:

A unique transaction ID

Sender and receiver details

Transaction amount

Timestamp

Previous hash and new hash values

This ensures transparency and prevents data tampering.

🧰 Tech Stack Used
Category	Technologies
Frontend	HTML, CSS, JavaScript, Bootstrap
Backend	Python (Django Framework)
Database	SQLite / MySQL
Machine Learning	Scikit-learn, XGBoost, Pandas, NumPy
Visualization	Matplotlib, Seaborn, Plotly
Version Control	Git & GitHub
🚀 How to Run the Project

Clone the repository

git clone https://github.com/YourUsername/Cryptocurrency-Price-Analysis.git


Navigate to the project directory

cd Cryptocurrency-Price-Analysis


Install dependencies

pip install -r requirements.txt


Run migrations

python manage.py makemigrations
python manage.py migrate


Run the server

python manage.py runserver


Access in browser

📽️ Output Screens (as seen in video)
Screen	Description
Home Page	Overview of the system
Admin Dashboard	Dataset upload, crypto rate update
Agent Dashboard	Coin prediction, buy/sell options
User Dashboard	Price view, trade history
Prediction Result	Displays predicted price and accuracy
Blockchain Ledger	List of all transactions with hash values
🧠 Future Enhancements

Integrate real-time crypto price APIs.

Deploy on cloud (AWS / Render).

Implement deep learning models (LSTM).

Enable real blockchain smart contract integration.

✨ Conclusion

This system provides a full-fledged environment to analyze, predict, and trade cryptocurrencies with machine learning and blockchain principles.
It demonstrates how predictive analytics and data-driven decisions can be used in financial and crypto domains efficiently.
