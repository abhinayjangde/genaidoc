process.loadEnvFile()
async function main() {
    const response = await fetch('https://api.perplexity.ai/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${process.env.PERPLEXITY_API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'sonar-pro',
            messages: [
                {
                    role: 'user',
                    content: "hello?"
                }
            ]
        })
    });

    const data = await response.json();
    console.log(data.choices[0].message.content);
}

main();