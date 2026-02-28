# Gaurav Gupta's Portfolio & Blog

A modern, responsive portfolio website with AI chatbot integration powered by Groq API.

## Features

✅ **Responsive Design** - Works seamlessly on mobile, tablet, and desktop  
✅ **Dark Mode** - Theme toggle with localStorage persistence  
✅ **AI Chatbot** - Intelligent chatbot powered by Groq's Llama 3.1 model  
✅ **Glassmorphism Design** - Modern UI with glass effect styling  
✅ **Smooth Animations** - CSS keyframes and scroll-triggered effects  
✅ **Portfolio Showcase** - Display projects with tags and descriptions  
✅ **Blog Section** - Featured blog posts with read time  
✅ **Experience Timeline** - Professional work history with skills  
✅ **Certifications** - Licenses and professional credentials  
✅ **Contact Integration** - Direct email, phone, and social links  
✅ **Visitor Counter** - Track website visits  
✅ **Sticky Footer** - Always-visible footer with slide-up animation  

## Tech Stack

**Frontend:**
- HTML5
- CSS3 (with animations and responsive design)
- JavaScript (vanilla)
- Font Awesome Icons (CDN)

**Backend:**
- Node.js
- Express.js
- Groq API (for AI chatbot)
- CORS enabled

## Project Structure

```
├── index.html              # Main portfolio page
├── css/
│   └── styles.css         # All styling and animations
├── js/
│   └── script.js          # Frontend logic and chatbot
├── media/
│   ├── image (1).png      # Profile photo
│   └── gg-logo.svg        # Animated GG logo
├── server.js              # Express backend server
├── package.json           # Node.js dependencies
├── .env                   # Environment variables (secrets)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Groq API Key (optional - fallback responses work without it)

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Configure Environment Variables
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
PORT=3000
NODE_ENV=development
```

### Step 3: Start the Server
```bash
npm start
```

The server will start on `http://localhost:3000`

### Step 4: Open in Browser
Visit `http://localhost:3000` in your web browser

## How the AI Chatbot Works

1. **Frontend** (js/script.js)
   - User types a message in the chatbot
   - Message is sent to `/api/chat` endpoint
   - Response is displayed in the chatbot widget

2. **Backend** (server.js)
   - Receives message from frontend
   - Calls Groq API securely (API key stays on server)
   - Returns intelligent AI response
   - Falls back to keyword-based responses if Groq isn't available

3. **Security**
   - API key is stored in `.env` (never committed to Git)
   - `.gitignore` prevents `.env` from being pushed
   - Frontend never exposes sensitive credentials
   - All API calls go through secure backend proxy

## Groq API Setup

### Getting a Groq API Key
1. Visit https://console.groq.com
2. Sign up for a free account
3. Go to API keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Model Information
- **Model**: `llama-3.1-8b-instant`
- **Max Tokens**: 200 (for quick responses)
- **Temperature**: 0.7 (balanced creativity)

## Customization

### Change Chatbot Responses
Edit `js/script.js` in the `botResponses` object to customize fallback responses for keyword matching.

### Update Portfolio Content
- Edit `index.html` to change text content
- Update `projectsData` array in `js/script.js` for projects
- Update `blogPostsData` array in `js/script.js` for blog posts

### Modify Styling
- Edit `css/styles.css` for colors, fonts, and layouts
- CSS variables at the top allow easy theme customization

## Deployment

### GitHub Pages (Static Frontend)
1. Push code to GitHub repository
2. Enable GitHub Pages in repository settings
3. Choose main branch as source
4. Add custom domain (optional)

### Backend Hosting Options
- **Heroku** - Free tier available
- **Railway.app** - Simple deployment
- **Render** - Free tier with good performance
- **Fly.io** - Distributed hosting

**Note**: GitHub Pages only hosts static files. Use one of the above services to host the Node.js backend.

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| GROQ_API_KEY | Your Groq API key | gsk_xxxxxxx... |
| GROQ_MODEL | AI model to use | llama-3.1-8b-instant |
| GROQ_API_URL | Groq API endpoint | https://api.groq.com/... |
| PORT | Server port | 3000 |
| NODE_ENV | Environment | development / production |

## Troubleshooting

### Chatbot not responding
- Check if server is running (`npm start`)
- Check browser console for errors
- Verify `.env` file has correct API key
- Try fallback responses (keyword-based)

