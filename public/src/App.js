import React, { useState, useEffect } from "react";

function App() {
  // State to track which view is currently active (episodes list, guests list, etc.)
  const [view, setView] = useState("episodes");
  // Lists of episodes and guests fetched from the API
  const [episodes, setEpisodes] = useState([]);
  const [guests, setGuests] = useState([]);
  // Details for a specifically selected episode
  const [selectedEpisode, setSelectedEpisode] = useState(null);
  // Form state for creating a new appearance
  const [appearanceForm, setAppearanceForm] = useState({
    rating: 5,
    episode_id: "",
    guest_id: "",
  });
  // Feedback message for the user (success/error)
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchEpisodes();
    fetchGuests();
  }, []);

  // Fetch list of all episodes
  const fetchEpisodes = async () => {
    try {
      const response = await fetch("/episodes");
      const data = await response.json();
      setEpisodes(data);
    } catch (error) {
      console.error("Error fetching episodes:", error);
    }
  };

  const fetchGuests = async () => {
    try {
      const response = await fetch("/guests");
      const data = await response.json();
      setGuests(data);
    } catch (error) {
      console.error("Error fetching guests:", error);
    }
  };

  const fetchEpisodeDetails = async (id) => {
    try {
      const response = await fetch(`/episodes/${id}`);
      if (response.ok) {
        const data = await response.json();
        setSelectedEpisode(data);
        setView("episode-detail");
      }
    } catch (error) {
      console.error("Error fetching episode:", error);
    }
  };

  const handleDeleteEpisode = async (id, e) => {
    e.stopPropagation();
    try {
      const response = await fetch(`/episodes/${id}`, { method: "DELETE" });
      if (response.ok) {
        setMessage("Episode deleted successfully!");
        fetchEpisodes();
        if (selectedEpisode && selectedEpisode.id === id) {
          setView("episodes");
          setSelectedEpisode(null);
        }
      }
    } catch (error) {
      setMessage("Error deleting episode");
    }
  };

  // Submit the form to create a new Appearance
  const handleAppearanceSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/appearances", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(appearanceForm),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage("Appearance created successfully!");
        // Reset form after success
        setAppearanceForm({ rating: 5, episode_id: "", guest_id: "" });
        fetchEpisodes();
        fetchGuests();
      } else {
        // If the backend returns validation errors (status 400), we show them here
        setMessage("Error: " + JSON.stringify(data.errors || data));
      }
    } catch (error) {
      setMessage("Error creating appearance");
    }
  };

  const renderEpisodes = () => (
    <div>
      <h2>Episodes</h2>
      <div className="card-grid">
        {episodes.map((episode) => (
          <div
            key={episode.id}
            className="card"
            onClick={() => fetchEpisodeDetails(episode.id)}
          >
            <h3>Episode {episode.number}</h3>
            <p>Date: {episode.date}</p>
            <button onClick={(e) => handleDeleteEpisode(episode.id, e)}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderEpisodeDetail = () => (
    <div>
      <button onClick={() => setView("episodes")}>Back to Episodes</button>
      <h2>Episode {selectedEpisode.number}</h2>
      <p>Date: {selectedEpisode.date}</p>
      <h3>Appearances</h3>
      {selectedEpisode.appearances.map((appearance) => (
        <div key={appearance.id} className="appearance-card">
          <p>
            <strong>Guest:</strong> {appearance.guest.name}
          </p>
          <p>
            <strong>Occupation:</strong> {appearance.guest.occupation}
          </p>
          <p>
            <strong>Rating:</strong> {appearance.rating}/5
          </p>
        </div>
      ))}
    </div>
  );

  const renderGuests = () => (
    <div>
      <h2>Guests</h2>
      <div className="card-grid">
        {guests.map((guest) => (
          <div key={guest.id} className="card">
            <h3>{guest.name}</h3>
            <p>{guest.occupation}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCreateAppearance = () => (
    <div>
      <h2>Create New Appearance</h2>
      <form onSubmit={handleAppearanceSubmit}>
        <div>
          <label>Rating (1-5):</label>
          <select
            value={appearanceForm.rating}
            onChange={(e) =>
              setAppearanceForm({
                ...appearanceForm,
                rating: parseInt(e.target.value),
              })
            }
          >
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Episode:</label>
          <select
            value={appearanceForm.episode_id}
            onChange={(e) =>
              setAppearanceForm({
                ...appearanceForm,
                episode_id: parseInt(e.target.value),
              })
            }
            required
          >
            <option value="">Select Episode</option>
            {episodes.map((ep) => (
              <option key={ep.id} value={ep.id}>
                Episode {ep.number} - {ep.date}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Guest:</label>
          <select
            value={appearanceForm.guest_id}
            onChange={(e) =>
              setAppearanceForm({
                ...appearanceForm,
                guest_id: parseInt(e.target.value),
              })
            }
            required
          >
            <option value="">Select Guest</option>
            {guests.map((guest) => (
              <option key={guest.id} value={guest.id}>
                {guest.name} - {guest.occupation}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Create Appearance</button>
      </form>
    </div>
  );

  return (
    <div className="App">
      <h1>🎭 Late Show API</h1>
      <nav>
        <button onClick={() => setView("episodes")}>Episodes</button>
        <button onClick={() => setView("guests")}>Guests</button>
        <button onClick={() => setView("create")}>New Appearance</button>
      </nav>
      {message && <p className="message">{message}</p>}
      {view === "episodes" && renderEpisodes()}
      {view === "episode-detail" && renderEpisodeDetail()}
      {view === "guests" && renderGuests()}
      {view === "create" && renderCreateAppearance()}
    </div>
  );
}

export default App;