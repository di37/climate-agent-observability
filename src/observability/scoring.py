"""Automatic scoring utilities for quality evaluation."""

import logging

logger = logging.getLogger(__name__)


def score_response(langfuse, observation_id: str, trace_id: str, response: str, question: str):
    """
    Add automatic quality scores to a trace.
    This populates the "Scores" section in Langfuse dashboard.
    
    Args:
        langfuse: Langfuse client instance
        observation_id: Observation ID for the query
        trace_id: Trace ID for the query
        response: Agent's response text
        question: User's question text
    """
    logger.debug(f"Adding automatic scores to trace {trace_id}")
    
    # Score 1: Response Length (detailed-ness)
    response_length = len(response.split())
    length_score = min(1.0, response_length / 100)  # 0-1 scale
    
    langfuse.create_score(
        trace_id=trace_id,
        observation_id=observation_id,
        name="response_length",
        value=length_score,
        comment=f"Response has {response_length} words"
    )
    
    # Score 2: Data-backed response (checks if SQL was used)
    has_data = "Query returned" in response or "records" in response.lower()
    data_score = 1.0 if has_data else 0.5
    
    langfuse.create_score(
        trace_id=trace_id,
        observation_id=observation_id,
        name="data_backed",
        value=data_score,
        comment="Response includes actual database results" if has_data else "Response may lack data"
    )
    
    # Score 3: Completeness (checks for key elements)
    completeness_checks = [
        "top" in response.lower() or "average" in response.lower(),
        any(str(i) in response for i in range(10)),  # Has numbers
        len(response) > 50  # Substantial response
    ]
    completeness_score = sum(completeness_checks) / len(completeness_checks)
    
    langfuse.create_score(
        trace_id=trace_id,
        observation_id=observation_id,
        name="completeness",
        value=completeness_score,
        comment=f"Response completeness: {completeness_score:.0%}"
    )
    
    # Score 4: Relevance (simple keyword matching)
    question_words = set(question.lower().split())
    response_words = set(response.lower().split())
    overlap = len(question_words & response_words)
    relevance_score = min(1.0, overlap / max(len(question_words), 1))
    
    langfuse.create_score(
        trace_id=trace_id,
        observation_id=observation_id,
        name="relevance",
        value=relevance_score,
        comment=f"Question-response overlap: {overlap} words"
    )
    
    logger.debug(f"Added 4 automatic scores to trace {trace_id}")


def add_user_feedback_score(langfuse, trace_id: str, observation_id: str, 
                            feedback: str, comment: str = ""):
    """
    Add user feedback score to a trace.
    
    Args:
        langfuse: Langfuse client instance
        trace_id: The trace ID
        observation_id: The observation ID
        feedback: "positive", "negative", or numeric value (0-1)
        comment: Optional user comment
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert feedback to numeric score
        if feedback.lower() == "positive" or feedback == "👍":
            score_value = 1.0
            score_comment = f"User feedback: Positive. {comment}".strip()
        elif feedback.lower() == "negative" or feedback == "👎":
            score_value = 0.0
            score_comment = f"User feedback: Negative. {comment}".strip()
        else:
            # Assume numeric value (accepts decimals)
            score_value = float(feedback)
            if not (0.0 <= score_value <= 1.0):
                logger.warning(f"Score value {score_value} out of range, clamping to 0-1")
                score_value = max(0.0, min(1.0, score_value))
            score_comment = f"User feedback: {score_value}. {comment}".strip()
        
        # Add user feedback score
        langfuse.create_score(
            trace_id=trace_id,
            observation_id=observation_id,
            name="user_feedback",
            value=score_value,
            comment=score_comment
        )
        
        logger.info(f"User feedback added to trace {trace_id}: {feedback}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid feedback value: {feedback} - {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to add user feedback: {e}")
        return False