### Styling not loading
- Clear browser cache (Ctrl+Shift+Delete)
- Check if `css/styles.css` path is correct
- Verify CSS is linked in `index.html`

### Images not loading
- Check `media/` folder exists
- Verify image file names match in HTML
- Ensure correct file paths in `index.html`

## Contact & Links

- **Email**: ggupta865@gmail.com
- **Phone**: +918869999358
- **LinkedIn**: https://www.linkedin.com/in/gauravgupta865
- **GitHub**: https://github.com/gauravgupta0612
- **Salesforce Trailblazer**: https://www.salesforce.com/trailblazer/ggupta56

## License

MIT License - Feel free to use this portfolio as a template!

## Support

For issues or questions, feel free to reach out via email or LinkedIn.

---

**Built with ❤️ by Gaurav Gupta**  
Last Updated: March 1, 2026

   python -m SimpleHTTPServer 8000
   
   # Using Node.js (with http-server)
   npx http-server
   ```

## Customization

### Update Your Information

Edit `index.html` to customize:
- Your name and title in the hero section
- About section content
- Contact links (email, LinkedIn, GitHub, Twitter, etc.)

### Update Project Data

Edit the `projectsData` array in `js/script.js`:
```javascript
const projectsData = [
    {
        title: 'Your Project Title',
        description: 'Your project description',
        tags: ['Tag1', 'Tag2'],
        link: 'https://your-project-link.com'
    }
    // Add more projects
];
```

### Update Blog Posts

Edit the `blogPostsData` array in `js/script.js`:
```javascript
const blogPostsData = [
    {
        title: 'Your Blog Title',
        date: 'Month Day, Year',
        excerpt: 'Brief excerpt of your blog post',
        readTime: 'X min read',
        link: 'https://your-blog-link.com'
    }
    // Add more blog posts
];
```

### Customize Styling

Edit `css/styles.css` to change:
- Color scheme (update CSS variables in `:root`)
- Fonts and typography
- Spacing and layout
- Animations and transitions

## Deployment to GitHub Pages

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and log in
2. Click "New Repository"
3. Name it: `gaurav-gupta.co.in` (optional, you can use any name)
4. Keep it public
5. Click "Create repository"

### Step 2: Push Your Code

```bash
# Initialize git in your project (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: Portfolio and blog website"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Configure GitHub Pages

1. Go to your repository settings
2. Scroll down to "Pages"
3. Under "Source", select `main` branch
4. Click "Save"
5. Your site will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

### Step 4: Link Your Custom Domain

1. In GitHub repository settings, scroll to "Pages"
2. Under "Custom domain", enter your domain: `gaurav-gupta.co.in`
3. Go to your domain registrar (where you purchased the domain)
4. Update DNS settings to point to GitHub Pages:
   - **Type A Records** should point to these IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or use **CNAME record** pointing to: `YOUR_USERNAME.github.io`

5. Wait 24 hours for DNS propagation
6. GitHub Pages will automatically issue an SSL certificate for your domain

### Step 5: Enable HTTPS

In GitHub repository settings under "Pages":
- Check "Enforce HTTPS" (once domain is verified)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Performance Optimization

- Minified CSS and JavaScript
- Lazy loading for images
- Optimized animations
- No external dependencies (except Font Awesome icons)

## SEO Optimization

The website includes:
- Semantic HTML structure
- Meta viewport tag for responsiveness
- Page title for browser tab
- Proper heading hierarchy

### To improve SEO further:

Add meta tags to `<head>` in `index.html`:
```html
<meta name="description" content="Your site description">
<meta name="keywords" content="your, keywords, here">
<meta property="og:title" content="Gaurav Gupta - Portfolio">
<meta property="og:description" content="Your site description">
<meta property="og:image" content="path/to/image.png">
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the existing documentation
2. Review the code comments
3. Consult VS Code built-in help

## Next Steps

1. **Customize content** - Edit HTML and JavaScript with your information
2. **Add projects** - Update the projects array with your work
3. **Add blog posts** - Populate the blog section with your content
4. **Update styling** - Modify CSS to match your personal brand
5. **Deploy** - Push to GitHub and enable GitHub Pages
6. **Add custom domain** - Point your purchased domain to the site

Happy building! 🚀
