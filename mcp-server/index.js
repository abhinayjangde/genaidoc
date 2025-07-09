import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js'
import {z} from "zod"
import axios from "axios";

const server = new McpServer({
    name: "customTools",
    version: "1.0.0"
})

server.tool("add", {
    title: "Addition Tool",
    inputSchema: {a: z.number(),b: z.number()}
}, async function({a,b}){
    const sum = a + b;
    return ({
        content: [{type: "text", text: String(sum)}]
    })
})
server.tool("weather", {
    title: "gives weather info",
    inputSchema: {city: z.string()}
}, async function({city}){
    let response = await axios.get(`https://wttr.in/${city}?format=%C+%t`)
   
    return ({
        content: [{type: "text", text: JSON.stringify(response.data)}]
    })
})

const transport = new StdioServerTransport();
await server.connect(transport);