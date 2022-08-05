# Udacitrivia

## What is Udacitrivia?

Trivia is a simple and complete general knowledge application to pass your free time

![image](https://user-images.githubusercontent.com/40785379/183159243-b76679a8-6022-4b2e-88ed-6b1ea8350f6b.png)

## Getting Started

To try the application at home, you will have to launch the backend server then the frontend one

### Backend

This directory contains the question generation API that you could also use for your personal
project ([See API documentation](#api-documentation)).

> View the [Backend README](./backend/README.md) for more details .

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask
server.

## <span id="api-documentation">API Reference</span>

### Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the
default,
`http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```

The API will return four error types when requests fail:

- `400`: Bad Request
  This error is returned when the request is not well-formed (For example the keys of the request object are wrong)
  or missing required parameters.
  Example: In this case, we have an error in the success
    ```json
    {
      "previous_questions": [1, 4, 20, 15],
      "quiz_category": "current category"
    }
    ```
- `404`: Resource Not Found
  This error is returned when the resource (Questions , categories or juste a simple page) is not found.
  The error is usually in the url
- `422`: Not Processable
  This error is returned when the request is well-formed but the server was unable to process it.
  This error can appear when you try to create a question with a category that does not exist
- `500`: Internal Server Error
  This error is returned when the server encounters an internal error.
  This error is usually when the server is not able to process the request.

### Endpoints

#### GET `/categories`

- General:
    - Returns a list of all questions categories, success value
    - If there are many categories this query will be paginated and the `page` argument must be used to specify the page
      to be returned.
- Sample:`curl http://127.0.0.1:5000/categories`
    ```json
    {
      "success": true,
      "categories": [
        {
          "type": "Science",
          "id": 1
        },
        {
          "type": "Sports",
          "id": 2
        },
        {
          "type": "Geography",
          "id": 3
        },
        {
          "type": "History",
          "id": 4
        },
        {
          "type": "Art",
          "id": 5
        },
        {
          "type": "Entertainment",
          "id": 6
        },
        {
          "type": "Politics",
          "id": 7
        },
        {
          "type": "Animals",
          "id": 8
        },
        {
          "type": "General Knowledge",
          "id": 9
        }
      ]
    }
    ```

#### GET `/categories/${id}/questions`

- General:
    - Returns a list of all questions in a category, success value
    - If there are many questions this query will be paginated and the `page` argument must be used to specify the page
      to be returned.
- Sample:`curl http://127.0.0.1:5000/categories/2/questions`
    ```json
    {
  "success": true,
  "questions": [
       {
         "id": 1,
         "question": "This is a question",
         "answer": "This is an answer",
         "difficulty": 5,
         "category": 4
       }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
    }
    ```

#### GET `/questions`

- General:
    - Returns a list of all questions, success value
    - If there are many questions this query will be paginated and the `page` argument must be used to specify the page
      to be returned.
- Sample:`curl http://127.0.0.1:5000/questions`
    ```json
    {
  "success": true,
  "categories": {
     "1": "History",
     "2": "Art",
     "3": "Tech",
     "5": "Entertainment",
     "6": "Sports",
     "7": "Geography"
  },
  "questions": [
       {
         "id": 1,
         "question": "This is a question",
         "answer": "This is an answer",
         "difficulty": 5,
         "category": 4
       }
  ],
  "totalQuestions": 100,
  "currentCategory": null
    }
    ```

#### POST `/questions`

- General:
    - Creates a new question, success value
    - The request body must contain a JSON object with the following keys:
        - `question`: The question itself
        - `answer`: The answer to the question
        - `difficulty`: The difficulty of the question (1-5)
        - `category`: The category of the question
- Sample:
  `
  curl -X POST -H "Content-Type: application/json" -d '{"question": "This is a question", "answer": "This is an
  answer", "difficulty": 5, "category": 4}' http://127.0.0.1:5000/questions
  `

    ```json
    {
      "success": true,
      "message": "Question added successfully"
    }
    ```

#### DELETE `/questions/${id}`

- General:
    - Deletes a given question
- Sample:`curl -X DELETE http://127.0.0.1:5000/questions/2
    ```json
    {
      "success": true,
      "message": "Question with id:2 is deleted"
    }
    ```

#### POST `/questions/search`

- General:
    - Searches for questions based on a given search term
    - The request body must contain a JSON object with the following keys:
        - `searchTerm`: The search term
- Sample (search for "history"):
  `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "history"}' http://127.0.0.1:5000/questions/search`
    ```json
    {
      "success": true,
      "questions": [
        {
          "id": 1,
          "question": "This is a history question",
          "answer": "This is an answer",
          "difficulty": 5,
          "category": 4
        }
      ],
      "totalQuestions": 100
    }
    ```

#### POST `/quizzes`

- General:
    - Starts a new quiz based on a given category
    - The request body must contain a JSON object with the following keys:
        - `quiz_category`: The category of the quiz
        - `previous_questions`: The previous questions already answered
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"type": "History", "id": 4},
  "previous_questions": [1, 4, 20, 15]}' http://127.0.0.1:5000/quizzes`
    ```json
    {
      "success": true,
      "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
      }
    }
    ```
