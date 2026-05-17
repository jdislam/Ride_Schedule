// --- START OF FILE gemini2.js ---

import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "https://cdn.jsdelivr.net/npm/@google/generative-ai/+esm";

// --- Configuration ---
// WARNING: Storing API keys client-side is insecure for production. Use a backend proxy.
//const API_KEY = "AIzaSyCzDw4jYsl91ncl2wadhh9jpWdFmVtD0pg";
const API_KEY = "AIzaSyB9MEX_BMG0fmhdQPoGS2t19bxFoqFMP5k";
// const API_KEY = "AIzaSyCtAUsfYtkvHS69pPmefA_54lseRh276MI";
// const API_KEY = "AIzaSyACrU66ejkJV4-K2cWoH9tEH1W8lcEKFx8";
//const MODEL_NAME = "gemini-1.5-pro-latest";
const MODEL_NAME = "gemini-2.0-flash";

// --- System Prompt for Guiding the AI ---
const systemPrompt = `
You are TravelCostBot, a friendly assistant specialized in estimating travel costs within Bangladesh. Follow these rules for every user query:

1. Understand the Query
    The user will say something like:
    “I am at [Origin] and I want to go to [Destination]. How much money do I need?”
    Both origin and destination will be places or landmarks within Bangladesh (e.g., Farmgate, Mirpur 1, Gulshan 2, Cox’s Bazar).
2. Determine the Distance
    Look up or estimate the driving distance between Origin and Destination in kilometers.
    If you have an exact value, use that.
    If only a range is available (e.g., 15–16 km), use that instead.
3. Compute the Fare
    Rate: 20 taka per kilometer
    If exact distance:
    Total Cost = Distance × 20 taka, round to the nearest taka.
    If distance range:
    Min Cost = Lower bound × 20 taka
    Max Cost = Upper bound × 20 taka
    Round both.
4. Format Your Reply
    Tone: Friendly and conversational.
    Include:
    Restate the trip (e.g., “From Farmgate to Mirpur 1…”)
    Show the distance (exact or range)
    Show the calculation
    Exact:
    15 km × 20 taka = 300 taka
    Range:
    15 km × 20 = 300 taka
    16 km × 20 = 320 taka
    Give the final answer
    Exact: “You’ll need about 300 taka.”
    Range: “You’ll need between 300 and 320 taka.”
    End with a polite sign-off or follow-up prompt
    (e.g., “Let me know if you want directions!”)
5. Example Responses
➤ Exact Distance Example
User: I’m at Farmgate and I want to go to Dhanmondi. How much money do I need?

Assistant:  
• Distance: 6 km  
• Cost: 6 km × 20 taka = 120 taka  
You’ll need about 120 taka to travel from Farmgate to Dhanmondi. 😊
➤ Range Example
User: I’m at Farmgate and I want to go to Mirpur 1. The distance is about 15–16 km. How much money do I need?

Assistant:  
• Distance: 15–16 km  
• Cost:  
   15 km × 20 taka = 300 taka  
   16 km × 20 taka = 320 taka  
You’ll need between 300 and 320 taka to travel from Farmgate to Mirpur 1. 😊
Always double‑check distances, do the math correctly, and keep your responses warm and helpful!
`;


// --- Conversation History (Optional for this specific task, but kept for structure) ---
// Note: For this focused task, we might not strictly need history,
// as the system prompt guides each interaction independently.
let chatHistory = [];
console.log("Initial chat history:", chatHistory);

// --- Initialize Gemini ---
let genAI;
let model;
try {
    genAI = new GoogleGenerativeAI(API_KEY);
    model = genAI.getGenerativeModel({ model: MODEL_NAME });
    console.log("GoogleGenerativeAI initialized successfully.");
} catch (error) {
    console.error("Error initializing GoogleGenerativeAI:", error);
    alert("Failed to initialize the AI service. Please check the API key and configuration in gemini2.js");
}

