import dotenv from "dotenv"
import readline from 'readline/promises'
import { GoogleGenerativeAIEmbeddings } from '@langchain/google-genai';
import { Pinecone } from '@pinecone-database/pinecone';
import { GoogleGenAI } from "@google/genai";

dotenv.config();
const rl = readline.createInterface({ input: process.stdin, output: process.stdout })

const client = new GoogleGenAI({})
const history = []

const embeddings = new GoogleGenerativeAIEmbeddings({
    apiKey: process.env.GEMINI_API_KEY,
    model: 'text-embedding-004',
});

const pinecone = new Pinecone();
const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX_NAME);

async function queryEnhancer(question) {

    history.push({
        role: "user",
        parts: [{ text: question }]
    })

    const response = await client.models.generateContent({
        model: "gemini-2.0-flash",
        contents: history,
        config: {
            systemInstruction: `You are a query rewriting expert. Based on the provided chat history, rephrase the "Follow Up user Question" into a complete, standalone question that can be understood without the chat history.
    Only output the rewritten question and nothing else.
      `,
        },
    })

    history.pop() // removing adde user question
    return response.text
}

async function chatting(question) {

    const query = await queryEnhancer(question)

    const queryVector = await embeddings.embedQuery(query);
    const searchResults = await pineconeIndex.query({
        topK: 10,
        vector: queryVector,
        includeMetadata: true,
    });

    const context = searchResults.matches
        .map(match => match.metadata.text)
        .join("\n\n---\n\n");

    history.push({
        role: "user",
        parts: [{ text: query }]
    })

    const response = await client.models.generateContent({
        model: "gemini-2.0-flash",
        contents: history,
        config: {
            systemInstruction: `You will be given a context of relevant information and a user question.
    Your task is to answer the user's question based ONLY on the provided context.
    If the answer is not in the context, you must say "I could not find the answer in the provided document."
    Keep your answers clear, concise, and educational.
      
      Context: ${context}
      `,
        },
    })

    history.push({
        role: 'model',
        parts: [{ text: response.text }]
    })

    console.log("\n");
    return response.text
}

async function main() {
    const query = await rl.question("[chatwithpdf]> ")
    if (query == "bye") {
        rl.close();
        return;
    }
    const response = await chatting(query)
    console.log(`[chatwithpdf]> ${response}`)
    main()
}

main()
