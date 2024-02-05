import React, { useState, useEffect } from 'react';
import AccountLogo from '../images/account.png';
import '../css/first-time.css';
import '../css/main-screen.css';
import ModalCard from '../pages/modal-component/modal-card';
import BookSection from './book-section';
import SongSection from './song-section';
import axios from 'axios';
const MainScreen = () => {
    const [loading, setLoading] = useState(true);
    const [personsMain, setPersonsMain] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const personsPerPage=5;
    const userId = localStorage.getItem('user_id');
    useEffect(() => {
        const fetchPersons = async () => {
          try {
            setLoading(true);
            console.log('start fetching...');
            const user=fetch(`https://userpf-dot-diesel-nova-412314.ew.r.appspot.com/users/${userId}`)
            .then(response => {
                if (!response.ok) {
                  throw new Error('Network response was not ok');
                }
                return response.json(); 
              })
              .then(data => {
                // Process the retrieved data
                console.log('Data:', data);
                findUsersByUserData(data);
              })
              .catch(error => {
                console.error('Fetch error:', error);
              });
          } catch (error) {
            console.error('Error fetching persons:', error);
          } finally {
            setLoading(false);
          }
        };
          fetchPersons();
      }, [ currentPage]);
const findUsersByUserData = async (data) => {
        // if (data['company'] && data['city']) {
        //     const company = data['company'];
        //     const city = data['city'];
    
            try {
                const response = await axios.get(`https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query/users?city=Iasi&company=Lidl`);
                const responseData = response.data;
                console.log('list users data: ',responseData);
                setPersonsMain(responseData);
                displayedPersons = personsMain.slice(startIndex, endIndex);
            } catch (error) {
                console.error('Error fetching users:', error);
                //setPersons([]);
            }
        // } else {
        //     setPersons([]);
        // }
    }
      const startIndex = (currentPage - 1) * personsPerPage;
      const endIndex = startIndex + personsPerPage;
      var displayedPersons = personsMain.slice(startIndex, endIndex);


    return (
        <div className='main-screen'>
            <div className="top-logo">
                <a href="/my-account">
                    <img src={AccountLogo} alt="Logo" />
                </a>
            </div>
            <div className='main-content' >
                <h3>Maybe you know them</h3>
                {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="person-list">
            {/* Map through the persons and display the rotative cards */}
            {displayedPersons.map(person => <ModalCard person={person} key={person.name}/>)}
          </div>
        )}
                <section className='info-container'>
                    <div className='info-card purple-back'>
                    <BookSection sectionTitle="Recommended books" />
                    </div>
                </section>
                <section className='info-container'>
                    <div className='info-card purple-back'>
                    <SongSection sectionTitle="Recommended Songs" />
                    </div>
                </section>
            </div>
        </div>

    );
}
export default MainScreen;