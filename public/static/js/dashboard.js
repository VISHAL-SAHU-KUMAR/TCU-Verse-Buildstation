// ==================== DASHBOARD.JS - Main Dashboard Logic ====================

// Global state
let currentUser = null;
let currentResumeId = null;
let currentAnalysis = null;
let extractedSkills = null;

// API Base URL
const API_BASE = "/api";

// ==================== INITIALIZATION ====================

document.addEventListener("DOMContentLoaded", () => {
  checkAuthentication();
  initializeEventListeners();
  initializeSidebar();
});

// ==================== AUTHENTICATION ====================

async function checkAuthentication() {
  try {
    const response = await fetch(`${API_BASE}/check-auth`, {
      credentials: "include",
    });
    const data = await response.json();

    if (data.authenticated) {
      currentUser = data.user;
      updateUserDisplay();
      loadDashboardData();
    } else {
      // Redirect to landing page
      window.location.href = "/index.html";
    }
  } catch (error) {
    console.error("Auth check error:", error);
    showToast("Authentication error. Please login again.", "error");
    setTimeout(() => {
      window.location.href = "/index.html";
    }, 2000);
  }
}

function updateUserDisplay() {
  const userName = document.getElementById("userName");
  const userNameDisplay = document.getElementById("userNameDisplay");

  if (userName) userName.textContent = currentUser.full_name.split(" ")[0];
  if (userNameDisplay)
    userNameDisplay.textContent = currentUser.full_name.split(" ")[0];
}

// Logout
document.getElementById("logoutBtn")?.addEventListener("click", async () => {
  try {
    await fetch(`${API_BASE}/logout`, {
      method: "POST",
      credentials: "include",
    });
    showToast("Logged out successfully", "success");
    setTimeout(() => {
      window.location.href = "/index.html";
    }, 1000);
  } catch (error) {
    console.error("Logout error:", error);
  }
});

// ==================== SIDEBAR NAVIGATION ====================

function initializeSidebar() {
  const navItems = document.querySelectorAll(".sidebar-nav .nav-item");
  const sections = document.querySelectorAll(".content-section");

  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();

      // Remove active class from all items
      navItems.forEach((nav) => nav.classList.remove("active"));

      // Add active class to clicked item
      item.classList.add("active");

      // Get section name
      const sectionName = item.dataset.section;

      // Hide all sections
      sections.forEach((section) => section.classList.remove("active"));

      // Show target section
      const targetSection = document.getElementById(`${sectionName}Section`);
      if (targetSection) {
        targetSection.classList.add("active");
      }
    });
  });

  // Sidebar toggle for mobile
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");

  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("active");
    });
  }
}

// Quick actions navigation
document.querySelectorAll(".action-card").forEach((card) => {
  card.addEventListener("click", () => {
    const targetSection = card.dataset.goto;
    const targetNavItem = document.querySelector(
      `.nav-item[data-section="${targetSection}"]`,
    );
    if (targetNavItem) {
      targetNavItem.click();
    }
  });
});

// ==================== DASHBOARD DATA ====================

async function loadDashboardData() {
  try {
    showLoading();

    const response = await fetch(`${API_BASE}/dashboard`, {
      credentials: "include",
    });
    const data = await response.json();

    if (data.success) {
      updateDashboardStats(data.analyses);
      displayRecentAnalyses(data.analyses);
    }

    hideLoading();
  } catch (error) {
    console.error("Dashboard data error:", error);
    hideLoading();
  }
}

function updateDashboardStats(analyses) {
  const totalResumes = document.getElementById("totalResumes");
  const avgScore = document.getElementById("avgScore");
  const skillsMastered = document.getElementById("skillsMastered");
  const coursesCount = document.getElementById("coursesCount");

  if (totalResumes) totalResumes.textContent = analyses.length;

  if (avgScore && analyses.length > 0) {
    const avg = Math.round(
      analyses.reduce((sum, a) => sum + a.score, 0) / analyses.length,
    );
    avgScore.textContent = `${avg}%`;
  }

  if (skillsMastered) {
    const mastered = analyses.filter((a) => a.score >= 80).length * 5;
    skillsMastered.textContent = mastered;
  }

  if (coursesCount) {
    coursesCount.textContent = analyses.length * 8;
  }
}

