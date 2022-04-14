import React, { Component, Profiler } from 'react';
import logo from '../logo.svg';
import '../css/Header.css';
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';
import Profile from './Profile';

class Header extends Component {

    navTo(uri){
      window.location.href = window.location.origin + uri;
    }

    
    render() {
      
      return (
        <div className="App-header">
          <h1 onClick={() => {this.navTo('')}}>Boardgame Forum</h1>
          <Profile />
          <LoginButton />
          <LogoutButton />
        </div>
      );
    }
  }
  
  export default Header;