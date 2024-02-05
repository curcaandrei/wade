import React, { useState, useEffect } from 'react';
import '../../css/modal.css';
import ModalCard from './modal-card';
import axios from 'axios';
const PersonModal = ({ isOpen, onClose }) => {
  const [skills, setSkills] = useState([]);
  const [cities, setCities] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [persons, setPersons] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [loadingResources, setLoadingResources] = useState(true);
  const personsPerPage=5;

  useEffect(() => {
    setLoadingResources(true);
    
    axios.get('https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query/skills')
      .then(response => {
        const skillsData = response.data;
        console.log('Skills Data:', skillsData);
        setSkills(skillsData?.results); // Update to handle potential undefined data
      })
      .catch(error => {
        console.error('Error fetching skills:', error);
      });
  
    axios.get('https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query/companies')
      .then(response => {
        const companiesData = response.data;
        console.log('Companies Data:', companiesData);
        setCompanies(companiesData?.results); // Update to handle potential undefined data
      })
      .catch(error => {
        console.error('Error fetching companies:', error);
      });
  
    axios.get('https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query/cities')
      .then(response => {
        const citiesData = response.data;
        console.log('Cities Data:', citiesData);
        setCities(citiesData?.results); // Update to handle potential undefined data
      })
      .catch(error => {
        console.error('Error fetching cities:', error);
      });
  
    setLoadingResources(false);
  }, []);
  
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

  const [selectedOptions, setSelectedOptions] = useState({});

  const handleSelectChange = (label, value) => {
    console.log('selected values:'+label+" "+value)
    setSelectedOptions(prevOptions => ({
      ...prevOptions,
      [label]: value
    }));
};
const handleButtonClick = async () => {
  try {
    setLoading(true);
    const queryParams = constructQueryParams(selectedOptions);
    const response = await axios.get(`https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query/users?${queryParams}`);
    const data = response.data
    console.log(data);
    setPersons(data);
    setSelectedOptions([]);
  } catch (error) {
    console.error('Error fetching users:', error);
  }finally{
    setLoading(false);
    displayedPersons = persons.slice(startIndex, endIndex);
  }
};

const constructQueryParams = (options, label, value) => {
  const updatedOptions = { ...options, [label]: value };
  const filteredOptions = Object.fromEntries(
    Object.entries(updatedOptions)
      .filter(([key, value]) => value !== undefined)
      .filter(([key, value]) => value !== 'skill')
  );
  const queryParams = Object.entries(filteredOptions)
    .map(([key, value]) => {
      // Modify the query parameter name based on the label
      const queryKey = key === 'Cities' ? 'city' : key === 'Companies' ? 'company' : 'skill';
      return `${queryKey}=${value}`;
    })
    .join('&');
    console.log('query params are 2'+queryParams)
  return queryParams;
};

  const startIndex = (currentPage - 1) * personsPerPage;
  const endIndex = startIndex + personsPerPage;
  var displayedPersons = persons.slice(startIndex, endIndex);
  return (
    <div className={`modal ${isOpen ? 'open' : ''}`}>
      <div className="modal-content">
        <div className='closeHeader'>
        <button className="close-button" onClick={onClose}>
          Close
        </button>
        </div>
        <div className='modal-header'>
       {
          loadingResources ? (
            <p>Loading...</p>
          ):
       [
            { label: "Skills", options: skills },
            { label: "Cities", options: cities },
            { label: "Companies", options: companies }
          ].map((dropdown, index) => (
            <div key={index}>
            {dropdown.options ? (
              <select className="dropdown" onChange={(e) => handleSelectChange(dropdown.label, e.target.value)}>
                <option value="">{`Select ${dropdown.label}`}</option>
                {dropdown.options.map((object, indexobj) => (
                  <option key={indexobj} value={object.name}>{object.name}</option>
                ))}
              </select>
            ) : (
              <select>
                <option value="">Empty</option>
              </select>
            )}
          </div>
          ))}
          <button onClick={handleButtonClick}>
            Search
          </button>
        </div>
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