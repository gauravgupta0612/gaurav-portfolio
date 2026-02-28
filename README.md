# Portfolio & Blog Website

A modern, responsive portfolio and blog website built with HTML, CSS, and JavaScript. This website is designed to be deployed for free on GitHub Pages.

## Features

- ✅ **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- ✅ **Dark Mode** - Toggle between light and dark themes with theme persistence
- ✅ **Portfolio Section** - Showcase your projects with descriptions and tags
- ✅ **Blog Section** - Display your latest blog posts
- ✅ **Contact Section** - Links to your social profiles and contact information
- ✅ **Smooth Animations** - Interactive animations and transitions
- ✅ **Accessibility** - Semantic HTML and ARIA labels
- ✅ **Modern Design** - Clean, professional, and eye-catching UI

## Project Structure

```
.
├── index.html           # Main HTML file
├── css/
│   └── styles.css       # Main stylesheet with dark mode support
├── js/
│   └── script.js        # JavaScript for interactivity
├── README.md            # Project documentation
└── .github/
    └── copilot-instructions.md  # Copilot configuration
```

## Getting Started

### Prerequisites

- A modern web browser
- Git (for deployment to GitHub Pages)
- A GitHub account

### Local Development

1. Open the project folder in VS Code
2. Use Live Server extension (recommended):
   - Install the "Live Server" extension from VS Code marketplace
   - Right-click on `index.html` and select "Open with Live Server"
   - The website will open at `http://localhost:5500`

3. Or use any other local server:
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Using Python 2
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
