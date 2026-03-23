// Portfolio Data
const portfolioData = {
    projects: [
        {
            id: 1,
            name: "SmartTask App",
            description: "A intelligent task management application with AI-powered prioritization, real-time collaboration, and advanced analytics. Built with Flask and Python, featuring automated task scheduling and productivity insights.",
            tech: ["Flask", "Python", "PostgreSQL", "Redis", "Celery"],
            github: "https://github.com/emmawilson/smarttask",
            demo: "https://smarttask-demo.vercel.app",
            stars: 127,
            forks: 34,
            commits: 245
        },
        {
            id: 2,
            name: "Recipe Finder",
            description: "An intelligent recipe discovery platform that suggests recipes based on ingredients, dietary preferences, and cooking time. Features include AI-powered recommendations, nutrition analysis, and meal planning.",
            tech: ["React", "Node.js", "Express", "MongoDB", "OpenAI API"],
            github: "https://github.com/emmawilson/recipe-finder",
            demo: "https://recipe-finder.vercel.app",
            stars: 89,
            forks: 23,
            commits: 178
        },
        {
            id: 3,
            name: "E-Commerce Platform",
            description: "A full-featured e-commerce solution with product management, shopping cart, payment integration, and order tracking. Built with Django and PostgreSQL for scalability and security.",
            tech: ["Django", "Python", "PostgreSQL", "Redis", "Stripe API"],
            github: "https://github.com/emmawilson/ecommerce-platform",
            demo: "https://ecommerce-demo.herokuapp.com",
            stars: 234,
            forks: 67,
            commits: 456
        }
    ],
    skills: [
        { name: "Python", percentage: 95, projects: 12, experience: "5 years" },
        { name: "JavaScript/TypeScript", percentage: 90, projects: 15, experience: "4 years" },
        { name: "React", percentage: 88, projects: 8, experience: "3 years" },
        { name: "Node.js", percentage: 85, projects: 6, experience: "3 years" },
        { name: "Django", percentage: 92, projects: 5, experience: "4 years" },
        { name: "Flask", percentage: 87, projects: 4, experience: "3 years" },
        { name: "AWS/Azure", percentage: 78, projects: 3, experience: "2 years" },
        { name: "Docker/Kubernetes", percentage: 82, projects: 4, experience: "2 years" }
    ],
    storage: {
        google: [
            { name: "Portfolio Assets", type: "folder", items: 12, size: "245 MB", modified: "2024-01-15" },
            { name: "Certificates", type: "folder", items: 4, size: "12 MB", modified: "2024-01-10" },
            { name: "Source Code", type: "folder", items: 5, size: "89 MB", modified: "2024-01-20" },
            { name: "Resume.pdf", type: "file", size: "2.4 MB", modified: "2024-01-05" },
            { name: "Project Documentation", type: "folder", items: 8, size: "156 MB", modified: "2024-01-18" }
        ],
        github: [
            { name: "smarttask-app", type: "repo", stars: 127, language: "Python", updated: "2 days ago" },
            { name: "recipe-finder", type: "repo", stars: 89, language: "JavaScript", updated: "5 days ago" },
            { name: "ecommerce-platform", type: "repo", stars: 234, language: "Python", updated: "1 week ago" },
            { name: "portfolio-website", type: "repo", stars: 45, language: "JavaScript", updated: "3 days ago" }
        ],
        aws: [
            { name: "project-assets-bucket", type: "bucket", size: "1.2 GB", objects: 345, region: "us-east-1" },
            { name: "static-website-host", type: "bucket", size: "456 MB", objects: 89, region: "us-east-1" },
            { name: "backup-storage", type: "bucket", size: "2.3 GB", objects: 567, region: "us-west-2" }
        ]
    }
};

// AI Assistant Responses
const aiResponses = {
    projects: "Emma has 3 main projects: SmartTask App (task management with AI), Recipe Finder (recipe discovery platform), and E-Commerce Platform (full-featured online store). All projects are open-source and available on GitHub!",
    skills: "Emma specializes in full-stack development with expertise in Python (95%), JavaScript/TypeScript (90%), React (88%), Node.js (85%), Django (92%), Flask (87%), and cloud technologies like AWS and Azure. She has 5+ years of experience in software development.",
    resume: "You can download Emma's resume by clicking the 'Download Resume' button at the top of the page. It contains her complete work history, education, and project details.",
    contact: "You can contact Emma through the 'Contact Me' button at the top of the page, or email her directly at emma.wilson@example.com. She typically responds within 24 hours.",
    github: "Emma's GitHub profile is at github.com/emmawilson. She has 15+ repositories, 500+ total stars, and actively contributes to open-source projects.",
    experience: "Emma has 5+ years of full-stack development experience, working with companies ranging from startups to enterprises. She specializes in building scalable web applications and leading development teams.",
    education: "Emma holds a Master's degree in Computer Science from Stanford University and a Bachelor's in Software Engineering from MIT."
};

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    loadSkills();
    loadStorage('google');
    loadGitHubActivity();
    loadHeatmap();
    setupEventListeners();
    
    // Hide loading overlay
    setTimeout(() => {
        document.getElementById('loading-overlay').style.opacity = '0';
        setTimeout(() => {
            document.getElementById('loading-overlay').style.display = 'none';
        }, 500);
    }, 1000);
});

