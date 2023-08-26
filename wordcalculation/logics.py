import json
import jsonschema
from wordcalculation import parameters
import openai
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)


def generate_questions(param: parameters.GenerateQuestionsParameters):
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "number",
                            "description": "連番",
                        },
                        "question": {
                            "type": "string",
                            "description": "問題"
                        },
                        "answer": {
                            "type": "string",
                            "descriotion": "想定する回答"
                        }
                    },
                    "required": ["id", "question"],
                },
                "minItems": param.count,
                "maxItems": param.count,
            }
        },
        "required": ["items"]
    }
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content":
                     f'''
                     言葉の意味の加算減算ゲームがあります。
                     ルールは以下の通り。
                     ・問題に使用する言葉は実在する1つの単語であること。
                     ・回答は実在する1つの単語として導き出せること。
                     ・回答は問題文の式の中で使用していない単語であり、実在する単語であること。
                     
                     例題です。
                     Q:「王様」-「男性」+「女性」= ?
                     A:「女王」
                     
                     Q:「パリ」-「フランス」+「日本」= ?
                     A:「東京」
                     続けて{param.count}問、問題と想定する回答を作成してください。
                     '''}
                ],
                functions=[{
                    "name": "generateQuestion",
                    "description": "生成した問題を全て返す",
                    "parameters": schema
                }],
                function_call={"name": "generateQuestion"})
            message = response['choices'][0]['message']  # type: ignore
            args = message['function_call']['arguments']
            ret = json.loads(args)
            jsonschema.validate(ret, schema)
            return ret
        except Exception as e:
            logging.error(e)
            continue


def evaluate_solution(param: parameters.EvaluateSolutionParameters):
    schema = {
        "type": "object",
        "properties": {
            "answer1_score": {
                "type": "number",
                "description": "answer1の点数",
            },
            "answer2_score": {
                "type": "number",
                "description": "answer2の点数",
            },
            "comment": {
                "type": "string",
                "description": "コメントを日本語で書く",
            },
        },
        "required": ["answer1_score", "answer2_score", "comment"]
    }
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": '''
                     言葉の意味の加算減算ゲームというゲームがあります。
                     例題です。
                     Q:王様-男性+女性= ?
                     A:女王
                     
                     Q:パリ-フランス+日本= ?
                     A:東京
                     
                     あなたは採点を担当し、問題文から導き出される意味と実際の回答の意味を比較し、どの程度近いか100点満点を採点、その理由を日本語で説明してください。
                     以下の問題について、2つの回答それぞれを採点してください。
                     '''},
                    {"role": "user", "content":
                     f'''question: {param.question}
                     answer1: {param.answer}
                     answer2: {param.assumed_answer}
                     '''}
                ],
                functions=[{
                    "name": "evaluateSolution",
                    "description": "evaluate the solution",
                    "parameters": schema
                }],
                function_call={"name": "evaluateSolution"})
            msg = response['choices'][0]['message']  # type: ignore
            args = msg['function_call']['arguments']
            ret = json.loads(args)
            jsonschema.validate(ret, schema)
            return ret
        except Exception as e:
            logging.error(e)
            continue