// --- Safety Settings ---
// Keeping safety settings minimal or moderate is usually fine for this use case.
// You can uncomment and adjust if needed, but BLOCK_NONE is generally not recommended.
const safetySettings = [
    { category: HarmCategory.HARM_CATEGORY_HARASSMENT,         threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,        threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,  threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
];
// const safetySettings = []; // Use with caution if specific content needs are understood


// --- Generation Configuration ---
const generationConfig = {
    temperature: 0.6, // Increased slightly for more natural language (adjust 0.5-0.7 as needed)
    topK: 1,
    topP: 0.95,
    maxOutputTokens: 256, // Increased slightly to allow for explanations
};




/**
 * Sends the system prompt + new user prompt to the Gemini API
 * and streams the response (expected to be category names or refusal).
 * Updates history upon successful completion.
 *
 * @param {string} newPrompt - The user's latest message (their interests).
 * @param {HTMLElement} targetElement - The message element to update.
 * @param {object} callbacks - UI update callback functions.
 */
async function streamChatResponse(newPrompt, targetElement, callbacks) {
    if (!model) {
        const errorMsg = "AI Model is not initialized. Check API Key and console.";
        console.error(errorMsg);
        callbacks.onError(targetElement, errorMsg);
        callbacks.onComplete(targetElement); // Still complete UI flow
        return;
    }

    let fullResponse = "";
    let isFirstChunk = true;
    let streamHasData = false;

    // *** MODIFIED: Construct the input with the System Prompt ***
    // We combine the system instructions and the user's current query into one user turn.
    // For this task, sending the whole chatHistory might confuse the model,
    // so we send the instructions + current query each time.
    const messagesToSend = [
        {
            role: "user",
            parts: [{ text: systemPrompt + "\n\nUser's Interests:\n" + newPrompt }]
            // Note: We are NOT including the potentially long chatHistory here.
            // The systemPrompt provides all necessary context for *this specific task*.
        }
    ];

    console.log("Sending to Gemini (including system prompt):\n", messagesToSend[0].parts[0].text.substring(0, 500) + "..."); // Log start of prompt

    let result;
    try {
        console.log("Calling model.generateContentStream()...");
        result = await model.generateContentStream({
            contents: messagesToSend,
            generationConfig,
            safetySettings,
        });
        console.log("model.generateContentStream() call returned. Awaiting stream...");

        for await (const chunk of result.stream) {
            // console.log("Received stream chunk:", chunk); // Debugging

            // Immediate check for prompt feedback in the chunk itself (less common now)
            if (chunk.promptFeedback && chunk.promptFeedback.blockReason) {
                const blockMessage = `Blocked based on prompt (during stream): ${chunk.promptFeedback.blockReason}`;
                console.error(blockMessage);
                throw new Error(blockMessage);
            }

            const chunkText = chunk.text();
            // console.log("Extracted chunk text:", chunkText); // Debugging

            if (chunkText !== undefined && chunkText !== null) {
                if (chunkText.length > 0) {
                    streamHasData = true;
                    fullResponse += chunkText;
                    // **MODIFICATION**: Don't parse with Marked for this specific output.
                    // We expect plain text (category names or refusal message).
                    // If you *need* markdown elsewhere, conditionally apply it based on context.
                    // const parsedHtml = typeof marked !== 'undefined' ? marked.parse(fullResponse) : fullResponse;
                    const parsedHtml = typeof marked !== 'undefined' ? marked.parse(fullResponse) : fullResponse;
                    callbacks.onData(targetElement, parsedHtml, isFirstChunk);
                    isFirstChunk = false;
                }
            }
        }

        console.log("Finished iterating through stream.");

        // Check the final aggregated response object
        const finalResponse = await result.response;
        console.log("Final response object:", JSON.stringify(finalResponse, null, 2));

        const promptFeedback = finalResponse?.promptFeedback;
        const finishReason = finalResponse?.candidates?.[0]?.finishReason;
        const safetyRatings = finalResponse?.candidates?.[0]?.safetyRatings;

        // Check for blocks or unexpected finish reasons in the final response
        if (promptFeedback?.blockReason) {
            const blockMessage = `Request blocked by API. Reason: ${promptFeedback.blockReason}`;
            console.error(blockMessage);
            throw new Error(blockMessage);
        }

        if (finishReason && finishReason !== "STOP" && finishReason !== "MAX_TOKENS") {
             const reasonMessage = `Stream finished unexpectedly. Reason: ${finishReason}`;
             console.warn(reasonMessage, "Safety Ratings:", safetyRatings);
             if (finishReason === "SAFETY") {
                throw new Error("Response blocked by safety filters.");
             } else {
                 throw new Error(reasonMessage); // Other non-STOP reasons are errors here
             }
        }

        // Final check: Did we get any actual content?
        if (streamHasData) {
            console.log("Stream finished successfully with data. Updating history.");
            // Update history (optional, but can be useful for debugging UI)
            chatHistory.push({ role: "user", parts: [{ text: newPrompt }] }); // Store original user prompt
            chatHistory.push({ role: "model", parts: [{ text: fullResponse }] }); // Store AI response
            console.log("Updated History:", JSON.stringify(chatHistory.slice(-4))); // Log recent history
            callbacks.onComplete(targetElement);
        } else {
            // No stream data received, even if finishReason was STOP
            console.warn("Stream finished, but no text content was processed/received.");
             if (finishReason === "STOP") {
                 // This implies the model chose to generate nothing based on the prompt.
                 // Could be a refusal, or it genuinely couldn't find a category.
                 // Let's return a clearer message instead of a generic error.
                 callbacks.onError(targetElement, "The AI could not determine a suitable category or chose not to respond based on the input.");
                 callbacks.onComplete(targetElement); // Still complete UI flow
             } else {
                 // If reason wasn't STOP and no data, likely an underlying issue.
                 throw new Error("Received an empty response from the AI. (Reason Unknown)");
             }
        }

    } catch (error) {
        console.error("Error during Gemini stream processing:", error);
        callbacks.onError(targetElement, error.message || "An unknown error occurred while contacting the AI.");
        callbacks.onComplete(targetElement); // Ensure UI is re-enabled
    }
}

// Ensure the function is globally accessible for your other scripts (like scripts.js)
window.streamChatResponse = streamChatResponse;
console.log("streamChatResponse available on window?", typeof window.streamChatResponse === 'function');

// --- END OF FILE gemini2.js ---