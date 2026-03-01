// Community Q&A Functionality

class CommunityForum {
    constructor() {
        this.questions = [];
        this.currentSort = 'newest';
        this.selectedQuestionId = null;
        this.init();
    }

    init() {
        this.setupTheme();
        this.loadData();
        this.setupEventListeners();
        this.renderQuestions();
        this.updateStats();
    }

    setupTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', theme);
    }

    setupEventListeners() {
        // Ask question form
        const askForm = document.getElementById('askQuestionForm');
        if (askForm) {
            askForm.addEventListener('submit', (e) => this.handleAskQuestion(e));
        }

        // Character counters
        const titleInput = document.getElementById('questionTitle');
        if (titleInput) {
            titleInput.addEventListener('input', (e) => {
                document.getElementById('titleCount').textContent = `${e.target.value.length}/200`;
            });
        }

        const descInput = document.getElementById('questionDescription');
        if (descInput) {
            descInput.addEventListener('input', (e) => {
                document.getElementById('descCount').textContent = `${e.target.value.length}/1000`;
            });
        }

        const replyInput = document.getElementById('replyText');
        if (replyInput) {
            replyInput.addEventListener('input', (e) => {
                document.getElementById('replyCount').textContent = `${e.target.value.length}/500`;
            });
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentSort = e.target.dataset.sort;
                this.renderQuestions();
            });
        });

        // Modal close
        const modalClose = document.getElementById('modalClose');
        const modal = document.getElementById('questionModal');
        if (modalClose && modal) {
            modalClose.addEventListener('click', () => {
                modal.style.display = 'none';
                this.selectedQuestionId = null;
            });

            // Close on outside click
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                    this.selectedQuestionId = null;
                }
            });
        }

        // Reply form
        const replyForm = document.getElementById('replyForm');
        if (replyForm) {
            replyForm.addEventListener('submit', (e) => this.handleReply(e));
        }

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Hamburger menu
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.querySelector('.nav-menu');
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
            });

            navMenu.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    hamburger.classList.remove('active');
                });
            });
        }
    }

    handleAskQuestion(e) {
        e.preventDefault();

        const title = document.getElementById('questionTitle').value.trim();
        const description = document.getElementById('questionDescription').value.trim();
        const name = document.getElementById('questionName').value.trim();
        const email = document.getElementById('questionEmail').value.trim();

        if (!title || !name) {
            alert('Please fill in all required fields');
            return;
        }

        const newQuestion = {
            id: Date.now(),
            title,
            description,
            author: name,
            email,
            timestamp: new Date().toLocaleString(),
            replies: []
        };

        this.questions.unshift(newQuestion);
        this.saveData();
        this.updateStats();
        this.renderQuestions();

        // Reset form
        document.getElementById('askQuestionForm').reset();
        document.getElementById('titleCount').textContent = '0/200';
        document.getElementById('descCount').textContent = '0/1000';

        // Show success message
        alert('✅ Question posted successfully!');
    }

    handleReply(e) {
        e.preventDefault();

        const replyText = document.getElementById('replyText').value.trim();
        const replyName = document.getElementById('replyName').value.trim();

        if (!replyText || !replyName) {
            alert('Please fill in all required fields');
            return;
        }

        const question = this.questions.find(q => q.id == this.selectedQuestionId);
        if (!question) return;

        const newReply = {
            id: Date.now(),
            text: replyText,
            author: replyName,
            timestamp: new Date().toLocaleString()
        };

        question.replies.push(newReply);
        this.saveData();
        this.updateStats();
        this.showQuestionDetail(this.selectedQuestionId);

        // Reset form
        document.getElementById('replyForm').reset();
        document.getElementById('replyCount').textContent = '0/500';

        alert('✅ Answer posted successfully!');
    }

    openQuestion(questionId) {
        this.selectedQuestionId = questionId;
        this.showQuestionDetail(questionId);
        document.getElementById('questionModal').style.display = 'flex';
    }

    showQuestionDetail(questionId) {
        const question = this.questions.find(q => q.id == questionId);
        if (!question) return;

        const detailDiv = document.getElementById('questionDetail');
        const repliesDiv = document.getElementById('repliesSection');
        const replyForm = document.getElementById('replyForm');

        // Question detail
        detailDiv.innerHTML = `
            <h2 class="detail-title">${this.escapeHtml(question.title)}</h2>
            <div class="detail-meta">
                <span><strong>Asked by:</strong> ${this.escapeHtml(question.author)}</span>
                <span><strong>Date:</strong> ${question.timestamp}</span>
            </div>
            ${question.description ? `<p class="detail-description">${this.escapeHtml(question.description)}</p>` : ''}
        `;

        // Replies
        let repliesHTML = `
            <div class="replies-header">
                <i class="fas fa-comments"></i> Answers (${question.replies.length})
            </div>
        `;

        if (question.replies.length > 0) {
            repliesHTML += '<div class="replies-list">';
            question.replies.forEach(reply => {
                repliesHTML += `
                    <div class="reply-card">
                        <div class="reply-header">
                            <span class="reply-author">✓ ${this.escapeHtml(reply.author)}</span>
                            <span class="reply-time">${reply.timestamp}</span>
                        </div>
                        <p class="reply-text">${this.escapeHtml(reply.text)}</p>
                    </div>
                `;
            });
            repliesHTML += '</div>';
        } else {
            repliesHTML += '<div class="no-replies">No answers yet. Be the first to answer!</div>';
        }

        repliesDiv.innerHTML = repliesHTML;
        replyForm.style.display = 'block';
        replyForm.reset();
        document.getElementById('replyCount').textContent = '0/500';
    }

    getSortedQuestions() {
        const sorted = [...this.questions];

        if (this.currentSort === 'newest') {
            return sorted;
        } else if (this.currentSort === 'popular') {
            return sorted.sort((a, b) => b.replies.length - a.replies.length);
        } else if (this.currentSort === 'unanswered') {
            return sorted.filter(q => q.replies.length === 0);
        }

        return sorted;
    }

    renderQuestions() {
        const listDiv = document.getElementById('questionsList');
        const sorted = this.getSortedQuestions();

        if (sorted.length === 0) {
            listDiv.innerHTML = `
                <div class="no-questions">
                    <i class="fas fa-inbox"></i>
                    <p>No questions yet. Be the first to ask!</p>
                </div>
            `;
            return;
        }

        let html = '';
        sorted.forEach(question => {
            const hasAnswers = question.replies.length > 0;
            const badge = hasAnswers 
                ? `<span class="badge answered"><i class="fas fa-check-circle"></i> ${question.replies.length} Answer${question.replies.length !== 1 ? 's' : ''}</span>`
                : '<span class="badge unanswered"><i class="fas fa-circle"></i> No Answers</span>';

            html += `
                <div class="question-card" onclick="forum.openQuestion(${question.id})">
                    <div class="question-header">
                        <div>
                            <h3 class="question-title">${this.escapeHtml(question.title)}</h3>
                        </div>
                        <div class="question-meta">
                            <div class="question-author">👤 ${this.escapeHtml(question.author)}</div>
                            <div>${question.timestamp}</div>
                        </div>
                    </div>
                    ${question.description ? `<p class="question-description">${this.escapeHtml(question.description)}</p>` : ''}
                    <div class="question-stats">
                        <div class="stat">
                            <i class="fas fa-comment-dots"></i>
                            <span class="stat-count">${question.replies.length}</span>
                            <span>Answer${question.replies.length !== 1 ? 's' : ''}</span>
                        </div>
                    </div>
                    <div>${badge}</div>
                </div>
            `;
        });

        listDiv.innerHTML = html;
    }

    updateStats() {
        let totalQuestions = this.questions.length;
        let totalAnswers = 0;
        let uniqueAuthors = new Set();

        this.questions.forEach(q => {
            uniqueAuthors.add(q.author);
            totalAnswers += q.replies.length;
            q.replies.forEach(r => {
                uniqueAuthors.add(r.author);
            });
        });

        document.getElementById('totalQuestions').textContent = totalQuestions;
        document.getElementById('totalAnswers').textContent = totalAnswers;
        document.getElementById('totalUsers').textContent = uniqueAuthors.size;
    }

    saveData() {
        localStorage.setItem('communityQuestions', JSON.stringify(this.questions));
    }

    loadData() {
        const stored = localStorage.getItem('communityQuestions');
        this.questions = stored ? JSON.parse(stored) : this.getDefaultQuestions();
    }

    getDefaultQuestions() {
        return [
            {
                id: 1,
                title: "How do I get started with Salesforce development?",
                description: "I'm new to Salesforce and want to learn Apex and Lightning Components. What's the best learning path?",
                author: "Alex Kumar",
                email: "",
                timestamp: new Date(Date.now() - 2 * 86400000).toLocaleString(),
                replies: [
                    {
                        id: 101,
                        text: "Start with Salesforce Trailhead! It's completely free and has comprehensive modules on Apex, Lightning, and more. Gaurav here has 213 badges, so you know it's effective!",
                        author: "Gaurav Gupta",
                        timestamp: new Date(Date.now() - 48 * 3600000).toLocaleString()
                    },
                    {
                        id: 102,
                        text: "I'd also recommend joining the Salesforce community forums and attending local user groups.",
                        author: "Sarah Mitchell",
                        timestamp: new Date(Date.now() - 24 * 3600000).toLocaleString()
                    }
                ]
            },
            {
                id: 2,
                title: "What's the best practice for error handling in Apex?",
                description: "I keep getting errors in production. How should I properly handle exceptions in Apex to make the code more robust?",
                author: "Developer Dave",
                email: "",
                timestamp: new Date(Date.now() - 86400000).toLocaleString(),
                replies: [
                    {
                        id: 103,
                        text: "Use try-catch blocks for predictable errors and custom exceptions for business logic. Always log errors for debugging!",
                        author: "John Chen",
                        timestamp: new Date(Date.now() - 23 * 3600000).toLocaleString()
                    }
                ]
            },
            {
                id: 3,
                title: "How to optimize SOQL queries for large datasets?",
                description: "My batch job is timing out when processing 100k+ records. How can I optimize queries?",
                author: "Performance Pete",
                email: "",
                timestamp: new Date(Date.now() - 3600000).toLocaleString(),
                replies: []
            }
        ];
    }

    toggleTheme() {
        const current = localStorage.getItem('theme') || 'light';
        const newTheme = current === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);

        // Update icon
        const icon = document.getElementById('themeToggle').querySelector('i');
        if (icon) {
            icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize forum when DOM is ready
let forum;
document.addEventListener('DOMContentLoaded', () => {
    forum = new CommunityForum();

    // Update visitor count
    updateVisitorCount();
});

function updateVisitorCount() {
    let visitors = localStorage.getItem('visitors') || 0;
    visitors = parseInt(visitors) + 1;
    localStorage.setItem('visitors', visitors);
    const count = document.getElementById('visitorCount');
    if (count) {
        count.innerHTML = `<strong>${visitors}</strong> visitors`;
    }
}
