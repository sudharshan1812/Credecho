# CredEcho — AI-Powered MSME Financial Health Card

![Project](https://img.shields.io/badge/Project-CredEcho-6C63FF)
![Frontend](https://img.shields.io/badge/Frontend-Next.js-black)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Machine Learning](https://img.shields.io/badge/ML-XGBoost-orange)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**CredEcho** is an AI-powered financial assessment platform designed to evaluate the financial health and creditworthiness of Micro, Small, and Medium Enterprises (MSMEs), particularly New-to-Credit (NTC) and New-to-Bank (NTB) businesses.

The platform analyzes digital financial indicators such as GST filing consistency, UPI transactions, cash flow, revenue, expenses, repayment history, and business stability to generate a multidimensional **Financial Health Score from 0 to 100**.

CredEcho combines machine learning, explainable financial indicators, and an interactive dashboard to help demonstrate how alternative financial data can support more transparent and accessible credit assessment.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Financial Health Assessment](#financial-health-assessment)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running with Docker](#running-with-docker)
- [API Documentation](#api-documentation)
- [Example Use Case](#example-use-case)
- [Security and Data Privacy](#security-and-data-privacy)
- [Limitations and Future Enhancements](#limitations-and-future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement

Many MSMEs face difficulties accessing formal credit because they lack conventional financial documentation, extensive credit histories, or established relationships with banks.

Traditional lending assessments may depend heavily on:

- Income tax returns and balance sheets.
- Credit bureau history.
- Conventional banking records.
- Established borrowing and repayment histories.

These requirements can make it difficult to evaluate promising businesses with limited formal credit records.

At the same time, businesses may generate valuable digital financial signals through GST filings, digital payments, invoices, employee records, bank transactions, and utility payments.

**The challenge:** How can these alternative financial indicators be organized into an understandable, data-driven financial assessment?

## Our Solution

CredEcho uses a machine-learning-based approach to convert financial and operational indicators into a structured MSME Financial Health Card.

The platform is designed to:

1. Process business financial indicators.
2. Generate a financial health score.
3. Classify businesses into health categories.
4. Highlight positive and negative contributing factors.
5. Present an indicative lending recommendation.
6. Simulate changes in financial indicators using a what-if analysis.
7. Display the assessment through an interactive dashboard.

The goal is to demonstrate how alternative data and explainable machine learning can support more informed credit assessments.

## Key Features

### 1. AI-Based Financial Health Scoring

Generates a score between 0 and 100 based on business financial and operational indicators.

### 2. MSME Risk Classification

Groups businesses into financial health categories such as Healthy, Moderate, and Risky.

### 3. Financial Health Card

Presents the assessment in a structured format, including the score, risk indicators, strengths, weaknesses, and recommendation.

### 4. Explainable Predictions

Displays important contributing factors to help users understand which financial indicators may influence the assessment.

### 5. Interactive Analytics Dashboard

Provides a visual overview of applicants, financial scores, model analytics, and assessment results.

### 6. What-If Scenario Simulation

Allows users to change selected financial indicators and compare the resulting assessment with the original scenario.

### 7. REST API

Uses a FastAPI backend to expose endpoints for authentication, predictions, health cards, analytics, and scenario simulations.

### 8. Synthetic Dataset Generation

Includes scripts for generating synthetic MSME records and training the machine learning model.

### 9. Containerized Deployment

Includes Dockerfiles and a Docker Compose configuration for running the frontend and backend alongside PostgreSQL and Redis services.

## How It Works

The platform follows a structured financial assessment pipeline.

1. **Business data input:** Financial and operational indicators are supplied for an MSME.
2. **Feature processing:** Relevant numerical and categorical indicators are prepared for the model.
3. **Machine learning inference:** The trained model processes the input features.
4. **Financial assessment:** The application produces a score, classification, and associated indicators.
5. **Explainability:** Contributing factors are presented in a human-readable format.
6. **Dashboard visualization:** The assessment is displayed as a Financial Health Card.
7. **Scenario analysis:** Users can explore how changes to selected indicators affect the assessment.

## System Architecture

```text
                 USER / BANK OFFICER
                          |
                          v
              +-----------------------+
              |    Next.js Frontend   |
              |   TypeScript / React  |
              |       Tailwind CSS    |
              +-----------------------+
                          |
                     REST API
                          |
                          v
              +-----------------------+
              |     FastAPI Backend  |
              | Authentication       |
              | Request Validation   |
              | Prediction Endpoints |
              +-----------------------+
                          |
                          v
              +-----------------------+
              |   ML Inference Layer  |
              |    XGBoost Model      |
              |   Feature Scaling     |
              | Financial Assessment  |
              +-----------------------+
                          |
             +------------+------------+
             |                         |
             v                         v
    +------------------+      +------------------+
    |   PostgreSQL     |      |      Redis       |
    | Persistent Data  |      | Cache Service    |
    +------------------+      +------------------+
                          |
                          v
              +-----------------------+
              | Financial Health Card |
              | Scores and Factors    |
              | Recommendations       |
              +-----------------------+
```

The repository also contains integration-ready project concepts for ULI, OCEN, Account Aggregator, GST, UPI, and EPFO data sources. These should be treated as planned or simulated integrations unless real provider connections have been implemented and configured.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | Next.js 14, React 18, TypeScript |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Charts | Recharts |
| Icons | Lucide React |
| Backend | Python, FastAPI, Pydantic |
| Machine Learning | XGBoost, scikit-learn |
| Data Processing | Pandas, NumPy |
| Explainability | SHAP and feature-contribution analysis |
| Model Serialization | Joblib |
| Database | PostgreSQL |
| Caching | Redis |
| Containerization | Docker, Docker Compose |
| API Documentation | FastAPI / OpenAPI |

## Financial Health Assessment

CredEcho considers multiple dimensions of business financial health.

| Dimension | Purpose |
|---|---|
| Financial Stability | Evaluate indicators of financial strength |
| Cash Flow Health | Examine the consistency of incoming and outgoing funds |
| Business Growth | Analyze revenue and growth patterns |
| Digital Activity | Assess the availability and consistency of digital signals |
| Compliance | Consider GST, tax, and related compliance indicators |
| Repayment Capability | Examine indicators related to repayment capacity |
| Fraud Risk | Identify configured fraud-related risk indicators |
| Revenue Consistency | Evaluate the stability of business revenue |
| Liquidity | Examine available funds and cash flow |
| Operational Stability | Consider business age, workforce, and operating patterns |

These dimensions are intended to support an interpretable assessment. They should not be treated as independently validated financial measures without further testing.

## Machine Learning Pipeline

The repository includes scripts for generating synthetic data and training the model.

### Training workflow

```text
Synthetic Data Generation
          |
          v
Data Preparation
          |
          v
Feature Engineering
          |
          v
Train / Test Evaluation
          |
          v
Feature Scaling
          |
          v
XGBoost Model Training
          |
          v
Model Evaluation
          |
          v
Save Model Artifacts
          |
          v
Backend Inference
```

### Important files

- `ml/generate_data.py` — generates synthetic MSME data.
- `ml/train_model.py` — trains the machine learning model.
- `ml/requirements.txt` — lists the ML dependencies.
- `models/model.joblib` — serialized model artifact included in the project archive.
- `models/scaler.joblib` — serialized feature scaler.
- `models/meta.json` — model metadata.

### Model evaluation

Model performance should be measured using appropriate metrics, including:

- Accuracy.
- Precision and recall.
- F1-score.
- ROC-AUC where applicable.
- Confusion matrix.
- Inference latency.

Because the included datasets are synthetic, high evaluation scores do not establish real-world lending accuracy. Actual performance must be validated using representative, authorized, and appropriately governed real-world data before production use.

## Project Structure

```text
credecho/
├── .github/
│   └── workflows/
│       └── ci.yml
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/
│   │   └── api.ts
│   ├── .env.local.example
│   ├── Dockerfile
│   ├── package.json
│   └── tailwind.config.ts
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   ├── schema.sql
│   └── Dockerfile
├── ml/
│   ├── generate_data.py
│   ├── train_model.py
│   └── requirements.txt
├── datasets/
│   ├── training_data.csv
│   ├── testing_data.csv
│   └── validation_data.csv
├── models/
│   ├── model.joblib
│   ├── scaler.joblib
│   └── meta.json
├── docs/
│   ├── API.md
│   ├── DATA_DICTIONARY.md
│   └── DEMO_SCRIPT.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install the following software before running the project:

- Node.js and npm.
- Python 3.10 or a compatible version supported by the dependencies.
- Git.
- Docker Desktop if using containerized deployment.

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/credecho.git
cd credecho
```

### 2. Set Up the Machine Learning Environment

From the project root:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Install the ML dependencies:

```bash
pip install -r ml/requirements.txt
```

Generate a synthetic dataset and train the model:

```bash
python ml/generate_data.py --n 50000
python ml/train_model.py
```

The scripts should generate the datasets and model artifacts required by the application. If you use the model artifacts already included in the repository, verify that they match the current model code and feature schema before retraining or replacing them.

### 3. Run the Backend

Open a terminal at the project root and activate the Python virtual environment.

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Start the API server:

```bash
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

The backend should be available at:

- API base URL: `http://localhost:8000`
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

### 4. Configure the Frontend

Open another terminal at the project root.

Move into the frontend directory:

```bash
cd frontend
```

Create the local environment file.

On Windows Command Prompt:

```bat
copy .env.local.example .env.local
```

On PowerShell:

```powershell
Copy-Item .env.local.example .env.local
```

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

`http://localhost:3000`

The frontend uses the API URL configured in `.env.local`. Confirm that `NEXT_PUBLIC_API_URL` points to the backend address:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If the API is unavailable, the frontend may use its configured offline fallback for demonstration purposes.

## Running with Docker

Docker Compose is provided to run the project's services together.

From the project root, execute:

```bash
docker compose up --build
```

Once the containers are ready, open:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

To stop the services:

```bash
docker compose down
```

To stop the services and remove the database volume as well:

```bash
docker compose down -v
```

**Warning:** The last command permanently removes the PostgreSQL data stored in the Compose volume.

For production deployment, replace all sample credentials and development secrets, restrict database exposure, configure appropriate network access, and use HTTPS.

## API Documentation

The backend provides REST endpoints for financial assessment and related operations.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/login` | Authenticate a demo user and obtain a token |
| POST | `/predict` | Generate a financial assessment |
| POST | `/healthcard` | Generate a detailed Financial Health Card |
| POST | `/whatif` | Compare a baseline assessment with a modified scenario |
| GET | `/analytics` | Retrieve configured model analytics |
| GET | `/health` | Check backend health and available model metrics |

Refer to [`docs/API.md`](docs/API.md) for request and response examples.

The interactive Swagger UI is available at `http://localhost:8000/docs` while the backend is running.

## Example Use Case

Consider a small retail business that has limited traditional credit history but maintains digital transaction records and regular business activity.

CredEcho can process available indicators such as:

- GST filing consistency.
- Monthly revenue and expenses.
- UPI transaction activity.
- Cash flow stability.
- Invoice payment delays.
- Debt ratio and credit utilization.
- Business age and operational indicators.

The application can then display a financial health score, a risk category, relevant contributing factors, and an indicative recommendation.

A user may also explore a what-if scenario, such as improving GST filing consistency, to understand how a changed input affects the model's output.

All displayed scores and recommendations depend on the implemented model and supplied data. They are illustrative decision-support outputs, not guarantees of repayment or credit approval.

## Security and Data Privacy

Financial data requires careful handling. Before using CredEcho with real businesses:

- Obtain appropriate authorization and consent for data collection.
- Avoid committing API keys, passwords, tokens, or production secrets.
- Exclude private financial information and personally identifiable information from public repositories.
- Validate and sanitize incoming API requests.
- Use appropriate authentication, authorization, and access controls.
- Configure secure database credentials and encrypted connections.
- Review the handling and retention of uploaded or processed data.
- Verify the security of model artifacts and third-party dependencies.
- Ensure that lending decisions comply with applicable laws, regulations, and fairness requirements.

The repository's synthetic datasets are intended for development and demonstration. Do not assume that the application is production-ready for financial decision-making.

## Limitations and Future Enhancements

Potential future improvements include:

- Integration with authorized financial data providers.
- Secure Account Aggregator consent-based data access.
- Improved validation on representative real-world MSME datasets.
- Fairness and bias evaluation across relevant business segments.
- More robust explainability and model monitoring.
- Role-based access control for bank officers and business users.
- Automated testing and continuous integration.
- Production-grade database migrations and deployment configuration.
- Improved audit trails and decision records.
- Secure PDF export and sharing of Financial Health Cards.

These are proposed enhancements and should not be interpreted as already implemented features.

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the affected components.
5. Submit a pull request with a clear description of the changes.

Please avoid submitting sensitive financial information, credentials, or datasets that you do not have permission to share.

## License

This project is distributed under the MIT License, provided that the repository owner has the necessary rights to license the included code and assets.

See the [`LICENSE`](LICENSE) file for the complete license text.

---

**CredEcho — Turning alternative financial signals into clearer MSME financial insights.**
