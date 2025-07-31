import dotenv from "dotenv";
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';
import { GoogleGenerativeAIEmbeddings } from '@langchain/google-genai';
import { Pinecone } from '@pinecone-database/pinecone';
import { PineconeStore } from '@langchain/pinecone';
import readline from "readline/promises"

dotenv.config();

// 1. loading pdf
const pdf_path = "./nodejs.pdf";
const pdfLoader = new PDFLoader(pdf_path);
const rawDocs = await pdfLoader.load();

// 2. chunking rawDocs
const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 200,
});
const chunkedDocs = await textSplitter.splitDocuments(rawDocs);

// 3. embedding the chunked Docs
const embeddings = new GoogleGenerativeAIEmbeddings({
    apiKey: process.env.GEMINI_API_KEY,
    model: 'text-embedding-004',
});

// 4. Initialize pinecone db
const pinecone = new Pinecone();
const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX_NAME);

// 5. langchain pinecone store
await PineconeStore.fromDocuments(chunkedDocs, embeddings, {
    pineconeIndex,
    maxConcurrency: 5, // 5-5 karke vector me convert kro and store kr do
});

