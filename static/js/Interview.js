function fetchQuestions(domain) {
    const endpoint = `https://ominous-enigma-g6pj5g6rj542w7wv-5001.app.github.dev/question_generation/${domain}`;

    // Using fetch to make a GET request to the endpoint
    return fetch(endpoint)
        .then(response => {
            // Check if the response is successful (status code 200)
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            // Parse JSON response
            return response.json();
        })
        .then(data => {
            // Extract and return the response array from the parsed JSON data
            return data.response;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle errors gracefully
            return []; // or throw error based on use case
        });
}

// Example usage:
// const domain = 'django'; // Replace 'example' with the actual domain
// fetchQuestions(domain)
//     .then(questions => {
//         console.log('Fetched questions:', questions);
//         // Process the fetched questions here
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         // Handle error if needed
//     });

