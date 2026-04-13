from google.genai import types


def think(thought):
    return thought


schema_think = types.FunctionDeclaration(
    name="think",
    description="Use this tool to think through the problem before acting. Write out your reasoning, plan and any concerns before using other tools",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "thought": types.Schema(
                type=types.Type.STRING,
                description="your reasoning plan and observations",
            ),
        },
        required=["thought"]
    )
)
