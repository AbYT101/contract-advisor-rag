# Contract Advisor RAG: High-Precision Legal Expert LLM APP

## Overview

**Lizzy AI** is an early-stage Israeli startup, developing the next-generation contract AI. We leverage Hybrid LLM technology (edge, private cloud, and LLM services) to build the first fully autonomous artificial contract lawyer. Our goal is to develop a fully autonomous contract bot, capable of drafting, reviewing, and negotiating contracts independently, end-to-end, without human assistance.

This repository contains the codebase for building, evaluating, and improving a Retrieval-Augmented Generation (RAG) system for Contract Q&A (chatting with a contract and asking questions about the contract).

## Business Objective

Develop a powerful contract assistant using RAG technology, which combines the capabilities of large language models with the richness of external data sources to provide accurate, informed, and context-rich outputs.

## Features

- **File Upload**: Upload a `.docx` file containing contract text.
- **Text Retrieval**: Retrieve relevant sections of the contract based on a query.
- **Text Generation**: Generate answers to questions based on the contract content.
- **Microsoft word integration**: Microsoft word integration.


## Directory Structure

```plaintext
contract-advisor-rag/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   └── services/
│   ├── models/
│   ├── data/
│   ├── utils/
│   ├── tests/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   └── index.js
├── notebooks/
├── scripts/
│   ├── setup.sh
│   └── run_tests.sh
├── .gitignore
└── README.md
```

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/contract-advisor-rag.git
    cd contract-advisor-rag/backend
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the flask api**:
    ```sh
    python main.py
    ```

## Usage

1. **Run the React app**:
    ```sh
    cd frontend/
    npm start
    ```

2. **API Endpoints**:
    - **Upload File**: `POST /api/upload`
        - Upload a `.docx` file.
    - **Generate Answer**: `POST /api/generate`
        - Generate answers to questions based on the contract content.
    - **Register**: `POST /api/register`
        - Register to the app.
    - **Login**: `POST /api/login`
        - Login to the app, returns a jwt token.


## Contributing

We welcome contributions to improve the Contract Advisor RAG system. Please fork the repository and submit pull requests.

## License

This project is licensed under the Apache-2.0 license. 

## Contributors

- [@abyt101](https://github.com/AbYT101) - Abraham Teka

## Contact

For any questions or suggestions, please contact aberhamyisaw@gmail.com.

## Challenge by

![10 Academy](https://static.wixstatic.com/media/081e5b_5553803fdeec4cbb817ed4e85e1899b2~mv2.png/v1/fill/w_246,h_106,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/10%20Academy%20FA-02%20-%20transparent%20background%20-%20cropped.png)