const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { OpenAI } = require('openai');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Initialize OpenAI
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

// Portfolio data API
app.get('/api/projects', (req, res) => {
    res.json(portfolioData.projects);
});

app.get('/api/skills', (req, res) => {
    res.json(portfolioData.skills);
});

app.get('/api/storage/:type', (req, res) => {
    const { type } = req.params;
    res.json(portfolioData.storage[type] || []);
});

// AI Chat API
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    
    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [
                {
                    role: "system",
                    content: "You are Emma Wilson's AI assistant. Help users learn about Emma's portfolio, projects, skills, and experience."
                },
                {
                    role: "user",
                    content: message
                }
            ]
        });
        
        res.json({ response: completion.choices[0].message.content });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Contact form submission
app.post('/api/contact', async (req, res) => {
    const { name, email, message } = req.body;
    
    // Add email sending logic here (Nodemailer, SendGrid, etc.)
    console.log(`Contact from ${name} (${email}): ${message}`);
    
    res.json({ success: true, message: "Message sent successfully!" });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});