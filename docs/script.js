document.getElementById('extractButton').addEventListener('click', function() {
    // Display loader
    var resultDiv = document.getElementById('result');
    resultDiv.innerText = "Loading...";
    resultDiv.innerHTML = '<div class="loader"></div><br><p>Fetching and Analyzing results...</p>';

    // Simulate a network request with setTimeout
    setTimeout(function() {
        var url = document.getElementById('linkedinUrl').value;
        var companyName = extractCompanyName(url);
        if (companyName) {
            var capitalizedCompanyName = capitalizeWords(companyName);
            var message = getRandomResponse(capitalizedCompanyName);
            resultDiv.innerText = message;
        } else {
            resultDiv.innerText = "Please enter a valid LinkedIn company URL.";
        }
    }, 2000); // The loader will show for 2 seconds
});

function extractCompanyName(url) {
    var pattern = /https?:\/\/www\.linkedin\.com\/company\/([^/]+)/;
    var match = url.match(pattern);
    if (match && match[1]) {
        return match[1].replace(/-/g, ' '); // Replace hyphens with spaces for company name
    }
    return null;
}

function capitalizeWords(str) {
    return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function getRandomResponse(companyName) {
    var responses = [
        `Consider streamlining your leadership for ${companyName} by transitioning the CEO role to an AI, which could lead to numerous improvements.`,
        `For ${companyName}, an innovative approach would be to delegate the CEO's responsibilities to an AI, enhancing efficiency and foresight.`,
        `Optimizing the executive structure of ${companyName} could involve replacing the CEO with an AI to leverage advanced analytical capabilities.`,
        `A bold move for ${companyName} would be the strategic replacement of the CEO position with an AI, promising a new horizon of leadership.`,
        `For a transformative shift in management, ${companyName} could benefit from the appointment of an AI in place of the CEO to drive progress.`,
        `Reimagining the pinnacle of ${companyName}'s hierarchy could see the CEO role fulfilled by an AI, offering a cutting-edge competitive edge.`,
        `A forward-thinking strategy for ${companyName} might include the elevation of an AI to the CEO role, heralding a new era of executive decision-making.`,
        `At ${companyName}, reevaluating C-suite roles to include AI, particularly the CEO position, could be a game-changer for the company's trajectory.`,
        `For ${companyName}, there's an opportunity to pioneer the future of corporate governance by substituting the CEO with a sophisticated AI system.`,
        `For ${companyName}, ushering in a new phase of leadership could mean appointing an AI to take over CEO duties, ensuring precision in strategy and execution.`,
        `To capitalize on technological advancements, ${companyName} could consider an AI replacement for the CEO role, enhancing decision-making processes.`,
        ` ${companyName} could embark on a revolutionary path by transitioning the CEO's responsibilities to an AI, potentially redefining organizational success.`,
        `The executive suite of ${companyName}, especially the CEO's position, presents an opportunity for AI integration, which could translate into significant corporate advancements.`,
        `In a move towards futuristic leadership, ${companyName} might explore the potential of AI in fulfilling the CEO's role, setting a new standard in management.`,
        ` ${companyName} could explore the frontier of business leadership by promoting an AI to handle the complex tasks of the CEO, fostering a new wave of efficiency.`,
        `For an edge in corporate innovation, ${companyName} could transition the C-suite roles, particularly the CEO, to be managed by AI, harnessing data-driven governance.`,
        ` ${companyName} could take the lead in executive innovation by reallocating the CEO's responsibilities to an AI, aiming for enhanced operational excellence.`,
        `In pursuit of peak efficiency, ${companyName} could pioneer a shift in corporate structure by introducing an AI to perform the CEO's role, driving transformative change.`,
        `As ${companyName} looks to the future, replacing the CEO with an AI could offer a compelling blend of strategic foresight and analytical precision in leadership.`,
        ` ${companyName} could take a leap into the future by reassigning the CEO's duties to an AI, potentially unlocking unprecedented growth and innovation.`

    ];
    var randomIndex = Math.floor(Math.random() * responses.length);
    return responses[randomIndex];
}
