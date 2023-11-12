// game.js


const gtext = document.createElement("p");
gtext.id = "game-text";
gtext.textContent = "";
document.querySelector("body").appendChild(gtext);
const gameText = document.getElementById("game-text"); // Define the gameText variable
let companyData = {
    'round': 1,
};

let sequentialScenarios; // Define the variable to store the game data
let randomScenarios;
let randomEvents;
let previousConsequences;
const scenarioHistory = [];
const maxHistoryLength = 3; // Adjust this value as needed
// Load game data from JSON (replace with your actual fetch logic)
async function loadGameData() {
    try {
        const response = await fetch("js/gameData.json");
        const data = await response.json();
        console.log(data)
        sequentialScenarios = data.sequentialScenarios; // Store the sequential scenarios
        randomScenarios = data.randomScenarios;
        events = data.events;

        console.log(sequentialScenarios)
        return data;
    } catch (error) {
        console.error("Error loading game data:", error);
        return null;
    }
}

// Call the loadGameData function to load the data
loadGameData()
    .then((gameData) => {
        if (gameData) {
            // The game data is loaded, you can now proceed with presenting scenarios
            presentNextScenario();
        } else {
            // Handle errors if needed
        }
    })
    .catch((error) => {
        console.error("Error loading game data:", error);
    });

// Assuming companyData has properties for shareholderSatisfaction, customerSatisfaction, and stockPrice
// You should initialize these in companyData object
companyData.shareholderSatisfaction = 0;
companyData.customerSatisfaction = 0;
companyData.stockPrice = 1.00; // Assuming a baseline stock price of 1.00
// Define endgame events
let endgameEvents = [
  {
    id: 'bankruptcy',
    condition: (companyData) => companyData.stockPrice <= 0.1,
    narrative: 'Due to poor financial management and a series of bad investments, your company has gone bankrupt.',
    effect: 'endgame'
  },
  {
    id: 'buyout',
    condition: (companyData) => companyData.shareholderSatisfaction < -10,
    narrative: 'Shareholder dissatisfaction has led to a hostile takeover. Your company is now owned by a competitor.',
    effect: 'endgame'
  },
  {
    id: 'fired',
    condition: (companyData) => companyData.customerSatisfaction < -10,
    narrative: 'Customer satisfaction has plummeted, leading to a loss of trust. The board has decided to let you go. Don\'t worry, your parachute is golden.',
    effect: 'endgame'
  }
];
// Function to update the display
function updateScoreDisplay() {
  const companyNameDisplay = document.getElementById('companyNameDisplay');
  const shareholderSatisfactionDisplay = document.getElementById('shareholderSatisfactionDisplay');
  const customerSatisfactionDisplay = document.getElementById('customerSatisfactionDisplay');
  const stockPriceDisplay = document.getElementById('stockPriceDisplay');

  companyNameDisplay.textContent = companyData['name'] || 'Not set';
  shareholderSatisfactionDisplay.textContent = companyData.shareholderSatisfaction;
  customerSatisfactionDisplay.textContent = companyData.customerSatisfaction;
  stockPriceDisplay.textContent = companyData.stockPrice.toFixed(2); // Fix to 2 decimal places
}

// Call this function whenever you need to update the scores, for example after handling choices
function handleConsequences(consequences) {
    // show the consequences text
    previousConsequences = consequences;
    console.log('handleconsequences function')
    console.log(previousConsequences)

  if (consequences.stockPrice) {
    companyData.stockPrice += consequences.stockPrice;
  }
  if (consequences.shareholderSatisfaction) {
    companyData.shareholderSatisfaction += consequences.shareholderSatisfaction;
  }
  if (consequences.customerSatisfaction) {
    companyData.customerSatisfaction += consequences.customerSatisfaction;
  }

    updateScoreDisplay();
}




let sequentialScenarioIndex = 0; // Initialize the index for sequential scenarios

