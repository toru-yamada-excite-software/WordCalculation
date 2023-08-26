#!/usr/bin/env python
from wordcalculation import logics
from wordcalculation import parameters
import streamlit as st
import json


def main():
    st.title("WordCalculation")
    if 'questions' not in st.session_state:
        st.session_state.count = 0
        count_t = st.text_input("問題数を入力してください：", str(st.session_state.count))
        st.session_state.input1 = st.button("送信", key="keyx")
        if not st.session_state.input1:
            return
        st.session_state.count = int(count_t)
        param = parameters.GenerateQuestionsParameters(int(count_t))
        st.session_state.questions = logics.generate_questions(param)

    if 'answers' not in st.session_state:
        st.session_state.answers = [{} for _ in range(
            len(st.session_state.questions["items"]))]

    for item in st.session_state.questions["items"]:
        st.write("問題：")
        st.write(item["question"])
        answer = st.text_input(
            "回答：", st.session_state.answers[item["id"]-1]["answer"] if "answer" in st.session_state.answers[item["id"]-1] else "", key=f"answer{item['id']}")
        if (not "answered" in st.session_state.answers[item["id"] - 1]):
            if st.button("送信", key=f"key{item['id']}"):
                st.session_state.answers[item["id"] -
                                         1]["answered"] = True
        if not "answered" in st.session_state.answers[item["id"] - 1] or not st.session_state.answers[item["id"] - 1]["answered"]:
            print(st.session_state)
            return
        st.session_state.answers[item["id"]-1]["answer"] = answer
        if not "score" in st.session_state.answers[item["id"]-1]:
            param_solution = parameters.EvaluateSolutionParameters(
                item["question"], answer, item["answer"])
            st.session_state.answers[item["id"]-1]["score"] = logics.evaluate_solution(
                param_solution)

        st.write("正解" if st.session_state.answers[item["id"]-1]["score"]["answer1_score"] >=
                 st.session_state.answers[item["id"]-1]["score"]["answer2_score"] else "不正解")
        st.write(f"想定回答：{item['answer']}")
        st.write(st.session_state.answers[item["id"]-1]["score"]["comment"])
    st.write("Thank you for your playing.")


main()
