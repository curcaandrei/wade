import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import { Bounce } from 'react-toastify';
const SongSection = ({ sectionTitle}) => {
    const [songs, setSongs] = useState([]);
    const [selectedSongs, setSelectedSongs] = useState([]);
    const userId = localStorage.getItem('user_id');
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      const fetchSongs = async () => {
        setLoading(true);
      axios.post(`https://recommendation-dot-diesel-nova-412314.ew.r.appspot.com/recommendations/music/${userId}`)
      .then((response) => {
        console.log('Response songs data:', response.data);
        setSongs(response.data)
      })
      .catch((error) => {
        // Handle error
        console.error('Error:', error);
      });
      setLoading(false);
      };
      fetchSongs();
    }, []);
    const notify = (message) => toast.info(message, {
      position: "top-right",
      autoClose: 1000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "light",
      transition: Bounce,
      });

    const handleSelect = (song) => {
      notify('song was selected');
      setSelectedSongs((prevSelectedSongs) => [...prevSelectedSongs, song]);
   
    };
  

    const handleSearch = () => {
      notify('wait for recommendations');
      setLoading(true);
      const postData={'favorite_songs':selectedSongs};
      axios.post('https://recommendation-dot-diesel-nova-412314.ew.r.appspot.com/recommendations/music',postData)
      .then((response) => {
        console.log('Response recomm songs data:', response.data);
        setSongs(response.data)
      })
      .catch((error) => {
        // Handle error
        console.error('Error:', error);
      });
      setSelectedSongs([]);
      setLoading(false);
      console.log('selected songs empty'+selectedSongs);
    };
 
    return (
      <div>
        <ToastContainer />
        <h2>{sectionTitle}</h2>
        <button onClick={handleSearch}>Make recommandations</button>
        {loading ? (
          <p>Loading...</p>
        ) : (<div className="grid-main">{
          songs.map((song) => (
            <div key={song.uri+song.track_name} className="card-main">
              <h3>Title: {song.track_name}</h3>
              <p>Artist: {song.artist_name}</p>
              <p>Album: {song.album_name}</p>
              <p>Genres: {song.genres}</p>
              <button className="button-main" onClick={() => handleSelect(song)}>Select</button>
            </div>  ))
            }
        </div>
        )}
       
      </div>
    );
  };
  
export default SongSection;