document.getElementById("analyze-button").addEventListener("click", () => {
    const videoUrl = document.getElementById("video-url").value;

    if (!videoUrl) {
        alert("Please enter a YouTube video URL!");
        return;
    }

    // Extract the video ID from the URL
    const videoId = videoUrl.split("v=")[1]?.split("&")[0];
    if (!videoId) {
        alert("Invalid YouTube video URL!");
        return;
    }

    // Send the video ID to the Flask backend
    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ video_id: videoId }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Update the results section with the analysis
            document.getElementById("positive-count").innerText = `Positive Comments: ${data.positive}`;
            document.getElementById("neutral-count").innerText = `Neutral Comments: ${data.neutral}`;
            document.getElementById("negative-count").innerText = `Negative Comments: ${data.negative}`;

            // Create a pie chart using the data
            const ctx = document.getElementById("sentiment-chart").getContext("2d");
            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["Positive", "Neutral", "Negative"],
                    datasets: [
                        {
                            data: [data.positive, data.neutral, data.negative],
                            backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
                        },
                    ],
                },
            });
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while analyzing the video.");
        });
});