// Function to get the next sequential scenario
function getNextSequentialScenario() {
    if (sequentialScenarioIndex < sequentialScenarios.length) {
        return sequentialScenarios[sequentialScenarioIndex++];
    }
    return null;
}
// After loading game data, assign randomScenarios

// Function to randomly select a scenario from randomScenarios
function getRandomScenario(scenarios) {
    if (scenarios.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * scenarios.length);
    return scenarios[randomIndex];
}

function formatNarrative(narrative, companyData) {
  console.log(companyData);
  // for each property in companyData console log the property name and value
  for (const property in companyData) {
      console.log('for loop')
    console.log(`${property}: ${companyData[property]}`);
  }

  // Corrected regular expression to match the placeholders in the narrative
  narrative = narrative.replace(/\{(\w+(\.\w+)?)}/g, (match, propName) => {
    // Split the property name on dots in case of nested properties like aiImplementer.name
    const propParts = propName.split('.');
    let propValue = companyData;
    console.log(propValue)

    // Iterate through parts to access nested properties
    for (const part of propParts) {
      if (propValue[part] !== undefined) {
        propValue = propValue[part];
      } else {
        // If property does not exist, return a placeholder string
        propValue = `[${propName} not set]`;
        break;
      }
    }

    console.log(match);
    console.log(propName);
    console.log(propValue);

    return propValue;
  });

  return narrative;
}




