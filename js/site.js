// Classical site — navigation + chatbot
(function () {
  const toggle = document.querySelector('.nav-toggle');
  const list = document.querySelector('.nav ul');
  if (toggle && list) {
    toggle.addEventListener('click', () => list.classList.toggle('open'));
    list.querySelectorAll('a').forEach(a => a.addEventListener('click', () => list.classList.remove('open')));
  }
})();

if (document.getElementById('chatbotToggle')) {
// AI Chatbot Functionality
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotWidget = document.getElementById('chatbotWidget');
const closeChatbot = document.getElementById('closeChatbot');
const sendMessage = document.getElementById('sendMessage');
const userInput = document.getElementById('userInput');
const chatbotMessages = document.getElementById('chatbotMessages');

// Chatbot responses - Enhanced with better keyword matching
const botResponses = {
    'hello|hi|hey': 'Hey there! 👋 Welcome to my portfolio. How can I help you today?',
    'how are you|how are you doing|whats up|how you doing': '😊 I\'m doing great, thanks for asking! I\'m here to help you learn about my experience, skills, and projects. What would you like to know?',
    'thanks|thank you|thanks so much|appreciate': '🙏 You\'re welcome! Happy to help. Feel free to ask me anything about my work and experience!',
    'experience|work|job|career': '💼 I have 6+ years of experience. I am a Senior Software Engineer at ARCAD Software, building IBM i developer tools (RDi Eclipse plug-ins, VS Code extensions), Java and AI integrations, after several years on Salesforce.',
    'skills|ibm|rpg|as400|rdi': '🛠️ Key skills: IBM i (RPGLE, CL, DDS, Db2 for i SQL, IFS, PASE), IBM RDi 9.8/9.9, z/OS (JCL, z/OSMF), Java & Eclipse/OSGi plug-ins, TypeScript, VS Code extensions, AI/LLM & MCP, and Salesforce Apex/Lightning. RDi 9.9 fix list: /rdi-9-9.html',
    'salesforce': '☁️ Salesforce Trailhead All Star Ranger (213 badges, 83,875 points)! Expert in Lightning, Apex, Salesforce admin, and cloud solutions.',
    'projects|vanthrex|tavrion|routinel|devsuite|jarpilot|devflow|devpilot': '🚀 Recent projects: Vanthrex for IBM i (VS Code), Tavrion Studio (Eclipse-ready IDE, Windows .exe), AI-Native Developer Platform, IBM i & z/OS Explorer, Routinel, DevSuite, JarPilot, Salesforce DevPilot Pack and DevFlow. See the Projects section, the Journal, or Downloads for every release.',
    'certifications': '🏆 Certifications: Copado, Oracle Cloud AI, IBM, GA4, and more. Check Certifications section for details!',
    'contact|email|phone': '📧 ggupta865@gmail.com | 📱 +918869999358 | 💼 linkedin.com/in/gauravgupta865',
    'team|about|who are you': '👨‍💼 I\'m Gaurav Gupta, Senior Software Engineer with 6+ years of experience, from Lucknow. Passionate about building innovative solutions and learning new technologies!',
    'location|lucknow': '📍 Lucknow, Uttar Pradesh 226016, India.',
    'java': '☕ Java specialist in enterprise applications, plugin development, and scalable backend solutions.',
    'typescript|react': '📘 Experienced with TypeScript/React for web apps, VS Code extensions, and responsive UIs.',
    'ai|chatbot': '🤖 Specializing in AI/LLM integration and intelligent chatbot development.',
    'download|release|exe|vsix|install': '⬇️ Every release (Windows .exe installers and .vsix files) is listed on the Downloads page: /downloads.html',
    'help|what can you do|what can i ask': '❓ You can ask me about: experience, skills, salesforce, java, projects, certifications, contact info, location, team, or anything about my portfolio!',
    'default': 'That\'s a great question! 🤔 Try asking about: experience, skills, projects, salesforce, certifications, or contact me. Type \'help\' for more options!'
};

// Toggle chatbot open/close
chatbotToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    chatbotWidget.classList.toggle('active');
    if (chatbotWidget.classList.contains('active')) {
        userInput.focus();
    }
});

closeChatbot.addEventListener('click', (e) => {
    e.stopPropagation();
    chatbotWidget.classList.remove('active');
});

// Close chatbot when clicking outside
document.addEventListener('click', (e) => {
    if (!chatbotWidget.contains(e.target) && !chatbotToggle.contains(e.target)) {
        chatbotWidget.classList.remove('active');
    }
});

// Send message
function sendUserMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user-message';
    userMessageDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;
    chatbotMessages.appendChild(userMessageDiv);

    // Clear input
    userInput.value = '';

    // Scroll to bottom
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = `<p>💭 Thinking...</p>`;
    chatbotMessages.appendChild(typingDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Get bot response from Groq API via backend
    setTimeout(() => {
        getGroqResponse(message).then(botResponse => {
            // Remove typing indicator
            typingDiv.remove();
            
            // Display bot response
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message bot-message';
            botMessageDiv.innerHTML = `<p>${escapeHtml(botResponse)}</p>`;
            chatbotMessages.appendChild(botMessageDiv);
            
            // Scroll to bottom
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        });
    }, 300);
}

// AI Integration - Calls secure backend proxy
async function getGroqResponse(userMessage) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error('Chat API error');
        }

        const data = await response.json();
        return data.response || getBotResponse(userMessage.toLowerCase());
    } catch (error) {
        console.error('Chat Error:', error);
        // Fallback to local responses if API fails
        return getBotResponse(userMessage.toLowerCase());
    }
}

// Get appropriate bot response with smart keyword matching
function getBotResponse(message) {
    for (const [key, response] of Object.entries(botResponses)) {
        // Handle pipe-separated keywords
        const keywords = key.split('|');
        for (const keyword of keywords) {
            if (message.includes(keyword.trim())) {
                return response;
            }
        }
    }
    return botResponses['default'];
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Send message on button click
sendMessage.addEventListener('click', sendUserMessage);

// Send message on Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendUserMessage();
    }
});

}
