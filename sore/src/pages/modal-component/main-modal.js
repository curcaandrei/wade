import React, { useState, useEffect } from 'react';
import '../../css/modal.css';
import ModalCard from './modal-card';
const PersonModal = ({ isOpen, onClose }) => {
  const [persons, setPersons] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const personsPerPage=5;
  useEffect(() => {
    const fetchPersons = async () => {
      try {
        setLoading(true);
        console.log('start fetching...');
        const response = await fetch('./persons.json');
        const data = await response.json();
        console.log(data);
        setPersons(data);
      } catch (error) {
        console.error('Error fetching persons:', error);
      } finally {
        setLoading(false);
      }
    };

    if (isOpen) {
      fetchPersons();
    }
  }, [isOpen, currentPage]);

  const handleNextPage = () => {
    setCurrentPage(prevPage => prevPage + 1);
  };

  const handlePrevPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1));
  };
  const startIndex = (currentPage - 1) * personsPerPage;
  const endIndex = startIndex + personsPerPage;
  const displayedPersons = persons.slice(startIndex, endIndex);
  return (
    <div className={`modal ${isOpen ? 'open' : ''}`}>
      <div className="modal-content">
        <button className="close-button" onClick={onClose}>
          Close
        </button>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="person-list">
            {/* Map through the persons and display the rotative cards */}
            {displayedPersons.map(person => <ModalCard person={person} key={person.name}/>)}
          </div>
        )}
        <div className="pagination">
          <button onClick={handlePrevPage} disabled={currentPage === 1}>
            Prev
          </button>
          <span>{currentPage}</span>
          <button onClick={handleNextPage}>Next</button>
        </div>
      </div>
    </div>
  );
};

export default PersonModal;