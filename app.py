import streamlit as st
from schema_extractor import SchemaExtractor
from nl2sql import NL2SQL
from db_executor import DBExecutor
from answer_generator import AnswerGenerator
import pandas as pd

st.title("🎯 SQL Query Assistant")
st.write("Ask questions about the Chinook music database in plain English!")

# Store query history across interactions
if "history" not in st.session_state:
    st.session_state.history = []

@st.cache_resource
def load_modules():
    """Initialize and cache heavy components (DB, LLM, schema)."""
    extractor = SchemaExtractor("chinook.db")
    schema = extractor.get_schema()
    return schema, NL2SQL(), DBExecutor("chinook.db"), AnswerGenerator()

schema, nl2sql, executor, generator = load_modules()

question = st.text_input("Ask a question:")

def show_chart(results):
    """Render bar chart if result is (label, numeric value) format."""
    if not results or len(results[0]) != 2:
        return
    if not isinstance(results[0][1], (int, float)):
        return

    df = pd.DataFrame(results, columns=["Label", "Value"])
    st.subheader("📊 Chart")
    st.bar_chart(df.set_index("Label"))

if st.button("Ask"):
    if not question:
        st.error("⚠️ Please enter a question!")
    else:
        try:
            with st.spinner("Thinking..."):
                sql_query = nl2sql.generate_sql(question, schema)

                st.subheader("Generated SQL:")
                st.code(sql_query, language="sql")

                results = executor.run_query(sql_query)

                answer = generator.generate_answer(question, sql_query, results)

                st.subheader("Answer:")
                st.success(answer)

                show_chart(results)

                # Save to history
                st.session_state.history.append({
                    "question": question,
                    "sql": sql_query,
                    "answer": answer
                })

        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ API quota exceeded. Please wait and try again.")
            else:
                st.error(f"Something went wrong: {str(e)}")

# Display history
if st.session_state.history:
    st.divider()
    st.subheader("🕐 Query History")

    for item in reversed(st.session_state.history):
        st.write(f"**Q:** {item['question']}")
        st.code(item['sql'], language="sql")
        st.success(item['answer'])
        st.divider()
