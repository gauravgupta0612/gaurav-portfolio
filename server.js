const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const fetch = require('node-fetch');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Force HTTPS (behind Heroku/Render/any proxy) and tell browsers to always use HTTPS
app.enable('trust proxy');
app.use((req, res, next) => {
    const local = /^(localhost|127\.0\.0\.1)(:\d+)?$/.test(req.headers.host || '');
    if (!local && !req.secure) {
        return res.redirect(301, 'https://' + req.headers.host + req.originalUrl);
    }
    if (!local) {
        res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    }
    next();
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// Groq API Configuration
const GROQ_API_KEY = process.env.GROQ_API_KEY;
const GROQ_MODEL = process.env.GROQ_MODEL || 'llama-3.1-8b-instant';
const GROQ_API_URL = process.env.GROQ_API_URL || 'https://api.groq.com/openai/v1/chat/completions';

// Default fallback responses
const fallbackResponses = {
    'hello|hi|hey': 'Hey there! 👋 Welcome to my portfolio. How can I help you today?',
    'how are you|how are you doing|whats up|how you doing': '😊 I\'m doing great, thanks for asking! I\'m here to help you learn about my experience, skills, and projects. What would you like to know?',
    'thanks|thank you|thanks so much|appreciate': '🙏 You\'re welcome! Happy to help. Feel free to ask me anything about my work and experience!',
    'experience|work|job|career': '💼 I have 5+ years of experience as a Senior Software Engineer. Currently at ARCAD Software, specializing in Salesforce, Java, and modern tech.',
    'skills': '🛠️ My key skills: Salesforce Apex, Lightning, Java, TypeScript, React, GitHub, DevOps, VS Code extensions, and AI/LLM integration.',
    'salesforce': '☁️ Salesforce Trailhead All Star Ranger (213 badges, 83,875 points)! Expert in Lightning, Apex, Salesforce admin, and cloud solutions.',
    'projects': '🚀 I develop: Salesforce CRM solutions, Java plugins, VS Code extensions, and AI chatbots. Check Projects section!',
    'certifications': '🏆 Certifications: Copado, Oracle Cloud AI, IBM, GA4, and more. Check Certifications section for details!',
    'contact|email|phone': '📧 ggupta865@gmail.com | 📱 +918869999358 | 💼 linkedin.com/in/gauravgupta865',
    'team|about|who are you': '👨‍💼 I\'m Gaurav Gupta, Senior Software Engineer from Lucknow. Passionate about building innovative solutions and learning new technologies!',
    'location|lucknow': '📍 Lucknow, Uttar Pradesh 226016, India.',
    'java': '☕ Java specialist in enterprise applications, plugin development, and scalable backend solutions.',
    'typescript|react': '📘 Experienced with TypeScript/React for web apps, VS Code extensions, and responsive UIs.',
    'ai|chatbot': '🤖 Specializing in AI/LLM integration and intelligent chatbot development.',
    'help|what can you do|what can i ask': '❓ You can ask me about: experience, skills, salesforce, java, projects, certifications, contact info, location, team, or anything about my portfolio!',
    'default': 'That\'s a great question! 🤔 Try asking about: experience, skills, projects, salesforce, certifications, or contact me. Type \'help\' for more options!'
};

// Chat endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        // If Groq API key is not configured, use fallback responses
        if (!GROQ_API_KEY) {
            console.warn('⚠️ Groq API key not configured. Using fallback responses.');
            const response = getFallbackResponse(message);
            return res.json({ response });
        }

        // Call Groq API
        const groqResponse = await fetch(GROQ_API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${GROQ_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: GROQ_MODEL,
                messages: [
                    {
                        role: 'system',
                        content: `You are a friendly and professional AI assistant for Gaurav Gupta's portfolio website. You help visitors learn about his experience, skills, projects, and certifications. 

Be conversational and natural - if someone asks "How are you?" respond warmly and personally. Keep responses concise (2-3 sentences), friendly, and informative.
                        
About Gaurav Gupta:
- Senior Software Engineer with 5+ years experience at ARCAD Software
- Expertise: Salesforce (Apex, Lightning), Java, TypeScript, React, DevOps, AI/LLM
- Salesforce Trailhead All Star Ranger: 213 badges, 83,875 points
- Previous roles: Kloudrac, C&S Electric, Delhivery, Kcloud Technologies
- Location: Lucknow, Uttar Pradesh 226016, India
- Contact: ggupta865@gmail.com | +918869999358
- LinkedIn: linkedin.com/in/gauravgupta865 | GitHub: github.com/gauravgupta0612 | Trailblazer: salesforce.com/trailblazer/ggupta56

Tone: Professional yet approachable. Answer questions naturally and encourage visitors to explore the portfolio sections for more details.`
                    },
                    {
                        role: 'user',
                        content: message
                    }
                ],
                max_tokens: 200,
                temperature: 0.7
            })
        });

        if (!groqResponse.ok) {
            const error = await groqResponse.text();
            console.error('Groq API Error:', error);
            const fallback = getFallbackResponse(message);
            return res.json({ response: fallback });
        }

        const data = await groqResponse.json();
        const aiResponse = data.choices[0]?.message?.content || getFallbackResponse(message);

        res.json({ response: aiResponse });
    } catch (error) {
        console.error('Server Error:', error);
        const fallback = getFallbackResponse(req.body.message || '');
        res.json({ response: fallback });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok',
        groqConfigured: !!GROQ_API_KEY,
        model: GROQ_MODEL
    });
});

// Fallback response function
function getFallbackResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    for (const [keys, response] of Object.entries(fallbackResponses)) {
        const keywords = keys.split('|');
        for (const keyword of keywords) {
            if (lowerMessage.includes(keyword.trim())) {
                return response;
            }
        }
    }
    
    return fallbackResponses['default'];
}

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Portfolio Server running on http://localhost:${PORT}`);
    console.log(`📡 Chat API: POST http://localhost:${PORT}/api/chat`);
    console.log(`✅ Health Check: GET http://localhost:${PORT}/api/health`);
    if (GROQ_API_KEY) {
        console.log('✅ Groq API configured and ready');
    } else {
        console.log('⚠️  Groq API key not found. Using fallback responses.');
    }
});
