class GenerateQuestionsParameters(object):
    def __init__(self, count: int):
        self.count = count


class EvaluateSolutionParameters(object):
    def __init__(self, question: str, answer: str, assumed_answer: str):
        self.question = question
        self.answer = answer
        self.assumed_answer = assumed_answer
