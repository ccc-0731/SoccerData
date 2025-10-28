// ---------------------------------------------------------
// 1️⃣ Get references to HTML elements
// ---------------------------------------------------------
const slider = document.getElementById("slider");
const frameNum = document.getElementById("frame-number");
const canvas = document.getElementById("field");
const ctx = canvas.getContext("2d");

// ---------------------------------------------------------
// 2️⃣ Add an event listener: runs every time slider moves
// ---------------------------------------------------------
slider.addEventListener("input", async () => {
  // Get current frame number from slider
  const frame = slider.value;

  // Show frame number next to the slider
  frameNum.textContent = frame;

  // -------------------------------------------------------
  // 3️⃣ Ask Flask backend for that frame’s data
  // -------------------------------------------------------
  const response = await fetch(`/frame/${frame}`);
  const data = await response.json(); // Parse JSON into JS objects

  // -------------------------------------------------------
  // 4️⃣ Clear the canvas before drawing the next frame
  // -------------------------------------------------------
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // -------------------------------------------------------
  // 5️⃣ Draw simple dots for each detected player
  // -------------------------------------------------------
  data.forEach(p => {
    if (p.is_detected) {
      ctx.beginPath();

      // Scale down coordinates to fit in the canvas
      ctx.arc(p.x / 2, p.y / 2, 3, 0, Math.PI * 2);

      // Use color by team (adjust based on your data)
      ctx.fillStyle = p.team === "home" ? "blue" : "red";
      ctx.fill();
    }
  });
});
