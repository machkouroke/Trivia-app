from flask import abort

QUESTIONS_PER_PAGE = 10


def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    if page < 1:
        abort(400, "Page number must be greater than 0")
    if page > len(data) // QUESTIONS_PER_PAGE + 1:
        abort(400, f"Page number must be less than or equal to {len(data) // QUESTIONS_PER_PAGE + 1}")
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return data[start:end]
