from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  
db = client['quiz_app']
quizzes_collection = db['quizzes']

# Quiz data to insert
quizzes_data = [
    {
        "subject": "Data Structures",
        "questions": [
            {
                "question": "Which of the following data structures uses LIFO order?",
                "choices": ["Queue", "Stack", "Array", "Linked List"],
                "answer": "Stack"
            },
            {
                "question": "What is the time complexity of searching in a binary search tree (BST) in the average case?",
                "choices": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
                "answer": "O(log n)"
            },
            {
                "question": "Which data structure is used in implementing BFS (Breadth-First Search)?",
                "choices": ["Stack", "Queue", "Heap", "Linked List"],
                "answer": "Queue"
            }
        ]
    },
    {
        "subject": "Computer Networks",
        "questions": [
            {
                "question": "What is the purpose of the OSI model?",
                "choices": ["To standardize networking protocols", "To design hardware", "To specify algorithms", "None of the above"],
                "answer": "To standardize networking protocols"
            },
            {
                "question": "Which layer in the OSI model is responsible for routing?",
                "choices": ["Transport", "Network", "Data Link", "Session"],
                "answer": "Network"
            },
            {
                "question": "What is an IP address?",
                "choices": ["A physical address", "A logical address", "A MAC address", "None of the above"],
                "answer": "A logical address"
            }
        ]
    },
    {
        "subject": "Machine Learning",
        "questions": [
            {
                "question": "Which of the following is a supervised learning algorithm?",
                "choices": ["K-means", "Linear regression", "Apriori", "DBSCAN"],
                "answer": "Linear regression"
            },
            {
                "question": "What is overfitting in machine learning?",
                "choices": ["Model performs well on test data", "Model performs well on training data but poorly on test data", "Model performs poorly on all data", "None of the above"],
                "answer": "Model performs well on training data but poorly on test data"
            },
            {
                "question": "Which of the following is used to reduce the dimensionality of a dataset?",
                "choices": ["PCA", "Gradient Descent", "Backpropagation", "Linear Regression"],
                "answer": "PCA"
            }
        ]
    },
    {
        "subject": "Operating Systems",
        "questions": [
            {
                "question": "Which of the following is a real-time operating system?",
                "choices": ["Windows", "Linux", "RTOS", "macOS"],
                "answer": "RTOS"
            },
            {
                "question": "What is virtual memory?",
                "choices": ["Physical memory", "An abstraction of memory", "Secondary storage", "None of the above"],
                "answer": "An abstraction of memory"
            },
            {
                "question": "What is a system call?",
                "choices": ["A function call in the kernel", "A call to hardware", "A user-defined function", "None of the above"],
                "answer": "A function call in the kernel"
            }
        ]
    },
    {
        "subject": "ADBMS",
        "questions": [
            {
                "question": "Which of the following is a characteristic of a distributed database?",
                "choices": ["Centralized storage", "Data stored at multiple locations", "Single access point", "None of the above"],
                "answer": "Data stored at multiple locations"
            },
            {
                "question": "In a relational database, what does normalization aim to achieve?",
                "choices": ["Eliminate redundancy", "Improve performance", "Ensure security", "None of the above"],
                "answer": "Eliminate redundancy"
            },
            {
                "question": "What is the primary key in a relational database?",
                "choices": ["A unique identifier for each record", "A foreign key", "A data attribute", "None of the above"],
                "answer": "A unique identifier for each record"
            }
        ]
    }
]

# Insert quizzes into the MongoDB collection
for quiz in quizzes_data:
    quizzes_collection.update_one(
        {"subject": quiz["subject"]},
        {"$set": quiz},
        upsert=True
    )

print("Quizzes inserted/updated successfully.")
