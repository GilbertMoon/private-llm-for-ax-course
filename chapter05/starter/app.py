import streamlit as st

from rag import build_index, generate_answer, retrieve


st.set_page_config(page_title="Private AI Assistant", page_icon="🔒")
st.title("🔒 Private AI Assistant")
st.caption("교육용 샘플 회사 규정을 기반으로 답변합니다.")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "index" not in st.session_state:
    try:
        with st.spinner("문서 인덱스를 준비하고 있습니다..."):
            st.session_state.index = build_index()
    except Exception as exc:
        st.error(f"초기화 오류: {exc}")
        st.stop()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input("회사 규정에 대해 질문해 보세요.")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.status("관련 문서를 검색하고 답변을 생성하고 있습니다...", expanded=False):
            retrieved = retrieve(question, st.session_state.index)
            answer = generate_answer(question, retrieved)

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("Retrieval Evidence / Source"):
                for item in retrieved:
                    st.markdown(
                        f"**{item['source']} / chunk {item['chunk_id']} / score {item['score']:.4f}**"
                    )
                    st.write(item["text"])

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as exc:
        st.error(f"처리 중 오류가 발생했습니다: {exc}")
