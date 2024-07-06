import os
import sys
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision, answer_correctness
from datasets import Dataset

# Assuming these functions are defined elsewhere and imported correctly
from api.services import retriever_service, generator_service, bm_25_cosine_retriever_service, bm25_retriever

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

questions = [
    "Under what circumstances and to what extent the Sellers are responsible for a breach of representations and warranties?",
    "Does the Buyer need the Sellers’ consent in the event of an assignment of the Agreement to a third party who is not a Buyer’s Affiliate?",
    "Would the Sellers be responsible if after the closing it is determined that there were inaccuracies in the representation provided by them where such inaccuracies are the result of the Sellers’ gross negligence?",
    "How much is the escrow amount?",
    "Is escrow amount greater than the Retention Amount?",
    "What is the purpose of the escrow?",
    "May the Escrow Amount serve as a recourse for the Buyer in case of breach of representations by the Company?",
    "Are there any conditions to the closing?",
    "Are Change of Control Payments considered a Seller Transaction Expense?",
    "Would the aggregate amount payable by the Buyer to the Sellers be affected if it is determined that the actual Closing Debt Amount is greater the estimated Closing Debt Amount?",
    "Does the Buyer need to pay the Employees Closing Bonus Amount directly to the Company’s employees?",
    "Does any of the Sellers provide a representation with respect to any Tax matters related to the Company?",
    "Is any of the Sellers bound by a non-competition covenant after the Closing?",
    "Whose consent is required for the assignment of the Agreement by the Buyer?"
]

ground_truths = [
    ["Except in the case of fraud, the Sellers have no liability for breach of representations and warranties (See section 10.01)"],
    ["No. If the assignment is not part of a sale of all or substantially all of the Buyer’s assets, the assignment requires the consent of the Company and the Seller’s Representative."],
    ["No"],
    ["The escrow amount is equal to $1,000,000."],
    ["No."],
    ["To serve as a recourse of the Buyer in case of post-closing adjustments of the purchase price. (See section 2.07(e))."],
    ["No"],
    ["No, as the signing and closing are simultaneous."],
    ["Yes. (See defining of Sellers Transaction Expenses)."],
    ["Yes (See Section 2.07)"],
    ["No. (See Section 2.10)"],
    ["No. Only the Company provides such a representation."],
    ["No."],
    ["If the assignment is to an Affiliate or purchaser of all of the Buyer’s assets, no consent is required. Otherwise, the consent of the Company and the Seller Representative is required."]
]


def main():
    answers = []
    contexts = []

    # Create retriever
    retriever = retriever_service.create_retriever()

    # Inference
    for query in questions:
        generated_prompts = generator_service.generate(query, retriever)
        result = retriever.invoke(query)
        answers.append(generated_prompts)
        contexts.append([doc.page_content for doc in result])

    # Prepare data for evaluation
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truths": ground_truths
    }

    # Convert dict to dataset
    dataset = Dataset.from_dict(data)

    # Evaluation
    result = evaluate(
        dataset=dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
            answer_correctness
        ],
    )
    print("The evaluation result is", result)
    df = result.to_pandas()
    print(df)

if __name__ == "__main__":
    main()