function displayRecentAnalyses(analyses) {
  const recentAnalyses = document.getElementById("recentAnalyses");
  const historyContainer = document.getElementById("historyContainer");

  if (!analyses || analyses.length === 0) {
    if (recentAnalyses) {
      recentAnalyses.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>No analyses yet. Upload your resume to get started!</p>
                </div>
            `;
    }
    return;
  }

  const analysesHTML = analyses
    .map(
      (analysis) => `
        <div class="analysis-item">
            <div class="analysis-info">
                <div class="analysis-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <div class="analysis-details">
                    <h4>${analysis.target_role}</h4>
                    <p>${new Date(analysis.date).toLocaleDateString("en-IN", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}</p>
                </div>
            </div>
            <div class="analysis-score">${analysis.score}%</div>
        </div>
    `,
    )
    .join("");

  if (recentAnalyses) {
    recentAnalyses.innerHTML = analysesHTML;
  }

  if (historyContainer) {
    historyContainer.innerHTML = `
            <div class="analyses-list">
                ${analysesHTML}
            </div>
        `;
  }
}

// ==================== RESUME UPLOAD ====================

function initializeEventListeners() {
  const uploadArea = document.getElementById("uploadArea");
  const resumeInput = document.getElementById("resumeInput");
  const browseBtn = document.getElementById("browseBtn");

  if (uploadArea) {
    // Click to upload
    uploadArea.addEventListener("click", () => {
      resumeInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = "var(--primary-color)";
      uploadArea.style.background = "#f9fafb";
    });

    uploadArea.addEventListener("dragleave", (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = "var(--border-color)";
      uploadArea.style.background = "var(--white)";
    });

    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = "var(--border-color)";
      uploadArea.style.background = "var(--white)";

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        handleFileUpload(files[0]);
      }
    });
  }

  if (browseBtn) {
    browseBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      resumeInput.click();
    });
  }

  if (resumeInput) {
    resumeInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
      }
    });
  }

  // Proceed to analysis button
  const proceedBtn = document.getElementById("proceedToAnalysis");
  if (proceedBtn) {
    proceedBtn.addEventListener("click", () => {
      // Switch to analysis section
      const analysisNavItem = document.querySelector(
        '.nav-item[data-section="analysis"]',
      );
      if (analysisNavItem) {
        analysisNavItem.click();
      }
    });
  }

  // Role selection
  initializeRoleSelection();
}

async function handleFileUpload(file) {
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showToast("Please upload a PDF file", "error");
    return;
  }

  if (file.size > 16 * 1024 * 1024) {
    showToast("File size must be less than 16MB", "error");
    return;
  }

  const uploadArea = document.getElementById("uploadArea");
  const uploadProgress = document.getElementById("uploadProgress");
  const uploadSuccess = document.getElementById("uploadSuccess");
  const progressFill = document.getElementById("progressFill");
  const uploadStatus = document.getElementById("uploadStatus");

  // Hide upload area, show progress
  uploadArea.style.display = "none";
  uploadProgress.style.display = "block";

  const formData = new FormData();
  formData.append("resume", file);

  try {
    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += 10;
      if (progress <= 90) {
        progressFill.style.width = `${progress}%`;
      }
    }, 200);

    const response = await fetch(`${API_BASE}/upload-resume`, {
      method: "POST",
      credentials: "include",
      body: formData,
    });

    clearInterval(progressInterval);
    progressFill.style.width = "100%";

    const data = await response.json();

    if (response.ok && data.success) {
      currentResumeId = data.resume_id;
      extractedSkills = data.skills;

      uploadStatus.textContent = "Upload complete!";

      setTimeout(() => {
        uploadProgress.style.display = "none";
        uploadSuccess.style.display = "block";

        // Display extracted skills preview
        displayExtractedSkills(data.skills);
      }, 500);

      showToast("Resume uploaded successfully!", "success");
    } else {
      throw new Error(data.error || "Upload failed");
    }
  } catch (error) {
    console.error("Upload error:", error);
    showToast(error.message || "Upload failed. Please try again.", "error");

    // Reset upload area
    uploadProgress.style.display = "none";
    uploadArea.style.display = "block";
  }
}

function displayExtractedSkills(skills) {
  const extractedPreview = document.getElementById("extractedPreview");

  if (!extractedPreview) return;

  const categories = [
    { key: "programming_languages", label: "Programming Languages" },
    { key: "web_technologies", label: "Web Technologies" },
    { key: "data_science", label: "Data Science" },
    { key: "databases", label: "Databases" },
    { key: "cloud_devops", label: "Cloud & DevOps" },
  ];

  let html = "<h4>Extracted Skills:</h4>";

  categories.forEach((cat) => {
    if (skills[cat.key] && skills[cat.key].length > 0) {
      html += `
                <div class="skill-category">
                    <strong>${cat.label}:</strong>
                    <div class="skill-tags">
                        ${skills[cat.key]
                          .map(
                            (skill) =>
                              `<span class="skill-tag present">${skill}</span>`,
                          )
                          .join("")}
                    </div>
                </div>
            `;
    }
  });

  html += `<p style="margin-top: 15px; color: var(--text-secondary);">
        <strong>Career Level:</strong> ${skills.career_level}
    </p>`;

  extractedPreview.innerHTML = html;
}

// ==================== ROLE SELECTION & ANALYSIS ====================

function initializeRoleSelection() {
  const roleOptions = document.querySelectorAll(".role-option");

  roleOptions.forEach((option) => {
    option.addEventListener("click", async () => {
      if (!currentResumeId) {
        showToast("Please upload your resume first", "warning");
        // Switch to upload section
        const uploadNavItem = document.querySelector(
          '.nav-item[data-section="upload"]',
        );
        if (uploadNavItem) uploadNavItem.click();
        return;
      }

      // Remove selected class from all options
      roleOptions.forEach((opt) => opt.classList.remove("selected"));

      // Add selected class to clicked option
      option.classList.add("selected");

      const targetRole = option.dataset.role;

      // Perform analysis
      await performSkillAnalysis(targetRole);
    });
  });
}

async function performSkillAnalysis(targetRole) {
  try {
    showLoading("Analyzing your skills...");

    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        resume_id: currentResumeId,
        target_role: targetRole,
      }),
    });

    const data = await response.json();

    if (response.ok && data.success) {
      currentAnalysis = data;

      // Display analysis results
      displayAnalysisResults(data, targetRole);

      // Generate and display roadmap
      displayRoadmap(data.roadmap, targetRole);

      // Display course recommendations
      displayCourseRecommendations(data.course_recommendations);

      showToast("Analysis complete!", "success");

      // Reload dashboard data
      loadDashboardData();
    } else {
      throw new Error(data.error || "Analysis failed");
    }

    hideLoading();
  } catch (error) {
    console.error("Analysis error:", error);
    showToast(error.message || "Analysis failed. Please try again.", "error");
    hideLoading();
  }
}

function displayAnalysisResults(data, targetRole) {
  const analysisResults = document.getElementById("analysisResults");
  const selectedRole = document.getElementById("selectedRole");
  const skillScore = document.getElementById("skillScore");
  const gapSummary = document.getElementById("gapSummary");
  const careerLevel = document.getElementById("careerLevel");
  const presentSkills = document.getElementById("presentSkills");
  const criticalMissing = document.getElementById("criticalMissing");
  const importantMissing = document.getElementById("importantMissing");
  const niceToHave = document.getElementById("niceToHave");
  const scoreCircle = document.getElementById("scoreCircle");

  // Show results section
  if (analysisResults) {
    analysisResults.style.display = "block";
  }

  // Update role
  if (selectedRole) {
    selectedRole.textContent = targetRole;
  }

  // Update score
  const score = data.gap_analysis.score;
  if (skillScore) {
    skillScore.textContent = score;
  }

  // Animate score circle
  if (scoreCircle) {
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (score / 100) * circumference;
    scoreCircle.style.strokeDashoffset = offset;
  }

  // Update summary
  if (gapSummary) {
    gapSummary.textContent = data.gap_analysis.gap_summary;
  }

  // Update career level
  if (careerLevel) {
    careerLevel.textContent = data.career_level;
  }

  // Update skills
  if (presentSkills) {
    presentSkills.innerHTML = data.gap_analysis.present_skills
      .map((skill) => `<span class="skill-tag present">${skill}</span>`)
      .join("");
  }

  if (criticalMissing) {
    criticalMissing.innerHTML = data.gap_analysis.critical_missing
      .map((skill) => `<span class="skill-tag missing">${skill}</span>`)
      .join("");
  }

  if (importantMissing) {
    importantMissing.innerHTML = data.gap_analysis.important_missing
      .map((skill) => `<span class="skill-tag missing">${skill}</span>`)
      .join("");
  }

  if (niceToHave) {
    niceToHave.innerHTML = data.gap_analysis.nice_to_have_missing
      .map((skill) => `<span class="skill-tag optional">${skill}</span>`)
      .join("");
  }

  // Scroll to results
  analysisResults.scrollIntoView({ behavior: "smooth", block: "start" });
}

function displayRoadmap(roadmap, targetRole) {
  const roadmapContainer = document.getElementById("roadmapContainer");

  if (!roadmapContainer) return;

  const phases = [
    {
      key: "beginner",
      title: "Beginner Phase",
      icon: "fa-seedling",
      color: "#10b981",
    },
    {
      key: "intermediate",
      title: "Intermediate Phase",
      icon: "fa-chart-line",
      color: "#3b82f6",
    },
    {
      key: "advanced",
      title: "Advanced Phase",
      icon: "fa-trophy",
      color: "#8b5cf6",
    },
  ];

  let html = "";

  phases.forEach((phase) => {
    const phaseData = roadmap[phase.key];

    html += `
            <div class="roadmap-phase">
                <div class="phase-header">
                    <div class="phase-icon">
                        <i class="fas ${phase.icon}"></i>
                    </div>
                    <div class="phase-title">
                        <h3>${phase.title}</h3>
                        <p>${phaseData.duration}</p>
                    </div>
                </div>
                <div class="phase-content">
                    ${
                      phaseData.skills && phaseData.skills.length > 0
                        ? `
                        <h4><i class="fas fa-book"></i> Skills to Learn</h4>
                        <ul>
                            ${phaseData.skills.map((skill) => `<li>${skill}</li>`).join("")}
                        </ul>
                    `
                        : ""
                    }

                    ${
                      phaseData.projects && phaseData.projects.length > 0
                        ? `
                        <h4><i class="fas fa-project-diagram"></i> Practice Projects</h4>
                        <ul>
                            ${phaseData.projects.map((project) => `<li>${project}</li>`).join("")}
                        </ul>
                    `
                        : ""
                    }
                </div>
            </div>
        `;
  });

  roadmapContainer.innerHTML = html;
}

function displayCourseRecommendations(courses) {
  const coursesContainer = document.getElementById("coursesContainer");

  if (!coursesContainer || !courses || courses.length === 0) return;

  const html = courses
    .map(
      (course) => `
        <div class="course-card">
            <div class="course-header">
                <div class="course-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <div class="course-info">
                    <h3>${course.skill}</h3>
                    <div class="course-platform">${course.platform}</div>
                </div>
            </div>
            <div class="course-description">
                ${course.reason}
            </div>
            <a href="#" class="course-link">
                <i class="fas fa-external-link-alt"></i> Learn More
            </a>
        </div>
    `,
    )
    .join("");

  coursesContainer.innerHTML = html;
}

// ==================== LOADING & TOAST ====================

function showLoading(message = "Loading...") {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) {
    overlay.classList.add("active");
    const text = overlay.querySelector("p");
    if (text) text.textContent = message;
  }
}

function hideLoading() {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) {
    overlay.classList.remove("active");
  }
}

function showToast(message, type = "info") {
  const toastContainer = document.getElementById("toastContainer");

  if (!toastContainer) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  const icon =
    type === "success"
      ? "fa-check-circle"
      : type === "error"
        ? "fa-exclamation-circle"
        : type === "warning"
          ? "fa-exclamation-triangle"
          : "fa-info-circle";

  toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span class="toast-message">${message}</span>
    `;

  toastContainer.appendChild(toast);

  // Remove after 4 seconds
  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 4000);
}

// Add slideOut animation
const style = document.createElement("style");
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== PROFILE MANAGEMENT ====================

async function loadProfileData() {
  try {
    showLoading("Loading profile...");

    const response = await fetch(`${API_BASE}/profile`, {
      credentials: "include",
    });

    const data = await response.json();

    if (response.ok && data.success) {
      const profile = data.profile;
      const stats = data.stats;

      // Update profile display
      if (document.getElementById("profileName")) {
        document.getElementById("profileName").textContent = profile.full_name;
      }
      if (document.getElementById("profileEmail")) {
        document.getElementById("profileEmail").textContent = profile.email;
      }

      // Update avatar
      const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.full_name)}&background=667eea&color=fff&size=120`;
      if (document.getElementById("profileAvatar")) {
        document.getElementById("profileAvatar").src = avatarUrl;
      }

      // Update join date
      if (document.getElementById("profileJoinDate")) {
        const joinDate = new Date(profile.created_at);
        document.getElementById("profileJoinDate").textContent =
          joinDate.toLocaleDateString("en-IN", {
            year: "numeric",
            month: "short",
          });
      }

      // Update stats
      if (document.getElementById("profileResumeCount")) {
        document.getElementById("profileResumeCount").textContent =
          stats.resume_count;
      }
      if (document.getElementById("profileAnalysisCount")) {
        document.getElementById("profileAnalysisCount").textContent =
          stats.analysis_count;
      }
      if (document.getElementById("profileAvgScore")) {
        document.getElementById("profileAvgScore").textContent =
          `${stats.avg_score}%`;
      }

      // Populate edit form
      if (document.getElementById("editFullName")) {
        document.getElementById("editFullName").value = profile.full_name || "";
      }
      if (document.getElementById("editEmail")) {
        document.getElementById("editEmail").value = profile.email || "";
      }
      if (document.getElementById("editPhone")) {
        document.getElementById("editPhone").value = profile.phone || "";
      }
      if (document.getElementById("editLocation")) {
        document.getElementById("editLocation").value = profile.location || "";
      }
      if (document.getElementById("editBio")) {
        document.getElementById("editBio").value = profile.bio || "";
      }
      if (document.getElementById("editLinkedIn")) {
        document.getElementById("editLinkedIn").value = profile.linkedin || "";
      }
      if (document.getElementById("editGitHub")) {
        document.getElementById("editGitHub").value = profile.github || "";
      }
    }

    hideLoading();
  } catch (error) {
    console.error("Profile load error:", error);
    hideLoading();
    showToast("Failed to load profile", "error");
  }
}

// Edit Profile Form Handler
const editProfileForm = document.getElementById("editProfileForm");
if (editProfileForm) {
  editProfileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
      full_name: document.getElementById("editFullName").value,
      email: document.getElementById("editEmail").value,
      phone: document.getElementById("editPhone").value,
      location: document.getElementById("editLocation").value,
      bio: document.getElementById("editBio").value,
      linkedin: document.getElementById("editLinkedIn").value,
      github: document.getElementById("editGitHub").value,
    };

    try {
      showLoading("Updating profile...");

      const response = await fetch(`${API_BASE}/profile`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showToast("Profile updated successfully!", "success");

        // Update user display
        currentUser.full_name = formData.full_name;
        currentUser.email = formData.email;
        updateUserDisplay();

        // Reload profile data
        await loadProfileData();
      } else {
        showToast(data.error || "Failed to update profile", "error");
      }

      hideLoading();
    } catch (error) {
      console.error("Profile update error:", error);
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

// Change Password Form Handler
const changePasswordForm = document.getElementById("changePasswordForm");
if (changePasswordForm) {
  changePasswordForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const currentPassword = document.getElementById("currentPassword").value;
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Validate passwords match
    if (newPassword !== confirmPassword) {
      showToast("New passwords do not match", "error");
      return;
    }

    // Validate password length
    if (newPassword.length < 6) {
      showToast("Password must be at least 6 characters", "error");
      return;
    }

    try {
      showLoading("Updating password...");

      const response = await fetch(`${API_BASE}/change-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showToast("Password updated successfully!", "success");
        changePasswordForm.reset();
      } else {
        showToast(data.error || "Failed to update password", "error");
      }

      hideLoading();
    } catch (error) {
      console.error("Password change error:", error);
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

// Delete Account Handler
const deleteAccountBtn = document.getElementById("deleteAccountBtn");
if (deleteAccountBtn) {
  deleteAccountBtn.addEventListener("click", async () => {
    const confirmation = confirm(
      "⚠️ WARNING: This action cannot be undone!\n\n" +
        "Are you absolutely sure you want to delete your account?\n" +
        "All your resumes, analyses, and data will be permanently deleted.",
    );

    if (!confirmation) return;

    const doubleConfirm = confirm(
      "Last chance! Type DELETE in the next prompt to confirm account deletion.",
    );

    if (!doubleConfirm) return;

    const finalConfirm = prompt("Type DELETE (in capital letters) to confirm:");

    if (finalConfirm !== "DELETE") {
      showToast("Account deletion cancelled", "warning");
      return;
    }

    try {
      showLoading("Deleting account...");

      const response = await fetch(`${API_BASE}/delete-account`, {
        method: "DELETE",
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showToast("Account deleted successfully", "success");
        setTimeout(() => {
          window.location.href = "/index.html";
        }, 2000);
      } else {
        showToast(data.error || "Failed to delete account", "error");
      }

      hideLoading();
    } catch (error) {
      console.error("Account deletion error:", error);
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

// Change Avatar Handler
const changeAvatarBtn = document.getElementById("changeAvatarBtn");
if (changeAvatarBtn) {
  changeAvatarBtn.addEventListener("click", () => {
    showToast("Avatar upload coming soon!", "info");
    // Future: Implement file upload for custom avatars
  });
}

// Load profile data when profile section is opened
const profileNavItem = document.querySelector(
  '.nav-item[data-section="profile"]',
);
if (profileNavItem) {
  profileNavItem.addEventListener("click", () => {
    loadProfileData();
  });
}

// ==================== CONSOLE BRANDING ====================

console.log(
  "%c🧠 SkillLens AI Dashboard",
  "color: #667eea; font-size: 20px; font-weight: bold;",
);
console.log(
  "%cWelcome to your career intelligence hub!",
  "color: #764ba2; font-size: 12px;",
);