// Function to present the next scenario
// Function to present the next scenario
function presentNextScenario() {
    // Check if there are any more sequential scenarios to present
    const nextScenario = getNextSequentialScenario();
    console.log(nextScenario)
    checkForEvents(); // New addition to check for triggered events

    if (nextScenario) {
        // Check if the scenario has a 'randomAIImplementer' effect and handle it
        if (nextScenario.id === "randomAIImplementer") {
            handleRandomAIImplementerEffect(nextScenario);
        } else if (nextScenario.input) {
            // If the scenario has an input field, display input field and submit button
            displayInputScenario(nextScenario);
        } else {
            // If the scenario has choices, display choice buttons
            displayChoiceScenario(nextScenario);
        }
    } else {
        // If sequential scenarios are finished, check if it's time to start the game
            if (!nextScenario && companyData.gameState === 'game') {
    // Begin presenting random scenarios
    if (!checkEndgameEvents()) { // Only proceed if the game hasn't ended
      presentRandomScenario();
    }
  }
}

    function presentEvent(event) {
        // Display the event narrative in the game text element
        gameText.innerHTML = `<p>${event.narrative}</p>`;

        // Check if the event has any choices for the player to make
        if (event.choices && event.choices.length > 0) {
            // Create a container for the choice buttons
            const buttonsContainer = document.createElement('div');

            // Iterate through each choice and create a button for it
            event.choices.forEach(choice => {
                const button = document.createElement("button");
                button.textContent = choice.text;
                button.addEventListener('click', () => {
                    // Handle the player's choice
                    handleEventChoice(event, choice);
                });
                buttonsContainer.appendChild(button);
            });

            // Append the buttons container to the game text element
            gameText.appendChild(buttonsContainer);
        } else {
            // If there are no choices, the event may just be informative
            // You might have a button to continue or automatically proceed
            const continueButton = document.createElement('button');
            continueButton.textContent = 'Continue';
            continueButton.addEventListener('click', () => {
                // Continue the game after the event
                presentNextScenario();
            });
            gameText.appendChild(continueButton);
        }
    }

    function handleEventChoice(event, choice) {
        // If the choice has consequences, handle them
        if (choice.consequences) {
            handleConsequences(choice.consequences);
        }

        // If the choice moves the game to the next scenario or event
        if (choice.nextEventId) {
            // Find and present the next event
            const nextEvent = events.find(e => e.id === choice.nextEventId);
            if (nextEvent) {
                presentEvent(nextEvent);
            }
        } else if (choice.nextScenarioId) {
            // Find and present the next scenario
            const nextScenario = [...sequentialScenarios, ...randomScenarios].find(s => s.id === choice.nextScenarioId);
            if (nextScenario) {
                presentScenario(nextScenario);
            }
        } else {
            // If there's no specified next step, just proceed in the game
            presentNextScenario();
        }
    }

// Add this function to present a specific scenario based on its ID
    function presentScenario(scenario) {
        if (scenario.input) {
            // Display input field and submit button
            displayInputScenario(scenario);
        } else {
            // Display choice buttons
            displayChoiceScenario(scenario);
        }
    }

// Function to present a random scenario
    function presentRandomScenario() {
        handleRoundProgression(); // Handle round progression and random events
        // Filter out scenarios that have already been presented
        const newScenarios = randomScenarios.filter(scenario => !isScenarioInHistory(scenario));

        const relevantScenarios = newScenarios.filter(scenario => {
            // check if scenario is in history
            if (scenarioHistory.includes(scenario.id)) return false;
            console.log(scenarioHistory)
            if (!scenario.condition) return true; // If no condition is specified, the scenario is always relevant
            // Check if the condition matches the current company data
            //companyData.triggerEventRound[scenario.condition.target] = companyData.round;
            // console log filtered scenarios from relevant scenarios

            return companyData[scenario.condition.target] === scenario.condition.value;
        });
        console.log(relevantScenarios)
        // Select a random scenario from the filtered list
        const scenario = getRandomScenario(relevantScenarios);
        if (scenario) {
            // Present the chosen random scenario
            displayChoiceScenario(scenario);
            addToScenarioHistory(scenario);
        } else {
            // No more random scenarios or conditions not met for any scenario
            console.log("No more scenarios or conditions not met.");
            // Handle this situation, maybe by ending the game or looping scenarios
        }
    }

function isScenarioInHistory(scenario) {
    return scenarioHistory.some(historyScenario => historyScenario.id === scenario.id);
}

function addToScenarioHistory(scenario) {
    // Add the scenario to the beginning of the history
    scenarioHistory.unshift(scenario);
    console.log(scenarioHistory)

    // Ensure the history doesn't exceed the maximum length
    if (scenarioHistory.length > maxHistoryLength) {
        scenarioHistory.pop(); // Remove the oldest scenario
    }
}

// Function to display a scenario with input field
    function displayInputScenario(scenario) {
        console.log('display input scenario')
        gameText.innerHTML = `<p>${scenario.narrative}</p>`;
        const inputField = document.createElement("input");
        inputField.setAttribute("type", scenario.input.type);
        inputField.setAttribute("placeholder", scenario.input.placeholder);
        const submitButton = document.createElement("button");
        submitButton.textContent = scenario.input.submitText;
        submitButton.addEventListener("click", () => {
            const inputValue = inputField.value;
            handleInputChoice(scenario, inputValue);
        });
        gameText.appendChild(inputField);
        gameText.appendChild(submitButton);
    }

// Function to handle the input choice and its consequences
    function handleInputChoice(scenario, inputValue) {
        console.log('handle input choice');
          if (scenario.triggerEvent) {
            companyData.eventsTriggerRound[scenario.triggerEvent.event] = companyData.round + scenario.triggerEvent.roundsAfter;
          }

        let choiceConsequences;

        // If the effect is to select a random AI Implementer, handle it separately
        if (scenario.effect && scenario.effect.type === "randomAIImplementer") {
            handleRandomAIImplementerEffect(scenario);
            return; // Exit early since the rest of the logic will be handled after selection
        }

        // Update the company data based on the input choice
        if (scenario.effect && scenario.effect.type === "update") {
            companyData[scenario.effect.target] = (typeof inputValue === 'object' && inputValue.effect) ? inputValue.effect.value : inputValue;

            // If there are consequences to this choice, note them down for later processing
            choiceConsequences = inputValue.consequences || scenario.consequences;
        }

        // If the current scenario is the start of the game, change the game state and move to random scenarios
        if (scenario.id === "gamescenariostart") {
            companyData.gameState = inputValue.effect.value; // this should be set to "game"
            presentRandomScenario();
            return; // Exit the function since we're now moving to a different phase of the game
        }

        // Display any consequences of the chosen action and handle them
        if (choiceConsequences) {
            gameText.innerHTML = `<p>${choiceConsequences.text}</p>`;
            handleConsequences(choiceConsequences);
        }

        // Check for events triggered by the choice made
        checkForEvents(); // New addition to check for triggered events

        // Proceed to the next scenario if the game hasn't ended
        if (!checkEndgameEvents()) { // Check if the game has ended
            presentNextScenario();
        }
    }
}
function checkForEvents() {
  Object.keys(companyData.eventsTriggerRound).forEach(eventId => {
    if (companyData.round === companyData.eventsTriggerRound[eventId]) {
      let event = events.find(e => e.id === eventId);
      if (event && event.triggerCondition && companyData[event.triggerCondition.workforceAnalysts] === "AI") {
        presentEvent(event);
        // Reset the trigger round to avoid re-triggering
        companyData.eventsTriggerRound[eventId] = null;
      }
    }
  });
}

