// Meetings Scheduler Functionality

class MeetingScheduler {
    constructor() {
        this.meetings = [];
        this.init();
    }

    init() {
        this.setupTheme();
        this.loadMeetings();
        this.setupEventListeners();
        this.renderMeetings();
        this.setMinDate();
    }

    setupTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', theme);
    }

    setMinDate() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const minDate = `${year}-${month}-${day}`;
        
        const dateInput = document.getElementById('meetingDate');
        if (dateInput) {
            dateInput.min = minDate;
        }
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('meetingForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Character counter
        const topicInput = document.getElementById('meetingTopic');
        if (topicInput) {
            topicInput.addEventListener('input', (e) => {
                document.getElementById('topicCount').textContent = `${e.target.value.length}/500`;
            });
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

    handleSubmit(e) {
        e.preventDefault();

        const name = document.getElementById('meetingName').value.trim();
        const email = document.getElementById('meetingEmail').value.trim();
        const phone = document.getElementById('meetingPhone').value.trim();
        const type = document.getElementById('meetingType').value;
        const format = document.getElementById('meetingFormat').value;
        const date = document.getElementById('meetingDate').value;
        const time = document.getElementById('meetingTime').value;
        const duration = document.getElementById('meetingDuration').value;
        const topic = document.getElementById('meetingTopic').value.trim();

        // Validate all fields
        if (!name || !email || !phone || !type || !format || !date || !time || !duration || !topic) {
            alert('❌ Please fill in all required fields');
            return;
        }

        // Validate date is not in past
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            alert('❌ Please select a future date');
            return;
        }

        // Validate time is within availability
        const hour = parseInt(time.split(':')[0]);
        const day = new Date(date).getDay();
        
        if (!this.isTimeAvailable(hour, day)) {
            alert('⏰ This time is outside availability hours');
            return;
        }

        const newMeeting = {
            id: Date.now(),
            name,
            email,
            phone,
            type,
            format,
            date,
            time,
            duration,
            topic,
            timestamp: new Date().toLocaleString(),
            status: 'pending'
        };

        this.meetings.unshift(newMeeting);
        this.saveMeetings();
        this.renderMeetings();
        this.showSuccess('Meeting scheduled successfully! ✅');
        
        // Reset form
        document.getElementById('meetingForm').reset();
        document.getElementById('topicCount').textContent = '0/500';

        // Log meeting details to console (in real app, would send to server/email)
        console.log('New Meeting:', newMeeting);
    }

    isTimeAvailable(hour, day) {
        // Monday (1) - Friday (5): 10 AM - 6 PM
        if (day >= 1 && day <= 5) {
            return hour >= 10 && hour < 18;
        }
        // Saturday (6): 11 AM - 3 PM
        if (day === 6) {
            return hour >= 11 && hour < 15;
        }
        // Sunday (0): Not available
        return false;
    }

    showSuccess(message) {
        const form = document.getElementById('meetingForm');
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
            <button type="button" class="close-msg" onclick="this.parentElement.remove()">&times;</button>
        `;
        
        form.parentElement.insertBefore(successDiv, form);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (successDiv.parentElement) {
                successDiv.remove();
            }
        }, 5000);

        // Scroll to meetings list
        setTimeout(() => {
            document.querySelector('.scheduled-meetings').scrollIntoView({ behavior: 'smooth' });
        }, 300);
    }

    deleteMeeting(id) {
        if (confirm('Are you sure you want to cancel this meeting?')) {
            this.meetings = this.meetings.filter(m => m.id !== id);
            this.saveMeetings();
            this.renderMeetings();
            alert('✅ Meeting cancelled');
        }
    }

    formatDateTime(date, time) {
        const dateObj = new Date(date);
        const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
        return `${dateObj.toLocaleDateString('en-US', options)} at ${time}`;
    }

    renderMeetings() {
        const listDiv = document.getElementById('meetingsList');
        
        if (this.meetings.length === 0) {
            listDiv.innerHTML = '<p class="no-meetings"><i class="fas fa-calendar-alt"></i> No meetings scheduled yet. Book your first meeting above!</p>';
            return;
        }

        let html = '';
        this.meetings.forEach(meeting => {
            const typeEmoji = {
                'consultation': '💼',
                'mentoring': '🎓',
                'project': '📋',
                'career': '🎯',
                'networking': '🤝',
                'other': '📞'
            };

            const formatEmoji = {
                'video': '📹',
                'phone': '☎️',
                'in-person': '🏢'
            };

            const emoji = typeEmoji[meeting.type] || '📅';
            const formatEmoji2 = formatEmoji[meeting.format] || '💬';

            html += `
                <div class="meeting-item">
                    <div class="meeting-header">
                        <div>
                            <h3 class="meeting-title">${emoji} ${this.capitalizeFirst(meeting.type)}</h3>
                            <p style="margin: 0.3rem 0; color: var(--text-secondary); font-size: 0.9rem;">
                                ${this.escapeHtml(meeting.name)} • ${this.escapeHtml(meeting.email)}
                            </p>
                        </div>
                        <span class="meeting-status confirmed">SCHEDULED</span>
                    </div>
                    
                    <div class="meeting-details">
                        <div class="detail">
                            <i class="fas fa-calendar"></i>
                            <div>
                                <div class="detail-label">Date & Time</div>
                                <div class="detail-value">${this.formatDateTime(meeting.date, meeting.time)}</div>
                            </div>
                        </div>
                        
                        <div class="detail">
                            <i class="fas fa-clock"></i>
                            <div>
                                <div class="detail-label">Duration</div>
                                <div class="detail-value">${meeting.duration} mins</div>
                            </div>
                        </div>
                        
                        <div class="detail">
                            <i class="fas fa-video"></i>
                            <div>
                                <div class="detail-label">Format</div>
                                <div class="detail-value">${formatEmoji2} ${this.capitalizeFirst(meeting.format)}</div>
                            </div>
                        </div>
                        
                        <div class="detail">
                            <i class="fas fa-phone"></i>
                            <div>
                                <div class="detail-label">Contact</div>
                                <div class="detail-value">${this.escapeHtml(meeting.phone)}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="meeting-topic">
                        <strong>Topic:</strong> ${this.escapeHtml(meeting.topic)}
                    </div>
                    
                    <div class="meeting-actions">
                        <button class="btn-small btn-edit" onclick="scheduler.editMeeting(${meeting.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn-small btn-delete" onclick="scheduler.deleteMeeting(${meeting.id})">
                            <i class="fas fa-trash"></i> Cancel
                        </button>
                    </div>
                </div>
            `;
        });

        listDiv.innerHTML = html;
    }

    editMeeting(id) {
        const meeting = this.meetings.find(m => m.id === id);
        if (!meeting) return;

        // Scroll to form
        document.querySelector('.booking-card').scrollIntoView({ behavior: 'smooth' });

        // Populate form
        document.getElementById('meetingName').value = meeting.name;
        document.getElementById('meetingEmail').value = meeting.email;
        document.getElementById('meetingPhone').value = meeting.phone;
        document.getElementById('meetingType').value = meeting.type;
        document.getElementById('meetingFormat').value = meeting.format;
        document.getElementById('meetingDate').value = meeting.date;
        document.getElementById('meetingTime').value = meeting.time;
        document.getElementById('meetingDuration').value = meeting.duration;
        document.getElementById('meetingTopic').value = meeting.topic;
        document.getElementById('topicCount').textContent = `${meeting.topic.length}/500`;

        // Store ID for update
        this.editingId = id;

        // Update button text
        const button = document.querySelector('.btn-large');
        button.innerHTML = '<i class="fas fa-save"></i> Update Booking';
        button.style.background = 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)';
    }

    saveMeetings() {
        localStorage.setItem('scheduledMeetings', JSON.stringify(this.meetings));
    }

    loadMeetings() {
        const stored = localStorage.getItem('scheduledMeetings');
        this.meetings = stored ? JSON.parse(stored) : this.getDefaultMeetings();
    }

    getDefaultMeetings() {
        return [];
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

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize scheduler when DOM is ready
let scheduler;
document.addEventListener('DOMContentLoaded', () => {
    scheduler = new MeetingScheduler();
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
