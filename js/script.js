// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Load theme preference
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
}

function enableDarkMode() {
    document.body.classList.add('dark-mode');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    localStorage.setItem('theme', 'dark');
}

function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', 'light');
}

themeToggle.addEventListener('click', () => {
    if (document.body.classList.contains('dark-mode')) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
});

// Mobile Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Close menu when link is clicked
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Projects Data
const projectsData = [
    {
        title: 'Salesforce CRM Solutions',
        description: 'Developed scalable and efficient Salesforce solutions focusing on Lightning Aura Components, Apex controllers, and declarative tools including validation rules and workflows to automate complex business processes.',
        tags: ['Salesforce', 'Apex', 'Lightning', 'CRM'],
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'Java Plugin Development',
        description: 'Contributed to the development of scalable and efficient solutions, focusing on Java plugin development and IBM i systems integration with advanced configuration management.',
        tags: ['Java', 'IBM i', 'Plugins'],
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'VS Code Extension Development',
        description: 'Designed and implemented user-friendly VS Code extensions using TypeScript and modern development practices to enhance developer productivity and streamline workflows.',
        tags: ['TypeScript', 'VS Code', 'React'],
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'AI-Driven Chatbot Solutions',
        description: 'Developed AI-driven chatbot solutions using large language models (LLMs) to enhance customer interactions and automate support processes for improved service delivery.',
        tags: ['AI', 'LLM', 'Chatbot', 'Python'],
        link: 'https://www.linkedin.com/in/gauravgupta865'
    }
];

// Blog Posts Data
const blogPostsData = [
    {
        title: 'Mastering Salesforce Lightning Development',
        date: 'March 1, 2026',
        excerpt: 'Learn best practices for building scalable Lightning Aura Components and Apex controllers to streamline your Salesforce development workflow.',
        readTime: '8 min read',
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'Building AI-Powered Chatbots with LLMs',
        date: 'February 25, 2026',
        excerpt: 'A comprehensive guide to developing intelligent chatbot solutions using large language models for enhanced customer interactions and automated support.',
        readTime: '10 min read',
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'VS Code Extension Development: A Complete Guide',
        date: 'February 18, 2026',
        excerpt: 'Discover how to build powerful VS Code extensions using TypeScript and React to boost developer productivity.',
        readTime: '7 min read',
        link: 'https://www.linkedin.com/in/gauravgupta865'
    },
    {
        title: 'Java Development Best Practices',
        date: 'February 10, 2026',
        excerpt: 'Explore industry best practices for Java development, plugin architecture, and integration patterns for robust applications.',
        readTime: '9 min read',
        link: 'https://www.linkedin.com/in/gauravgupta865'
    }
];

// Render Projects
function renderProjects() {
    const projectsContainer = document.getElementById('projectsContainer');

    if (projectsData.length === 0) {
        projectsContainer.innerHTML = '<div class="empty-state"><p>No projects yet. Check back soon!</p></div>';
        return;
    }

    projectsContainer.innerHTML = projectsData.map(project => `
        <div class="project-card">
            <div class="project-card-content">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="project-tags">
                    ${project.tags.map(tag => `<span class="project-tag">${tag}</span>`).join('')}
                </div>
                <a href="${project.link}" class="project-link">View Project →</a>
            </div>
        </div>
    `).join('');
}

// Render Blog Posts
function renderBlogPosts() {
    const blogContainer = document.getElementById('blogContainer');

    if (blogPostsData.length === 0) {
        blogContainer.innerHTML = '<div class="empty-state"><p>No blog posts yet. Check back soon!</p></div>';
        return;
    }

    blogContainer.innerHTML = blogPostsData.map(post => `
        <div class="blog-card">
            <div class="blog-card-meta">
                <div class="blog-card-date">${post.date}</div>
                <h3>${post.title}</h3>
                <p>${post.excerpt}</p>
            </div>
            <div class="blog-card-footer">
                <a href="${post.link}" class="blog-link">Read More →</a>
                <span class="read-time">${post.readTime}</span>
            </div>
        </div>
    `).join('');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    renderProjects();
    renderBlogPosts();

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const element = document.querySelector(href);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});

// Add fade-in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});