// Load Projects
function loadProjects() {
    const projectsGrid = document.getElementById('projects-grid');
    projectsGrid.innerHTML = portfolioData.projects.map(project => `
        <div class="project-card" onclick="showProjectDetails(${project.id})">
            <div class="project-header">
                <h3>${project.name}</h3>
                <div class="project-tech">
                    ${project.tech.slice(0, 3).map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    ${project.tech.length > 3 ? `<span class="tech-tag">+${project.tech.length - 3}</span>` : ''}
                </div>
            </div>
            <div class="project-body">
                <p>${project.description.substring(0, 120)}...</p>
                <div class="project-stats">
                    <span><i class="fas fa-star"></i> ${project.stars}</span>
                    <span><i class="fas fa-code-branch"></i> ${project.forks}</span>
                    <span><i class="fas fa-code-commit"></i> ${project.commits}</span>
                </div>
            </div>
            <div class="project-footer">
                <a href="${project.github}" target="_blank" class="project-link"><i class="fab fa-github"></i> Code</a>
                <a href="${project.demo}" target="_blank" class="project-link"><i class="fas fa-external-link-alt"></i> Demo</a>
            </div>
        </div>
    `).join('');
}

// Load Skills with Visualizations
function loadSkills() {
    const skillsContainer = document.getElementById('skills-container');
    skillsContainer.innerHTML = portfolioData.skills.map(skill => `
        <div class="skill-item">
            <div class="skill-info">
                <span class="skill-name">${skill.name}</span>
                <span class="skill-percentage">${skill.percentage}%</span>
            </div>
            <div class="skill-bar">
                <div class="skill-progress" style="width: 0%" data-width="${skill.percentage}"></div>
            </div>
            <div style="margin-top: 10px; font-size: 0.85rem; color: var(--text-secondary);">
                <span>📁 ${skill.projects} projects</span>
                <span style="margin-left: 15px;">⏱️ ${skill.experience}</span>
            </div>
        </div>
    `).join('');
    
    // Animate skill bars
    setTimeout(() => {
        document.querySelectorAll('.skill-progress').forEach(bar => {
            const width = bar.getAttribute('data-width');
            bar.style.width = `${width}%`;
        });
    }, 500);
}

