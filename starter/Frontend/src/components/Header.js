import React, { Component } from 'react';
import '../css/Header.css';
import AuthenticationButton from './Authorizedbutton';

class Header extends Component {

    navTo(uri){
      window.location.href = window.location.origin + uri;
    }

    
    render() {
      
      return (
        <div className="App-header">
          <h1 onClick={() => {this.navTo('')}}>Boardgame Forum</h1>
          <p onClick={() => {this.navTo('/createpost')}}>Create post</p>
          <p onClick={() => {this.navTo('/profile')}}>Profile</p>
          <AuthenticationButton />
        </div>
      );
    }
  }
  
  export default Header;