function displayChoiceScenario(scenario) {
    console.log('display choice scenario');
    // if previousConsequences is undefined, ignore
    console.log('find previous consequences in displaychoicescenario')
    console.log(previousConsequences)
                const consequencesContainer = document.getElementById('consequence')
            // clear current consequences text
  if (consequencesContainer.hasChildNodes()) {
    // Remove all existing children nodes from the consequencesContainer
    while (consequencesContainer.firstChild) {
        consequencesContainer.removeChild(consequencesContainer.firstChild);
    }
}

        if (previousConsequences && previousConsequences.text) {
            console.log('creating follow up')

        const previousConsequencesText = document.createElement("p");
        previousConsequencesText.textContent = ` ${previousConsequences.text}`;
        previousConsequencesText.style.color = 'grey';
        console.log(previousConsequencesText)
        consequencesContainer.appendChild(previousConsequencesText);
    }

    // Format and display the narrative for the scenario
    const narrative = formatNarrative(scenario.narrative, companyData);
    gameText.innerHTML = `<p>${narrative}</p>`;


    const choiceButtons = document.createElement("div");
    scenario.choices.forEach(choice => {
        const button = document.createElement("button");
        button.textContent = choice.text;
        button.addEventListener("click", () => {
            // Update the company data based on the choice effect
            if (choice.effect && choice.effect.type === "update") {
                companyData[choice.effect.target] = choice.effect.value;
            }
            // Handle consequences if any
            if (choice.consequences) {
                handleConsequences(choice.consequences);
            }
            // Proceed to the next scenario
            presentNextScenario();
        });
        choiceButtons.appendChild(button);
    });
    gameText.appendChild(choiceButtons);
}


function handleRandomAIImplementerEffect() {

  console.log('handle random AI implementer effect')

    // Generate 4 random choices
    const implementers = [
        "AI Corp",
        "Tech Innovators",
        "FutureTech Solutions",
        "AI Innovations Inc.",
        "Ninja Futures Tech",
        "Hardcore Scabbiosso LTD",
        "Pinkertons II, Technology Limited",
        "AI AI AI! AI Solutions",
        "Good Skynet Co",
        "Happy AI Limited",
        "Boring Machine Learning Company",
        "Vladimir's AI Solutions",
        "Notascam Inc.",
        "Robot Rockstars",
        "AI AI Captain",
        "Ain't No Party Like an AI Party",
        "It Ain't a Bug, It's a Feature",
        "AI for the People",
        "AI for the Animals",
        "Good Intentions Inc."
    ];
  // Shuffle array and take the first 4 elements
  const choices = shuffleArray(implementers).slice(0, 4);

  // Clear previous choices if any
  gameText.innerHTML = '<p>Choose an AI implementer for your company:</p>';
  const buttonsContainer = document.createElement('div');
  console.log(choices)

  // Create buttons for implementer choices
  choices.forEach(implementer => {
    const button = document.createElement("button");
    button.textContent = implementer;
    console.log(button)
    button.addEventListener('click', function() {
      // Set the chosen implementer and display the selection
      companyData['aiImplementer'] = implementer;
      gameText.innerHTML = `<p>You selected ${implementer} as your AI implementer.</p>`;
      // Proceed to the next scenario
      presentNextScenario();
    });
    buttonsContainer.appendChild(button);
  });

  gameText.appendChild(buttonsContainer);
}