// Load Storage Content
function loadStorage(storageType) {
    const storageContent = document.getElementById('storage-content');
    const data = portfolioData.storage[storageType];
    
    if (storageType === 'google') {
        storageContent.innerHTML = data.map(item => `
            <div class="storage-item">
                <i class="fas fa-${item.type === 'folder' ? 'folder' : 'file'}"></i>
                <div class="storage-item-info">
                    <div class="storage-item-name">${item.name}</div>
                    <div class="storage-item-meta">
                        ${item.type === 'folder' ? `${item.items} items • ${item.size}` : `${item.size} • Modified ${item.modified}`}
                    </div>
                </div>
                <div class="storage-item-actions">
                    <button class="storage-action" onclick="downloadFile('${item.name}')">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="storage-action" onclick="shareFile('${item.name}')">
                        <i class="fas fa-share-alt"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } else if (storageType === 'github') {
        storageContent.innerHTML = data.map(repo => `
            <div class="storage-item">
                <i class="fab fa-github"></i>
                <div class="storage-item-info">
                    <div class="storage-item-name">${repo.name}</div>
                    <div class="storage-item-meta">
                        ⭐ ${repo.stars} stars • ${repo.language} • Updated ${repo.updated}
                    </div>
                </div>
                <div class="storage-item-actions">
                    <button class="storage-action" onclick="window.open('https://github.com/emmawilson/${repo.name}', '_blank')">
                        <i class="fas fa-external-link-alt"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } else if (storageType === 'aws') {
        storageContent.innerHTML = data.map(bucket => `
            <div class="storage-item">
                <i class="fab fa-aws"></i>
                <div class="storage-item-info">
                    <div class="storage-item-name">${bucket.name}</div>
                    <div class="storage-item-meta">
                        ${bucket.size} • ${bucket.objects} objects • ${bucket.region}
                    </div>
                </div>
                <div class="storage-item-actions">
                    <button class="storage-action" onclick="viewBucket('${bucket.name}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
}

// Load GitHub Activity
async function loadGitHubActivity() {
    // Simulate GitHub API call
    const lastCommit = "2 hours ago";
    const githubStars = portfolioData.projects.reduce((sum, p) => sum + p.stars, 0);
    const activeProjects = portfolioData.projects.length;
    
    document.getElementById('last-commit').textContent = lastCommit;
    document.getElementById('github-stars').textContent = githubStars;
    document.getElementById('active-projects').textContent = activeProjects;
}

// Load Contribution Heatmap
function loadHeatmap() {
    const heatmap = document.getElementById('heatmap');
    const weeks = 53;
    const days = 7;
    
    for (let i = 0; i < weeks * days; i++) {
        const level = Math.floor(Math.random() * 5);
        const cell = document.createElement('div');
        cell.className = `heatmap-cell level-${level}`;
        heatmap.appendChild(cell);
    }
}

// AI Assistant Functions
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Generate response
    setTimeout(() => {
        removeTypingIndicator();
        const response = generateResponse(message);
        addMessage(response, 'bot');
    }, 1000);
}

function generateResponse(message) {
    const lowerMsg = message.toLowerCase();
    
    if (lowerMsg.includes('project')) {
        return aiResponses.projects;
    } else if (lowerMsg.includes('skill')) {
        return aiResponses.skills;
    } else if (lowerMsg.includes('resume')) {
        return aiResponses.resume;
    } else if (lowerMsg.includes('contact')) {
        return aiResponses.contact;
    } else if (lowerMsg.includes('github')) {
        return aiResponses.github;
    } else if (lowerMsg.includes('experience')) {
        return aiResponses.experience;
    } else if (lowerMsg.includes('education')) {
        return aiResponses.education;
    } else {
        return "I'm here to help you learn more about Emma! You can ask me about her projects, skills, experience, education, or how to contact her. What would you like to know?";
    }
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const indicator = document.createElement('div');
    indicator.className = 'message bot';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<div class="message-content">Emma is typing<span>.</span><span>.</span><span>.</span></div>';
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

// Project Details Modal
function showProjectDetails(projectId) {
    const project = portfolioData.projects.find(p => p.id === projectId);
    alert(`Project: ${project.name}\n\n${project.description}\n\nTech Stack: ${project.tech.join(', ')}\n\nGitHub Stars: ${project.stars}\nForks: ${project.forks}\nCommits: ${project.commits}`);
}

// File Operations
function downloadFile(filename) {
    alert(`Downloading ${filename}...\n\nThis would trigger an actual file download in a real implementation.`);
}

function shareFile(filename) {
    alert(`Sharing ${filename}...\n\nThis would open a sharing dialog in a real implementation.`);
}

function viewBucket(bucketName) {
    alert(`Viewing bucket: ${bucketName}\n\nThis would show bucket contents in a real implementation.`);
}

// Setup Event Listeners
function setupEventListeners() {
    // Download resume
    document.getElementById('download-resume').addEventListener('click', () => {
        alert('Downloading Emma Wilson Resume.pdf\n\nThis would download the actual resume file.');
    });
    
    // Contact modal
    const modal = document.getElementById('contact-modal');
    const contactBtn = document.getElementById('contact-btn');
    const closeBtn = document.querySelector('.close');
    
    contactBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Contact form submission
    document.getElementById('contact-form').addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Message sent successfully! Emma will get back to you soon.');
        modal.style.display = 'none';
        e.target.reset();
    });
    
    // GitHub button
    document.getElementById('github-btn').addEventListener('click', () => {
        window.open('https://github.com/emmawilson', '_blank');
    });
    
    // Chat input
    document.getElementById('send-message').addEventListener('click', sendMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Storage tabs
    document.querySelectorAll('.storage-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.storage-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            loadStorage(tab.dataset.storage);
        });
    });
    
    // Refresh storage
    document.getElementById('refresh-storage').addEventListener('click', () => {
        const activeTab = document.querySelector('.storage-tab.active');
        loadStorage(activeTab.dataset.storage);
        alert('Storage content refreshed!');
    });
    
    // Suggestion chips
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.getElementById('chat-input').value = chip.textContent;
            sendMessage();
        });
    });
}

// Export functions for global access
window.showProjectDetails = showProjectDetails;
window.downloadFile = downloadFile;
window.shareFile = shareFile;
window.viewBucket = viewBucket;