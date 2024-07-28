import React from 'react';

import './Title.css';

// const buttonStyle = {
//   padding: '10px 20px', // Adds padding to buttons
//   fontSize: '16px', // Increases font size
//   cursor: 'pointer', // Changes cursor to pointer on hover
// };

function Title(props) {
  return (
    <div className="heading">
      <div id="info">
        <h2>{props.title}</h2>
        <p>{props.total} Records</p>
      </div>
      <div id="navigation">
      {/* <Link to="/">
              <button style={buttonStyle}>Home</button>
            </Link> */}
      </div>
    </div>
  );
}

export default Title;
