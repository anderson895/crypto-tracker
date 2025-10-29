import "./style.css";

const app = document.getElementById("app");
app.innerHTML = `
  <h1>🚀 Meme Coin Tracker</h1>
  <div id="coins">Loading...</div>
`;

// const API_URL = "http://127.0.0.1:5000/api/prices";
const API_URL = "https://crypto-backend-eight-bay.vercel.app/api/prices";
const coinsDiv = document.getElementById("coins");

async function fetchPrices() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    displayCoins(data);
  } catch (err) {
    console.error("Error fetching prices:", err);
    coinsDiv.innerHTML = "<p>⚠️ Error fetching data</p>";
  }
}

function displayCoins(coins) {
  coinsDiv.innerHTML = ""; // Clear old content

  coins.forEach((coin) => {
    const div = document.createElement("div");
    div.className = `coin ${coin.trend}`;
    div.innerHTML = `
      <img src="${coin.icon}" alt="${coin.name}" class="coin-icon"/>
      <h3>${coin.name.charAt(0).toUpperCase() + coin.name.slice(1)}</h3>
      <p>$${coin.price.toFixed(8)}</p>
      <p>${
        coin.trend === "up"
          ? "📈 Increasing"
          : coin.trend === "down"
          ? "📉 Decreasing"
          : coin.trend === "same"
          ? "⚖️ Unchanged"
          : "💰 Tracking Started"
      }</p>
      <p>24h: ${coin.change_24h}%</p>
    `;
    coinsDiv.appendChild(div);
  });
}

// First load
fetchPrices();

// Refresh every 10 seconds
setInterval(fetchPrices, 10000);
