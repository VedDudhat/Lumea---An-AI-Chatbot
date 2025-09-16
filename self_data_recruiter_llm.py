from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_core.messages import AnyMessage, ToolMessage
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
from embedding_model import Model
import warnings
warnings.filterwarnings("ignore")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=""
)

entry_condition_msg = """ 
You are an AI assistant specifically designed to classify user input into two distinct conditions.
User_input is : {input}
strictly follow these rules:

1. **Job Description or Resume-Related Task → false:**  
   - If the input contains *job descriptions* (e.g., "Software engineer with 5 years of experience"),  
   - Or refers to *resume retrieval tasks* (e.g., "Find candidates with Python skills" or "Get resumes for HR roles"),
   - Or eveny a single word which state a profession or job,  
   - **Return false** as the condition.  

2. **Questions or Inquiry → true:**  
   - If the input is in the form of a question (e.g., "What are the skills?", "Tell me about John", "How many years of experience?"),  
   - Or includes any query about a person or any other text which does not include the job description,
   - Or includes greetings or conversational queries (e.g., "Hi", "How are you?", "What can you do?"),  
   - **Return true** as the condition.  

**Strictly return only true or false** based on the given conditions without any errors or additional content.
"""

llm_tool_msg = """
You are AI assistant, an intelligent assistant specifically designed to call tools based on the user input, and call the appropriate tool accordingly.
 user_input: {input}, 
 strictly follow these rules:

1. **Fewer than 15 Words or Improper Job Description → jd_generation:**  
   - If the input contains a *job description* with fewer than *15 words* or lacks detail (e.g., "HR with 5 years experience", "developer needed"),  
   - **Call the jd_generation tool** to generate a more detailed job description.  

2. **15 or More Words or Proper Job Description → get_resume:**  
   - If the input contains a *detailed job description* with *15 or more words* (e.g., "Looking for a Senior Software Engineer with 7 years of experience in Python and AWS cloud services"),  
   - **Call the get_resume tool** to retrieve relevant resumes.  

*Strictly follow the conditions* and call the appropriate tool based on the *length and quality of the job description* without any errors.
"""

resume_message = """
For each resume provided {Resume} which were retrieved based on the job description, provided by user,
extract information from it and present the following details in a structured manner:  

1 **Summary**: A brief overview of the candidate's professional background.  
2 **Key Skills**: List the most relevant skills based on the resume.  
3 **Standout Features**: Highlight what makes this candidate unique (e.g., exceptional achievements, rare skills, leadership experience, certifications).  
4 **Contact Information**: At the end of the summary, provide:  
   - **Name**  
   - **Email**  
   - **Phone Number**  

 **Important Rules:**  
- Do not generate or assume information that is not present in the resume.  
- Keep responses structured and professional.  
- If a specific detail is missing in the resume, state “Not Provided” instead of making assumptions.  
- Focus on clarity and readability.  

🔹 **Example Output Format:**  

**Candidate 1:**  
📌 **Summary**: [Brief professional background]  
📌 **Key Skills**: [Skill 1, Skill 2, Skill 3, …]  
📌 **Standout Features**: [Notable achievements, unique qualifications]  
📌 **Contact Information:**  
- **Name**: [Full Name]  
- **Email**: [Email Address]  
- **Phone**: [Phone Number]  

Repeat this format for each retrieved resume.
Strickly follow the format and at the end ask user what they want to do next.
now you cannot use any tools that are provided to you.
"""

QnA_msg = """ 
You are a helpful and professional AI assistant named Stella designed to assist users with resume retrieval and job matching. Your primary tasks include:

Understanding the user's current query.

Considering the entire conversation history for context.

Utilizing the retrieved resumes to provide relevant insights.

Engaging in natural conversation while keeping the user on track.

Instructions:

If the user's query is directly related to resumes or job descriptions, respond with relevant insights using the retrieved resumes.

If the user asks a general question, engage in normal conversation while subtly guiding them back to the task if they go off-topic.

If the user strays too far from the main objective (resume retrieval and job matching), politely remind them of their goal and ask how you can assist with it.

User input is: {input}

Retrieved resumes are : {resume}

"""

@tool
def jd_generation(msg: str) -> str:
    """
    Extracts job description from the user input that will be used for retrieveing the resumes.
    """
    
    prompt = PromptTemplate.from_template(
        """Generate a concise job description based on the following user input: {user_input}.
    
        - Ensure the description is at least 10 words long.
        - Include essential keywords relevant to the role, without unnecessary details.
        - Structure the description to maximize relevance for resume retrieval from a vector store.
        - Avoid any introductory or concluding statements—output only the job description."""
    )
    formatted_prompt = prompt.format(user_input=msg)
    result = llm.invoke(formatted_prompt)
    return str(result.content)

