import React, { useState} from 'react';
import '../../css/modal-card.css';
import LikeButton from '../../images/like-btn.png';
import DislikeButton from '../../images/dislike.png';
const ModalCard = ({ person }) => {
  const [isRotated, setIsRotated] = useState(false);
  const profile_picture="https://th.bing.com/th/id/OIP.B_atDrr4RpLoeIJmNsOCxgHaHa?rs=1&pid=ImgDetMain";
  const onRotate = () => setIsRotated((rotated) => !rotated);
  return (
    <div className={`rotative-card ${isRotated ? 'rotate' : ''}`} key={person.id} onClick={onRotate}>
      {/* Display person information on the front side of the card */}
      <div className="card-front">
        <div className="card-front-picture">
          <img src={profile_picture} alt="Profile" />
        </div>
        <div className="card-front-content">
          <p>Name: {person.userName}</p>
          <p>Work: {person.company}</p>
          <p>City: {person.city}</p>
        </div>
        <div className="card-front-buttons" >
          <button>
            <img src={LikeButton} alt="Like Btn" />
          </button>
          <button>
            <img src={DislikeButton} alt="Dislike btn" />
          </button>
        </div>
      </div>
      {/* Display otherInfo on the back side of the card */}
      <div className="card-back">
        <p>Other Info: {person.email}</p>
      </div>
    </div>
  );
}
export default ModalCard;