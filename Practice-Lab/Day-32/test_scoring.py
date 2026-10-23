from app import evaluate_answer


def test_required_keywords_are_scored():
    case = {
        "question": "What is Python?",
        "must_include": ["programming language", "automation"],
        "context": "",
        "expected_format": "paragraph"
    }

    result = evaluate_answer(
        case,
        "Python is a programming language used for automation."
    )

    assert result["completeness"] == 100
    assert result["passed"] is True


def test_missing_required_keywords_reduce_score():
    case = {
        "question": "What is Python?",
        "must_include": ["programming language", "automation", "quantum computing"],
        "context": "",
        "expected_format": "paragraph"
    }

    result = evaluate_answer(case, "Python is useful.")

    assert result["completeness"] == 0


def test_context_enables_groundedness_score():
    case = {
        "question": "How long is the trial?",
        "must_include": ["14 days"],
        "context": "The software trial lasts 14 days.",
        "expected_format": "paragraph"
    }

    result = evaluate_answer(
        case, "The trial lasts 14 days."
    )

    assert result["groundedness"] is not None
    assert result["completeness"] == 100