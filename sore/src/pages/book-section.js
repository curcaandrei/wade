import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/grid.css';
import { ToastContainer, toast } from 'react-toastify';
import { Bounce } from 'react-toastify';
const BookSection = ({ sectionTitle }) => {
  const [books, setBooks] = useState([]);
  const [selectedBooks, setSelectedBooks] = useState([]);
  const userId = localStorage.getItem('user_id');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBooks = async () => {
      setLoading(true);
      axios.post(`https://recommendation-dot-diesel-nova-412314.ew.r.appspot.com/recommendations/books/${userId}`)
      .then((response) => {
        console.log('Response books data:', response.data['results']);
        setBooks(response.data['results'])
      })
      .catch((error) => {
        // Handle error
        console.error('Error:', error);
      });
      setLoading(false);
    };
    fetchBooks();
  }, [userId]);
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

  const handleSelect = (book) => {
    notify('book was selected')
    setSelectedBooks((prevSelectedBooks) => [...prevSelectedBooks, book]);
   console.log(selectedBooks);
  };

  const handleSearch = async () => {
    notify('waiting for new recommendations');
    setLoading(true);
    axios.post(`https://recommendation-dot-diesel-nova-412314.ew.r.appspot.com/recommendations/books/${userId}`)
      .then((response) => {
        console.log('Response books data:', response.data['results']);
        setBooks(response.data['results'])
      })
      .catch((error) => {
        // Handle error
        console.error('Error:', error);
      });
      setLoading(false);
      setSelectedBooks([]);
    console.log('Searching with selected books:', selectedBooks);
  };

  return (
    <div>
      <h2>{sectionTitle}</h2>
      <ToastContainer />
      <button onClick={handleSearch}>Make recommandations</button>
      {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="grid-main">
            {
          books.map((book) => (
            <div key={book.bookId} className="card-main">
              <h2>{book.title}</h2>
              <p>{book.authors}</p>
              <p>{book.averageRating}</p>
              <button className="button-main" onClick={() => handleSelect(book)}>Select</button>
            </div>
             ))
}</div>
         
        )}
      </div>
    
  );
};
export default BookSection;