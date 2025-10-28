// Wait until the page is fully loaded
window.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("field");
  const ctx = canvas.getContext("2d");
  const slider = document.getElementById("slider");
  const frameNumber = document.getElementById("frame-number");

  // Function to load and draw a frame image from Flask
  async function loadFrame(frameId) {
    try {
      const response = await fetch(`/frame/${frameId}`);
      if (!response.ok) {
        console.error("Frame fetch failed:", response.status);
        return;
      }

      const blob = await response.blob(); // Get image bytes
      const img = new Image();

      img.onload = () => {
        // Clear the canvas before drawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };

      img.src = URL.createObjectURL(blob); // Convert blob to usable image
    } catch (err) {
      console.error("Error loading frame:", err);
    }
  }

  // When the slider moves, load that frame
  slider.addEventListener("input", () => {
    const frameId = slider.value;
    frameNumber.textContent = frameId;
    loadFrame(frameId);
  });

  // Load the first frame on startup
  loadFrame(0);
});
