/**
 * EcoPulse Lahore - Frontend Application Logic
 * Handles asynchronous API communication, state management, and real-time dashboard updates.
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// DOM Elements
const incidentForm = document.getElementById('incident-form');
const locationSelect = document.getElementById('location-select');
const reportInput = document.getElementById('report-text');
const submitBtn = document.getElementById('submit-btn');
const btnText = document.getElementById('btn-text');
const btnSpinner = document.getElementById('btn-spinner');

// Output DOM Elements
const outputPlaceholder = document.getElementById('output-placeholder');
const outputContent = document.getElementById('output-content');
const resCategory = document.getElementById('res-category');
const resSeverity = document.getElementById('res-severity');
const resLocation = document.getElementById('res-location');
const resAdvisory = document.getElementById('res-advisory');

/**
 * Event Listener for AI Threat Analysis Submission
 */
incidentForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const locationInfo = locationSelect.value;
    const reportText = reportInput.value.trim();

    if (!locationInfo || !reportText) {
        alert('Please select a location and describe the hazard before submitting.');
        return;
    }

    // Set UI to loading state
    setLoadingState(true);

    try {
        // Send request to FastAPI backend
        const response = await fetch(`${API_BASE_URL}/analyze-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                location: locationInfo,
                report_text: reportText
            })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        
        // Populate and display the results
        renderAnalysisOutput(data);

    } catch (error) {
        console.error('API Request Failed:', error);
        alert('Failed to connect to the EcoPulse AI engine. Please ensure the backend is running.');
        // Revert to placeholder on failure
        outputPlaceholder.classList.remove('hidden');
        outputContent.classList.add('hidden');
    } finally {
        // Restore button state
        setLoadingState(false);
    }
});

/**
 * Manages the button's loading spinner and disabled state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        btnText.textContent = 'Processing with AI...';
        btnSpinner.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        btnText.textContent = 'Analyze & Broadcast Advisory';
        btnSpinner.classList.add('hidden');
    }
}

/**
 * Populates the Output Card with the API Response
 */
function renderAnalysisOutput(data) {
    // Hide placeholder, show content
    outputPlaceholder.classList.add('hidden');
    outputContent.classList.remove('hidden');

    // Update UI elements
    resCategory.textContent = data.primary_category;
    resLocation.textContent = data.location;
    
    // Format Severity Score
    const severityPercentage = (data.severity_score * 100).toFixed(1);
    resSeverity.textContent = `Severity: ${severityPercentage}%`;
    
    // Adjust severity badge color dynamically based on threat level
    if (data.severity_score > 0.75) {
        resSeverity.style.backgroundColor = '#fee2e2'; // Light Red
        resSeverity.style.color = '#b91c1c'; // Dark Red
    } else if (data.severity_score > 0.40) {
        resSeverity.style.backgroundColor = '#fef3c7'; // Light Yellow
        resSeverity.style.color = '#b45309'; // Dark Yellow
    } else {
        resSeverity.style.backgroundColor = '#dcfce3'; // Light Green
        resSeverity.style.color = '#15803d'; // Dark Green
    }

    // Insert bilingual AI advisory text
    resAdvisory.textContent = data.public_advisory;

    // Smoothly scroll to the output on mobile devices
    if (window.innerWidth < 1024) {
        outputContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Live Dashboard Telemetry Simulation
 * Randomly fluctuates the environmental metrics to demonstrate real-time dashboard capabilities.
 */
function simulateLiveTelemetry() {
    const aqiElement = document.getElementById('aqi-value');
    const heatElement = document.getElementById('heat-value');
    const nodeElement = document.getElementById('node-value');

    setInterval(() => {
        // Fluctuate AQI between 300 and 330 (Hazardous range for Lahore smog)
        const currentAqi = parseInt(aqiElement.textContent);
        const aqiChange = Math.floor(Math.random() * 5) - 2; 
        aqiElement.textContent = Math.max(300, Math.min(350, currentAqi + aqiChange));

        // Fluctuate Heat Index 
        const currentHeat = parseFloat(heatElement.textContent);
        const heatChange = (Math.random() * 0.2 - 0.1);
        heatElement.textContent = `+${Math.max(2.5, Math.min(4.5, currentHeat + heatChange)).toFixed(1)}°C`;

    }, 3500); // Update every 3.5 seconds
}

// Initialize simulation on page load
document.addEventListener('DOMContentLoaded', () => {
    simulateLiveTelemetry();
});