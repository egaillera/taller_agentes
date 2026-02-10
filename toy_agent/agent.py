from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Load environment variables
load_dotenv()

# Define the tools
@tool
def get_square_area(side: float) -> float:
    """Usa esta herramienta para calcular el área de un cuadrado. La entrada debe ser 
    un número con el valor del lado"""
    return side ** 2

@tool
def get_circle_area(radius: float) -> float:
    """Usa esta herramienta para calcular al área de un círculo. La entrada debe ser un 
    numero con el valor del radio"""
    return 3.14159 * (radius ** 2)

# Initialize the LLM and bind tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [get_square_area, get_circle_area]
llm_with_tools = llm.bind_tools(tools)

# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en geometría. Ayuda a los usuarios a resolver problemas de geometría utilizando las herramientas disponibles."),
    ("human", "{input}"),
])

# Create the chain
chain = prompt | llm_with_tools

def main():
    print("Bienvenido al Agente de Geometría!")
    print("Puedes pedirme que calcule áreas de cuadrados o círculos.\n")

    while True:
        user_input = input("Introduce tu problema de geometría (o 'salir' para terminar): ")

        if user_input.lower() in ['quit', 'exit', 'q', 'salir']:
            print("¡Hasta luego!")
            break

        if not user_input.strip():
            continue

        try:
            # Invoke the chain
            response = chain.invoke({"input": user_input})

            # Check if the model wants to use tools
            if response.tool_calls:
                print("\nUsando herramientas para calcular...\n")

                # Execute the tool calls and collect results
                tool_messages = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']

                    # Find and execute the tool
                    for tool in tools:
                        if tool.name == tool_name:
                            result = tool.invoke(tool_args)
                            print(f"{tool_name}({tool_args}) = {result}")

                            # Create a tool message with the result
                            tool_messages.append(
                                ToolMessage(
                                    content=str(result),
                                    tool_call_id=tool_call['id']
                                )
                            )

                # Send tool results back to the model to get final answer
                messages = [
                    ("system", "Eres un experto en geometría. Ayuda a los usuarios a resolver problemas simples de geometría utilizando las herramientas disponibles."),
                    ("human", user_input),
                    response,
                ] + tool_messages
                print(tool_messages)

                final_response = llm_with_tools.invoke(messages)
                print(f"\nRespuesta: {final_response.content}\n")
            else:
                # Direct answer without tools
                print(f"\nRespuesta: {response.content}\n")

        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