// Helper function to shuffle an array
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]]; // Swap elements
  }
  return array;
}

presentNextScenario();




// Function to check for and handle endgame events
function checkEndgameEvents() {
  for (const event of endgameEvents) {
    if (event.condition(companyData)) {
      // Trigger the endgame event
      gameText.innerHTML = `<p>${event.narrative}</p>`;
      // Perform any additional endgame logic
      handleEndgame(event.effect);
      return true; // End the game
    }
  }
  return false; // Game continues
}
function checkForEvents() {
    // Check if the current round matches any event's triggerRound plus the round of the initial event
    const relevantEvents = events.filter(event =>
        companyData.round === (companyData.triggerEventRound + event.triggerRound) &&
        companyData[event.triggerCondition.workforceMarketers] === event.triggerCondition.workforceMarketers
    );

    for (const event of relevantEvents) {
        // Trigger the event
        presentEvent(event);
    }
}



function handleEndgame(effect) {
  if (effect === 'endgame') {
    // Disable further actions, display endgame options, etc.
    console.log('The game has ended due to:', effect);
    // Here you can redirect to a game over screen, show replay options, etc.
  }
}

function handleRoundProgression() {
  companyData.round++; // Increment round number
  console.log('Round: ' + companyData.round);
    // check if event should be triggered
   // checkForEvents();

  // Check if a random event should be triggered
  if (Math.random() < 0.02) { // 20% chance to trigger a random event
    triggerRandomEvent();
  }
}

function triggerRandomEvent() {
  // Define your random events
  const randomEvents = [
    {
      id: 'goodPress',
      condition: (companyData) => companyData.customerSatisfaction > 5,
      narrative: 'Your company has received positive media coverage for customer satisfaction!',
      effect: { shareholderSatisfaction: 2 } // Example effect
    }, {
    id: 'badPress',
    condition: (companyData) => companyData.customerSatisfaction < -5,
    narrative: 'Your company has received negative media coverage for customer dissatisfaction.',
    effect: { shareholderSatisfaction: -2 } // Example effect
    },
      {
          id: 'rivalbrand',
            condition: (companyData) => companyData.customerSatisfaction < -5,
            narrative: 'Your competitor has unveiled a futuristic buying AI.',
            effect: { shareholderSatisfaction: -2 } // Example effect

      }
  ];

  // Filter events based on their condition
  const possibleEvents = randomEvents.filter(event => event.condition(companyData));

  // If there are any possible events, select one at random to trigger
  if (possibleEvents.length > 0) {
    const event = possibleEvents[Math.floor(Math.random() * possibleEvents.length)];
      // Clear the previous content
  gameText.innerHTML = '';
  // Display the event narrative and add a continue button
  gameText.innerHTML = `<p>${event.narrative}</p>`;
  const continueButton = document.createElement('button');
  continueButton.textContent = 'Continue';
  gameText.appendChild(continueButton);
  continueButton.addEventListener('click', () => {
    // Handle what happens after the event
    handlePostEventLogic();
  });
}

function handlePostEventLogic() {
  // Clear the previous content
  gameText.innerHTML = '';
  // Check for endgame or proceed to next scenario
  if (!checkEndgameEvents()) {
    presentNextScenario();
  }
}
}