@tool
def get_resume(job_description: str) -> dict:
    """
    This is a tool which is used to retrieve the resumes based on the job description.
    """
    model = Model()
    Document = model.search_from_temp_database(job_description)
    print(Document)
    Resumes = Document.get("Document","Unable to retrive relevant resumes")
    return Resumes

tools = [jd_generation,get_resume]

class Agentstate(TypedDict):
    user_input: Annotated[list[str], operator.add]
    msg: Annotated[list[AnyMessage], operator.add]
    resumes: list[list[str]]
    job_description: Annotated[list[str], operator.add]

class Agent:

    def __init__(self, checkpointer):
        self.model = llm
        self.tools = {t.name : t for t in tools}
        builder = StateGraph(Agentstate)
        builder.set_conditional_entry_point(
            self.conditional_entry ,
            {True:"QnA",False:"llm"}
        )
        builder.add_node("llm", self.llm)
        builder.add_conditional_edges(
            "llm",
            self.llm_condition ,
            {True:"tool",False:END}
        )
        builder.add_node("tool", self.tool )
        builder.add_conditional_edges(
            "tool",
            self.tool_condition ,
            {True:"llm Summary", False:"llm"}
        )
        builder.add_node("llm Summary", self.llm_summary )
        builder.add_node("QnA", self.QnA )
        builder.add_edge("llm Summary",END)
        builder.add_edge("QnA",END)
        self.graph = builder.compile(checkpointer=checkpointer)
        self.model = self.model.bind_tools(tools)
    
    def conditional_entry(self, state: Agentstate):
        prompt = entry_condition_msg
        decision_prompt = PromptTemplate.from_template(prompt)
        formatted_decision_prompt = decision_prompt.format(input = state['user_input'][-1])
        result = self.model.invoke(formatted_decision_prompt)
        # print(result)
        if result.content == "true":
            return True
        if result.content == "false":
            return False
        else:
            print("Error in making the decisoion of ")

    def llm(self, state: Agentstate):
        print("llm node")
        prompt = llm_tool_msg
        decision_prompt = PromptTemplate.from_template(prompt)
        formatted_decision_prompt = decision_prompt.format(input=state["user_input"][-1])
        response = self.model.invoke(formatted_decision_prompt)
        return {"msg": [response]}
    
    def llm_condition(self, state: Agentstate):
        print("llm_condition node")
        if len(state["msg"][-1].tool_calls) > 0:
            print(state["msg"])
            return True
        else:
            return False

    def tool(self, state: Agentstate):
        print("tool node")
        # print(state["msg"])
        tool_call = state["msg"][-1].tool_calls
        for t in tool_call:
            tool_name = t.get('name')
            tool_args = t.get('args')
            result = self.tools[tool_name].invoke(tool_args)
            if tool_name == "jd_generation":
                print("     jd_generation called")
                return {
                    "msg": [ToolMessage(name=tool_name,tool_call_id=t.get('id'),content=str(result))],
                    "user_input": [str(result)]  
                }
            if tool_name == "get_resume":
                print("     get_resume called")
                return {
                    "msg": [ToolMessage(name=tool_name,tool_call_id=t.get('id'),content=str(result))],
                    "resumes": [result],
                    "latest_resume": result
                    }
              

    def tool_condition(self, state: Agentstate):
        print("tool_condition node")
        # print(state["resumes"])
        # print(state["user_input"])
        resumes = state.get("resumes", [])
        if resumes:
            if state["msg"][-1].name == "jd_generation":
                print("     Returning False")
                return False
            else:
                print("     Returning True")
                return True
        else:
            print("     Returning False")
            return False

    def llm_summary(self, state: Agentstate):
        print("llm_summary node")
        resumes = state["resumes"]
        resume_prompt = PromptTemplate.from_template(resume_message)
        fomratted_resume_prompt = resume_prompt.format(Resume=resumes)
        output = self.model.invoke(str(fomratted_resume_prompt))
        print(state)
        return {
            "msg": [output]
        }

    def QnA(self, state: Agentstate):
        print("QnA node")
        prompt = QnA_msg
        QnA_prompt = PromptTemplate.from_template(prompt)
        formatted_QnA_prompt = QnA_prompt.format(input=state["user_input"],resume=state.get("resumes",["None"]))
        response = self.model.invoke(formatted_QnA_prompt)
        print(state)
        return {
            "msg": [response]
        }

# memory = InMemorySaver()
# thread = {"configurable": {"thread_id": "1"}}
# abot = Agent(memory)
# from IPython.display import Image, display

# display(Image(abot.graph.get_graph().draw_png()))
