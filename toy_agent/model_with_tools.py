from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Define the tools
@tool
def get_square_area(side: float) -> float:
    """Calculate the area of a square given the length of its side."""
    return side ** 2

@tool
def get_circle_area(radius: float) -> float:
    """Calculate the area of a circle given its radius."""
    return 3.14159 * (radius ** 2)

# Initialize the LLM and bind tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [get_square_area, get_circle_area]
llm_with_tools = llm.bind_tools(tools)

# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in geometry. Help users solve simple geometry problems using the available tools."),
    ("human", "{input}"),
])

# Create the chain
chain = prompt | llm_with_tools

def main():
    print("Welcome to the Geometry Agent!")
    print("Ask me to calculate areas of squares or circles.\n")

    while True:
        user_input = input("Enter your geometry problem (or 'quit' to exit): ")

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not user_input.strip():
            continue

        try:
            # Invoke the chain
            response = chain.invoke({"input": user_input})

            # Check if the model wants to use tools
            if response.tool_calls:
                print("\nUsing tools to calculate...\n")
                # Execute the tool calls
                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']

                    # Find and execute the tool
                    for tool in tools:
                        if tool.name == tool_name:
                            result = tool.invoke(tool_args)
                            print(f"{tool_name}({tool_args}) = {result}")

                print()
            else:
                # Direct answer without tools
                print(f"\nAnswer: {response.content}\n")

        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
