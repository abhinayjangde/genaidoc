import OpenAI from "openai";
import { stdin, stdout } from "process";
import readline from "readline/promises";
import { getAllUsers } from "./tools/tools.js";


const openai = new OpenAI({
    apiKey: process.env.GEMINI_API_KEY,
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});


const rl = readline.createInterface({ input: stdin, output: stdout })

async function main() {

    const availableTools = {
        getAllUsers: getAllUsers
    }

    const system_prompt = `
        You are an helpful assistant. who has access of all my tools and help me to query on my database.

        Available Tools:

        - getAllusers : It is used get all users from database, takes table name as parameters and return all users 
    `

    let messages = [
        { role: "system", content: system_prompt },
    ]

    const tools = [
        {
            "type": "function",
            "function": {
                "name": "getAllUsers",
                "description": "It is used get all users from database, takes table name as parameters and return all users",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "Takes table name. e.g. users"
                        }
                    }
                }
            }
        }
    ];

    while (true) {

        const query = await rl.question("> ")

        if (query === "bye") {
            console.log("# bye!")
            break
        }
        messages.push({ "role": "user", "content": query })

        while (true) {

            try {
                const response = await openai.chat.completions.create({
                    model: "gemini-2.0-flash",
                    messages: messages,
                    tools: tools
                });


                const toolsToCall = response.choices[0].message.tool_calls;

                messages.push(response.choices[0].message)

                if (!toolsToCall) {
                    console.log(`# ${response.choices[0].message.content}`)
                    break;
                }


                for (const tool of toolsToCall) {
                    const funName = tool.function.name;
                    const funArgs = tool.function.arguments

                    let result = ""
                    if (availableTools[funName]) {
                        result = await availableTools[funName](JSON.parse(funArgs))
                    }
                    messages.push({
                        role: "tool",
                        content: result,
                        tool_call_id: tool.id
                    })
                }

            } catch (error) {
                console.error("ERROR :", error.message)
            }
        }

    }
    rl.close();

}

main()