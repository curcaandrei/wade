import React, { useState, useEffect } from 'react';
import '../../css/modal-card.css';
const ModalCard=({person})=>{
    const [isRotated, setIsRotated] = useState(false);

    const onRotate = () => setIsRotated((rotated) => !rotated);
  
    return (
        <div className={`rotative-card ${isRotated ? 'rotate' : ''}`} key={person.id} onClick={onRotate}>
        {/* Display person information on the front side of the card */}
        <div className="card-front">
        <img src={person.profilePicture} alt="Profile" />
          <p>Name: {person.name}</p>
          <p>Work: {person.work}</p>
          <p>City: {person.city}</p>
        </div>
        {/* Display otherInfo on the back side of the card */}
        <div className="card-back">
          <p>Other Info: {person.otherInfo}</p>
        </div>
      </div>
    );
}
export default ModalCard;