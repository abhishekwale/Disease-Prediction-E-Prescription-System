
document.addEventListener("DOMContentLoaded", () => {
// DOM Elements
const sidebar = document.getElementById("sidebar")
const toggleSidebar = document.getElementById("toggleSidebar")
const loginBtn = document.getElementById("loginBtn")
const logoutBtn = document.getElementById("logoutBtn")
const userName = document.getElementById("userName")
const resetButton = document.getElementById("resetButton")
const symptomForm = document.getElementById("symptomForm")
const symptomsInput = document.getElementById("symptoms")
const errorMessage = document.getElementById("errorMessage")
const chatMessages = document.getElementById("chatMessages")
const resultsContainer = document.getElementById("resultsContainer")

// Toggle sidebar functionality
toggleSidebar.addEventListener("click", () => {
sidebar.classList.toggle("expanded")
})

// Handle responsive sidebar
function handleResponsiveSidebar() {
if (window.innerWidth <= 992) {
sidebar.classList.remove("expanded")
if (window.innerWidth <= 576) {
  toggleSidebar.style.display = "flex"
}
} else {
sidebar.classList.remove("expanded")
toggleSidebar.style.display = "none"
}
}

// Initialize responsive sidebar
handleResponsiveSidebar()
window.addEventListener("resize", handleResponsiveSidebar)

// Login/Logout functionality (mock)
loginBtn.addEventListener("click", () => {
// Mock login - in a real app, this would be a proper authentication
const mockUserName = prompt("Enter your name to login:")
if (mockUserName && mockUserName.trim() !== "") {
userName.textContent = mockUserName
loginBtn.style.display = "none"
logoutBtn.style.display = "flex"

// Add welcome message
addBotMessage(`Welcome, ${mockUserName}! How can I help you today?`)
}
})

logoutBtn.addEventListener("click", () => {
// Mock logout
userName.textContent = "Guest"
loginBtn.style.display = "flex"
logoutBtn.style.display = "none"

// Add logout message
addBotMessage("You have been logged out. Have a great day!")
})

// Reset functionality
resetButton.addEventListener("click", () => {
symptomsInput.value = ""
errorMessage.textContent = ""
resultsContainer.style.display = "none"

// Clear chat except for the first welcome message
while (chatMessages.children.length > 1) {
chatMessages.removeChild(chatMessages.lastChild)
}

// Add reset message
addBotMessage("The conversation has been reset. Please describe your symptoms when you're ready.")
})

// Form submission
symptomForm.addEventListener("submit", (e) => {
e.preventDefault()

const symptoms = symptomsInput.value.trim()

if (!symptoms) {
errorMessage.textContent = "Please enter your symptoms."
return
}

errorMessage.textContent = ""

// Add user message to chat
addUserMessage(symptoms)

// Simulate processing (in a real app, this would be an API call)
addBotMessage("Analyzing your symptoms...")

// Mock data for demonstration
setTimeout(() => {
// Mock prediction data
const mockPrediction = {
  disease: "Common Cold",
  description:
    "The common cold is a viral infection of your nose and throat (upper respiratory tract). It's usually harmless, although it might not feel that way. Many types of viruses can cause a common cold.",
  precautions: [
    "Rest and stay hydrated",
    "Use a humidifier or take a hot shower to ease congestion",
    "Gargle with salt water to soothe a sore throat",
    "Avoid contact with others to prevent spreading the virus",
  ],
  medications: [
    "Over-the-counter pain relievers like acetaminophen or ibuprofen",
    "Decongestants to relieve nasal congestion",
    "Cough syrups or drops to suppress coughing",
    "Antihistamines may help if allergies are contributing to symptoms",
  ],
  workout: [
    "Light walking if you feel up to it",
    "Gentle stretching to relieve body aches",
    "Avoid strenuous exercise until symptoms improve",
    "Resume normal activity gradually as you recover",
  ],
  diet: [
    "Drink plenty of fluids like water, tea, and clear broths",
    "Consume vitamin C-rich foods like citrus fruits",
    "Eat chicken soup, which may help reduce inflammation",
    "Consume honey to soothe a sore throat (not for children under 1 year)",
  ],
}

// Display results
displayResults(symptoms, mockPrediction)

// Add bot response about prediction
addBotMessage(
  `Based on your symptoms, I predict you may have: <strong>${mockPrediction.disease}</strong>. I've prepared detailed information below.`,
)

// Scroll to results
resultsContainer.scrollIntoView({ behavior: "smooth" })
}, 2000)

// Clear input
symptomsInput.value = ""
})

// Helper function to add user message to chat
function addUserMessage(message) {
const messageDiv = document.createElement("div")
messageDiv.className = "message user-message"
messageDiv.innerHTML = `
      <div class="message-content">
          <p>${message}</p>
      </div>
      <div class="message-avatar">
          <i class="fas fa-user"></i>
      </div>
  `
chatMessages.appendChild(messageDiv)
chatMessages.scrollTop = chatMessages.scrollHeight
}

// Helper function to add bot message to chat
function addBotMessage(message) {
const messageDiv = document.createElement("div")
messageDiv.className = "message bot-message"
messageDiv.innerHTML = `
      <div class="message-avatar">
          <i class="fas fa-robot"></i>
      </div>
      <div class="message-content">
          <p>${message}</p>
      </div>
  `
chatMessages.appendChild(messageDiv)
chatMessages.scrollTop = chatMessages.scrollHeight
}

// Helper function to display results
function displayResults(symptoms, prediction) {
// Update symptom summary
document.getElementById("symptomsSummary").textContent = `Showing predictions for: ${symptoms}`

// Update disease
document.getElementById("predictedDisease").textContent = prediction.disease

// Update description
document.getElementById("diseaseDescription").textContent = prediction.description

// Update precautions
const precautionsList = document.getElementById("precautionsList")
precautionsList.innerHTML = ""
prediction.precautions.forEach((item) => {
const li = document.createElement("li")
li.textContent = item
precautionsList.appendChild(li)
})

// Update medications
const medicationsList = document.getElementById("medicationsList")
medicationsList.innerHTML = ""
prediction.medications.forEach((item) => {
const li = document.createElement("li")
li.textContent = item
medicationsList.appendChild(li)
})

// Update workout
const workoutList = document.getElementById("workoutList")
workoutList.innerHTML = ""
prediction.workout.forEach((item) => {
const li = document.createElement("li")
li.textContent = item
workoutList.appendChild(li)
})

// Update diet
const dietList = document.getElementById("dietList")
dietList.innerHTML = ""
prediction.diet.forEach((item) => {
const li = document.createElement("li")
li.textContent = item
dietList.appendChild(li)
})

// Show results container
resultsContainer.style.display = "block"
}
})


function toggleForm(type) {
    const predictForm = document.getElementById('predict-form');
    const searchForm = document.getElementById('pincode-form');
    const buttons = document.querySelectorAll('.toggle-btn');

    buttons.forEach(btn => btn.classList.remove('active'));

    if (type === 'predict') {
        predictForm.style.display = 'block';
        searchForm.style.display = 'none';
        buttons[0].classList.add('active');
    } else {
        predictForm.style.display = 'none';
        searchForm.style.display = 'block';
        buttons[1].classList.add('active');
    }
}

document.getElementById('pincode-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const pincode = e.target.pincode.value;
    
    const formData = new FormData();
    formData.append('pincode', pincode);

    const response = await fetch('/search-maps', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    if (data.maps_url) {
        window.open(data.maps_url, '_blank'); // Opens in a new tab
    }
});



